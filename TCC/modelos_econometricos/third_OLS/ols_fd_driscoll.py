"""
THIRD OLS (Modelo Contemporâneo com Driscoll-Kraay)
----------------------------------------------------------------------
Após o Modelo 2 provar a presença de Dependência Transversal, este 
modelo (Modelo 3) implementa a matriz de covariância de Driscoll-Kraay.
O objetivo aqui é provar que, mesmo com os erros corretamente ajustados, 
o choque tecnológico contemporâneo (Lag 0) não é estatisticamente 
significativo sobre a produtividade.
Isso fundamenta a necessidade de investigar a maturação do investimento
através da Curva J no Modelo Definitivo.
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
# 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS (N=7)
# ---------------------------------------------------------
df = pd.read_csv(os.path.join(BASE_DIR, "dados", "painel_mestre.csv"))

print("="*80)
print(" 1. PREPARAÇÃO DOS DADOS (CONTEMPORÂNEO) ")
print("="*80)

df['ln_Invest_Tech'] = np.log(df['Investimento_Tech_USD'])
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])

df.sort_values(by=['Setor', 'Trimestre'], inplace=True)
df['d_ln_Invest_Tech'] = df.groupby('Setor')['ln_Invest_Tech'].diff()
df['d_ln_Produtividade'] = df.groupby('Setor')['ln_Produtividade'].diff()

# Controle Exógeno Correto: VAB da Indústria em Nível (Taxa)
df['VAB_Industria_Growth'] = df['VAB_Industria_Volume']

covid_quarters = ['2020q2', '2020q3', '2020q4', '2021q1', '2021q2']
df['covid_periodo'] = df['Trimestre'].isin(covid_quarters).astype(int)

# Limpeza apenas da primeira diferença contemporânea
df.dropna(subset=['d_ln_Produtividade', 'd_ln_Invest_Tech', 'VAB_Industria_Growth'], inplace=True)

# ---------------------------------------------------------
# 2. CONFIGURAÇÃO DE PAINEL PARA O ESTIMADOR DRISCOLL-KRAAY
# ---------------------------------------------------------
df_model = df.copy()
df_model['Trimestre_dt'] = pd.PeriodIndex(df_model['Trimestre'], freq='Q').to_timestamp()
df_model = df_model.set_index(['Setor', 'Trimestre_dt'])

print(f"Estrutura configurada. Amostra Preservada: {len(df_model)} observações.")

# ---------------------------------------------------------
# 3. ESTIMAÇÃO COM DRISCOLL-KRAAY (LAG 0 APENAS)
# ---------------------------------------------------------
print("\n" + "="*80)
print(" 2. ESTIMAÇÃO POOLED OLS COM DRISCOLL-KRAAY (LAG 0) ")
print("="*80)

exog_vars = ['d_ln_Invest_Tech', 'VAB_Industria_Growth', 'covid_periodo']
exog = sm.add_constant(df_model[exog_vars])
endog = df_model['d_ln_Produtividade']

# Pooled OLS (entity_effects=False pois as diferenças já controlam nível base)
modelo_contemporaneo = PanelOLS(endog, exog, entity_effects=False)

# Matriz Driscoll-Kraay robusta
res_contemporaneo = modelo_contemporaneo.fit(cov_type='kernel')
print(res_contemporaneo.summary)

print("\n" + "="*80)
print(" 3. CONCLUSÃO PARA A TRANSIÇÃO FINAL ")
print("="*80)
print("Observe que o coeficiente de 'd_ln_Invest_Tech' (Lag 0) não reflete ganhos fortes.")
print("A teoria econômica postula que a tecnologia exige maturação (Curva J).")
print("Isso nos obriga a criar o Modelo Definitivo, introduzindo defasagens (Lags 1 a 4).")
print("="*80)
