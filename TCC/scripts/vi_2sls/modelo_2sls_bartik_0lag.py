import pandas as pd
from linearmodels.iv import IV2SLS
import warnings
warnings.filterwarnings('ignore')

print("=== INICIANDO MODELO 2SLS DEFINITIVO (0 LAGS / AIC OTIMIZADO) ===")

# 1. Carregamento do Painel
arquivo = '/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/painel_2sls_investimento.csv'
df = pd.read_csv(arquivo)

df['Period'] = pd.to_datetime(df['Period'])
df = df.set_index(['Setor', 'Period'])
df = df.sort_index()

# 2. O Instrumento Interagido e sua Defasagem
df['Instrumento_Bartik'] = df['Share_2012q1'] * df['d_ln_PPI_Semi']

# CRIAR A DEFASAGEM DO INSTRUMENTO ANTES DE LIMPAR OS DADOS
df['Instrumento_Bartik_lag1'] = df.groupby(level='Setor')['Instrumento_Bartik'].shift(1)
df['const'] = 1

# Matriz Estrita (0 Lags na Endógena, 1 Lag no Instrumento)
vars_todas = [
    'd_ln_Produtividade', 'const', 'd_ln_Cambio', 'VAB_Industria_Volume',
    'Impacto_tech_setor', 'Instrumento_Bartik_lag1' 
]

df_model = df[vars_todas].dropna()

# 3. Estimação com Mínimos Quadrados em Dois Estágios (2SLS)
dependent = df_model['d_ln_Produtividade']
exog = df_model[['const', 'd_ln_Cambio', 'VAB_Industria_Volume']]
endog = df_model[['Impacto_tech_setor']]

# INSTRUMENTANDO O INVESTIMENTO HOJE COM O PREÇO DE ONTEM
instruments = df_model[['Instrumento_Bartik_lag1']] 

iv_model = IV2SLS(dependent=dependent, exog=exog, endog=endog, instruments=instruments)
iv_res = iv_model.fit(cov_type='kernel')

print("\n================================================================================")
print("                 SUMÁRIO DO MODELO 2SLS DEFINITIVO (0 LAGS)                     ")
print("================================================================================")
print(iv_res.summary)
print("\n================================================================================")
print("                 DIAGNÓSTICO DO PRIMEIRO ESTÁGIO (FORÇA DO INSTRUMENTO)         ")
print("================================================================================")
print(iv_res.first_stage)
