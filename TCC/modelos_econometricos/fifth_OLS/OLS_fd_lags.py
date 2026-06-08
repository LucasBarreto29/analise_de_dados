"""
MODELO DEFINITIVO - Pooled OLS Dinâmico em Diferenças com Driscoll-Kraay
-----------------------------------------------------------------------------------
Estimação final com painel completo (N=7). 
Corrigido para evitar o viés de seleção do log em taxas negativas utilizando 
o VAB_Indice_Volume diretamente. 

Atualização: 
1) Implementada Seleção de Lags via Critérios de Informação (AIC/BIC)
2) Adicionado Teste de Wald para significância do Efeito Acumulado (Opções 1 e 2)
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
import warnings
import os

warnings.filterwarnings('ignore')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------
# 1. CARREGAMENTO E TRANSFORMAÇÕES BÁSICAS
# ---------------------------------------------------------
df = pd.read_csv(os.path.join(BASE_DIR, "dados", "painel_mestre.csv"))

print("="*80)
print(" PREPARAÇÃO DOS DADOS (N=7) E CÁLCULO DE LAGS ")
print("="*80)

df.sort_values(by=['Setor', 'Trimestre'], inplace=True)

df['ln_Invest_Tech'] = np.log(df['Investimento_Tech_USD'])
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])

df['d_ln_Invest_Tech'] = df.groupby('Setor')['ln_Invest_Tech'].diff()
df['d_ln_Produtividade'] = df.groupby('Setor')['ln_Produtividade'].diff()

for i in range(1, 5):
    df[f'd_ln_Invest_Tech_Lag{i}'] = df.groupby('Setor')['d_ln_Invest_Tech'].shift(i)

df['VAB_Industria_Growth'] = df['VAB_Industria_Volume']
covid_quarters = ['2020q2', '2020q3', '2020q4', '2021q1', '2021q2']
df['covid_periodo'] = df['Trimestre'].isin(covid_quarters).astype(int)

# ---------------------------------------------------------
# 2. SELEÇÃO DA ESTRUTURA DE LAGS (AIC/BIC)
# ---------------------------------------------------------
print("\n" + "="*80)
print(" FASE 1: SELEÇÃO DE LAGS VIA AIC E BIC (Amostra Fixa para Comparação) ")
print("="*80)

# Para comparar os critérios, a amostra precisa ser exatamente a mesma (perda de lags 1 a 4).
df_fixed = df.dropna(subset=['d_ln_Produtividade', 'd_ln_Invest_Tech_Lag1', 
                             'd_ln_Invest_Tech_Lag2', 'd_ln_Invest_Tech_Lag3', 
                             'd_ln_Invest_Tech_Lag4', 'VAB_Industria_Growth']).copy()

df_fixed['Trimestre_dt'] = pd.PeriodIndex(df_fixed['Trimestre'], freq='Q').to_timestamp()
df_fixed = df_fixed.set_index(['Setor', 'Trimestre_dt'])

endog_fixed = df_fixed['d_ln_Produtividade']
resultados_ic = []

for lag_count in range(1, 5):
    exog_vars = [f'd_ln_Invest_Tech_Lag{i}' for i in range(1, lag_count + 1)] + ['VAB_Industria_Growth', 'covid_periodo']
    exog_fixed = sm.add_constant(df_fixed[exog_vars])
    
    # Estimamos por OLS convencional apenas para extrair as métricas clássicas de AIC/BIC
    mod_sm = sm.OLS(endog_fixed.values, exog_fixed.values).fit()
    resultados_ic.append({
        'Qtd_Lags': lag_count,
        'AIC': mod_sm.aic,
        'BIC': mod_sm.bic
    })

df_ic = pd.DataFrame(resultados_ic)
print(df_ic.to_string(index=False))

# AIC costuma ser melhor para predição e preservação de dinâmica temporal em painéis curtos
best_lag_aic = df_ic.loc[df_ic['AIC'].idxmin(), 'Qtd_Lags']
print(f"\n-> Optando pela indicação do AIC: Modelo com {best_lag_aic} Lags.")

# ---------------------------------------------------------
# 3. ESTIMAÇÃO OFICIAL (RECUPERANDO GRAUS DE LIBERDADE)
# ---------------------------------------------------------
print("\n" + "="*80)
print(f" FASE 2: MODELO DEFINITIVO COM {best_lag_aic} LAGS (Driscoll-Kraay) ")
print("="*80)

# Reconstruindo a amostra usando apenas os lags necessários, ganhando observações!
subset_necessario = ['d_ln_Produtividade', 'VAB_Industria_Growth'] + [f'd_ln_Invest_Tech_Lag{i}' for i in range(1, best_lag_aic + 1)]
df_final = df.dropna(subset=subset_necessario).copy()

df_final['Trimestre_dt'] = pd.PeriodIndex(df_final['Trimestre'], freq='Q').to_timestamp()
df_final = df_final.set_index(['Setor', 'Trimestre_dt'])

print(f"Amostra ampliada: Recuperamos observações. Total agora: {len(df_final)} obs.")

exog_vars_final = [f'd_ln_Invest_Tech_Lag{i}' for i in range(1, best_lag_aic + 1)] + ['VAB_Industria_Growth', 'covid_periodo']
exog_final = sm.add_constant(df_final[exog_vars_final])
endog_final = df_final['d_ln_Produtividade']

modelo_definitivo = PanelOLS(endog_final, exog_final, entity_effects=False)
res_definitivo = modelo_definitivo.fit(cov_type='kernel')

print(res_definitivo.summary)

# ---------------------------------------------------------
# 4. TESTE DE WALD (EFEITO ACUMULADO)
# ---------------------------------------------------------
print("\n" + "="*80)
print(" FASE 3: TESTE DE WALD PARA EFEITO ACUMULADO DA TECNOLOGIA ")
print("="*80)

if best_lag_aic > 1:
    formula_wald = " + ".join([f"d_ln_Invest_Tech_Lag{i}" for i in range(1, best_lag_aic + 1)]) + " = 0"
    try:
        wald_res = res_definitivo.wald_test(formula=formula_wald)
        print(f"H0 (Hipótese Nula): Soma dos coeficientes de Tech (Lags 1 a {best_lag_aic}) = 0")
        print(f"Estatística Chi-quadrado: {wald_res.stat:.4f}")
        print(f"P-valor do Efeito Acumulado: {wald_res.pval:.4f}")
        
        if wald_res.pval < 0.10:
            print("-> CONCLUSÃO: O efeito acumulado da tecnologia é ESTATISTICAMENTE SIGNIFICATIVO no tempo!")
        else:
            print("-> CONCLUSÃO: O efeito acumulado continua não significativo estatisticamente (mas ganhamos graus de liberdade).")
    except Exception as e:
        print("Erro ao tentar fazer teste de wald:", e)
else:
    print("Apenas 1 lag no modelo. O Teste de Wald para efeito acumulado equivale ao próprio p-valor do Lag 1.")

print("="*80)
