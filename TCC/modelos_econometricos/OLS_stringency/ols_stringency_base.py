"""
OLS STRINGENCY (BASE / LAG 0) - Modelo Contemporâneo e Seleção de Lags
----------------------------------------------------------------------
Este script utiliza o Stringency Index (nível) como substituto para a dummy de COVID.
O objetivo é avaliar o impacto contemporâneo da tecnologia sob os erros de 
Driscoll-Kraay e rodar a seleção iterativa (AIC/BIC) para definir 
os lags que usaremos no modelo subsequente.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
import warnings
import os

warnings.filterwarnings('ignore')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 1. Carregamento do Painel V2
df = pd.read_csv(os.path.join(BASE_DIR, "dados", "painel_mestre_v2.csv"))

print("="*80)
print(" 1. PREPARAÇÃO DA BASE (STRINGENCY INDEX EM NÍVEL) ")
print("="*80)

df.sort_values(by=['Setor', 'Trimestre'], inplace=True)

# Lidar com os NAs gerados na conversão e manter Stringency_Index como float
# Lembrete: Nível para Stringency e VAB_Ind, Diferença para Tech e Produtividade
df['ln_Invest_Tech'] = np.log(df['Investimento_Tech_USD'])
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])

df['d_ln_Invest_Tech'] = df.groupby('Setor')['ln_Invest_Tech'].diff()
df['d_ln_Produtividade'] = df.groupby('Setor')['ln_Produtividade'].diff()

# VAB Indústria já é taxa, Stringency Index entra em nível pois é limitado (estacionário por natureza)
df['VAB_Industria_Growth'] = df['VAB_Industria_Volume']
# Transformar Stringency_Index para escala decimal para coeficiente mais legível (opcional, vamos manter original 0-100)
# Podemos normalizar o stringency index para facilitar a convergência e leitura do coeficiente:
df['Stringency_Index_Norm'] = df['Stringency_Index'] / 100.0

for i in range(1, 5):
    df[f'd_ln_Invest_Tech_Lag{i}'] = df.groupby('Setor')['d_ln_Invest_Tech'].shift(i)

# Configurar Painel
df_model = df.dropna(subset=['d_ln_Produtividade', 'd_ln_Invest_Tech', 'VAB_Industria_Growth', 'Stringency_Index_Norm']).copy()
df_model['Trimestre_dt'] = pd.PeriodIndex(df_model['Trimestre'], freq='Q').to_timestamp()
df_model = df_model.set_index(['Setor', 'Trimestre_dt'])

print(f"Base contemporânea configurada: {len(df_model)} observações.")

# 2. Modelo Contemporâneo Base (Lag 0)
print("\n" + "="*80)
print(" 2. MODELO BASE CONTEMPORÂNEO (LAG 0) ")
print("="*80)

exog_vars_base = ['d_ln_Invest_Tech', 'VAB_Industria_Growth', 'Stringency_Index_Norm']
exog_base = sm.add_constant(df_model[exog_vars_base])
endog_base = df_model['d_ln_Produtividade']

modelo_base = PanelOLS(endog_base, exog_base, entity_effects=False)
res_base = modelo_base.fit(cov_type='kernel')
print(res_base.summary)

# 3. Seleção de Lags (AIC / BIC)
print("\n" + "="*80)
print(" 3. TESTE ITERATIVO DE SELEÇÃO DE LAGS (AIC / BIC) ")
print("="*80)

df_fixed = df.dropna(subset=['d_ln_Produtividade', 'd_ln_Invest_Tech_Lag1', 
                             'd_ln_Invest_Tech_Lag2', 'd_ln_Invest_Tech_Lag3', 
                             'd_ln_Invest_Tech_Lag4', 'VAB_Industria_Growth', 
                             'Stringency_Index_Norm']).copy()
df_fixed['Trimestre_dt'] = pd.PeriodIndex(df_fixed['Trimestre'], freq='Q').to_timestamp()
df_fixed = df_fixed.set_index(['Setor', 'Trimestre_dt'])

endog_fixed = df_fixed['d_ln_Produtividade']
resultados_ic = []

for lag_count in range(1, 5):
    exog_vars = [f'd_ln_Invest_Tech_Lag{i}' for i in range(1, lag_count + 1)] + ['VAB_Industria_Growth', 'Stringency_Index_Norm']
    exog_fixed = sm.add_constant(df_fixed[exog_vars])
    
    mod_sm = sm.OLS(endog_fixed.values, exog_fixed.values).fit()
    resultados_ic.append({
        'Qtd_Lags': lag_count,
        'AIC': mod_sm.aic,
        'BIC': mod_sm.bic
    })

df_ic = pd.DataFrame(resultados_ic)
print(df_ic.to_string(index=False))

best_lag_aic = df_ic.loc[df_ic['AIC'].idxmin(), 'Qtd_Lags']
print(f"\n-> Recomendação AIC: Utilizar {best_lag_aic} Lags no modelo definitivo.")
print("================================================================================")
