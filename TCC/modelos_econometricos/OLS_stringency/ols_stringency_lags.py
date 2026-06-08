"""
OLS STRINGENCY (MODELO FINAL COM LAGS) - Pooled OLS com Driscoll-Kraay
----------------------------------------------------------------------
Este script implementa o modelo sugerido pela rotina de seleção (AIC/BIC),
que recomendou 2 defasagens para o investimento em tecnologia.
O Stringency Index entra em nível (limitando a variação entre 0-1) para 
controlar os lockdowns governamentais no Brasil.
Inclui o Teste de Wald para significância do efeito acumulado da tecnologia.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
import warnings
import os

warnings.filterwarnings('ignore')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 1. Carregamento e Preparação da Base
df = pd.read_csv(os.path.join(BASE_DIR, "dados", "painel_mestre_v2.csv"))

print("="*80)
print(" 1. PREPARAÇÃO DA BASE E ESTRUTURAÇÃO DOS LAGS (2 LAGS) ")
print("="*80)

df.sort_values(by=['Setor', 'Trimestre'], inplace=True)

df['ln_Invest_Tech'] = np.log(df['Investimento_Tech_USD'])
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])

df['d_ln_Invest_Tech'] = df.groupby('Setor')['ln_Invest_Tech'].diff()
df['d_ln_Produtividade'] = df.groupby('Setor')['ln_Produtividade'].diff()

df['VAB_Industria_Growth'] = df['VAB_Industria_Volume']
df['Stringency_Index_Norm'] = df['Stringency_Index'] / 100.0

# O modelo utilizará 2 lags conforme indicado pelo AIC
num_lags = 2
for i in range(1, num_lags + 1):
    df[f'd_ln_Invest_Tech_Lag{i}'] = df.groupby('Setor')['d_ln_Invest_Tech'].shift(i)

# Omitimos NAs baseados estritamente nas variáveis utilizadas para salvar observações
subset_necessario = ['d_ln_Produtividade', 'VAB_Industria_Growth', 'Stringency_Index_Norm'] + [f'd_ln_Invest_Tech_Lag{i}' for i in range(1, num_lags + 1)]
df_model = df.dropna(subset=subset_necessario).copy()

df_model['Trimestre_dt'] = pd.PeriodIndex(df_model['Trimestre'], freq='Q').to_timestamp()
df_model = df_model.set_index(['Setor', 'Trimestre_dt'])

print(f"Base de dados final configurada com {len(df_model)} observações.")

# 2. Estimação do Modelo
print("\n" + "="*80)
print(f" 2. ESTIMAÇÃO DO MODELO COM STRINGENCY INDEX E {num_lags} LAGS DE TECH ")
print("="*80)

exog_vars = [f'd_ln_Invest_Tech_Lag{i}' for i in range(1, num_lags + 1)] + ['VAB_Industria_Growth', 'Stringency_Index_Norm']
exog = sm.add_constant(df_model[exog_vars])
endog = df_model['d_ln_Produtividade']

modelo_lags = PanelOLS(endog, exog, entity_effects=False)
res_lags = modelo_lags.fit(cov_type='kernel')

print(res_lags.summary)

# 3. Teste de Wald
print("\n" + "="*80)
print(" 3. TESTE DE WALD PARA O EFEITO ACUMULADO DA TECNOLOGIA ")
print("="*80)

formula_wald = " + ".join([f"d_ln_Invest_Tech_Lag{i}" for i in range(1, num_lags + 1)]) + " = 0"
try:
    wald_res = res_lags.wald_test(formula=formula_wald)
    print(f"H0: Soma dos coeficientes de Tech (Lags 1 a {num_lags}) = 0")
    print(f"Estatística Chi-quadrado: {wald_res.stat:.4f}")
    print(f"P-valor: {wald_res.pval:.4f}")
    
    if wald_res.pval < 0.10:
        print("-> CONCLUSÃO: O efeito acumulado da tecnologia é ESTATISTICAMENTE SIGNIFICATIVO (p < 0.10).")
    else:
        print("-> CONCLUSÃO: O efeito acumulado continua não significativo estatisticamente.")
except Exception as e:
    print("Erro no Teste de Wald:", e)

print("="*80)
