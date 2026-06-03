import pandas as pd
import numpy as np
import os
import warnings
from linearmodels.panel import PooledOLS
from statsmodels.stats.outliers_influence import variance_inflation_factor
from patsy import dmatrices

warnings.filterwarnings('ignore')
# Ajuste do BASE_DIR para resolver a raiz da pasta TCC
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. PREPARAÇÃO DOS DADOS
df = pd.read_csv(os.path.join(BASE_DIR, "dados", "painel_mestre.csv"))
df = df[df['Setor'] != 'Comércio']

df['ln_Invest_Tech'] = np.log(df['Investimento_Tech_USD'])
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])
df['ln_VAB_Industria'] = np.log(df['VAB_Industria_Volume'])

df.sort_values(by=['Setor', 'Trimestre'], inplace=True)
df['d_ln_Produtividade'] = df.groupby('Setor')['ln_Produtividade'].diff()
df['d_ln_Invest_Tech'] = df.groupby('Setor')['ln_Invest_Tech'].diff()
df['d_ln_VAB_Industria'] = df.groupby('Setor')['ln_VAB_Industria'].diff()

for i in range(1, 5):
    df[f'd_ln_Invest_Tech_L{i}'] = df.groupby('Setor')['d_ln_Invest_Tech'].shift(i)

covid_quarters = ['2020q2', '2020q3', '2020q4', '2021q1', '2021q2']
df['covid_periodo'] = df['Trimestre'].isin(covid_quarters).astype(int)

df_diff = df.dropna().copy()
df_diff['Trimestre_id'] = df_diff['Trimestre'].str.replace('q', '').astype(int)
df_diff = df_diff.set_index(['Setor', 'Trimestre_id'], drop=False)

# 2. ESTIMAÇÃO COM DRISCOLL-KRAAY
print("="*80)
print(" MODELO DEFINITIVO - IMPACTO DA TECNOLOGIA NOS SERVIÇOS ")
print("="*80)

formula = (
    'd_ln_Produtividade ~ 1 + d_ln_Invest_Tech_L1 + d_ln_Invest_Tech_L2 + '
    'd_ln_Invest_Tech_L3 + d_ln_Invest_Tech_L4 + d_ln_VAB_Industria + '
    'covid_periodo + C(Setor)'
)

modelo = PooledOLS.from_formula(formula, data=df_diff)
res = modelo.fit(cov_type='kernel', kernel='newey-west', bandwidth=4)
print(res.summary)

# 3. DIAGNÓSTICO DE VIF
print("\n" + "="*80)
print(" DIAGNÓSTICO DE MULTICOLINEARIDADE (VIF) ")
print("="*80)
y, X = dmatrices(formula, data=df_diff.reset_index(drop=True), return_type='dataframe')
vif_data = pd.DataFrame()
vif_data["Variavel"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
print(vif_data)
print("="*80)
