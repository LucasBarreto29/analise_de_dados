import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PooledOLS, PanelOLS, RandomEffects
from statsmodels.tsa.stattools import adfuller
from scipy import stats
import warnings
import os
warnings.filterwarnings('ignore')

print("=== INICIANDO ETAPA 1: PREPARAÇÃO E MODELAGEM EM NÍVEL ===")

# 1. Limpeza e Transformação
df = pd.read_csv('/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/painel_bartik.csv')
df = df.dropna(subset=['Bartik_Tech_it']).copy()

df['Period'] = pd.PeriodIndex(df['Trimestre'].str.replace('q', 'Q', case=False), freq='Q').to_timestamp()
df = df.set_index(['Setor', 'Period'])

df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])
df['ln_Bartik_Tech'] = np.log(df['Bartik_Tech_it'])
df['const'] = 1

# 2. Teste de Raiz Unitária (ADF por Setor)
print("\n--- Teste de Raiz Unitária (ADF) na ln_Produtividade por Setor ---")
for setor in df.index.levels[0]:
    serie = df.xs(setor, level='Setor')['ln_Produtividade']
    resultado_adf = adfuller(serie, autolag='AIC')
    print(f"Setor: {setor} | ADF Stat: {resultado_adf[0]:.4f} | p-value: {resultado_adf[1]:.4f}")

print("\nNota: Se a maioria dos p-valores for > 0.05, a série possui raiz unitária (é I(1)).")

# 3. Modelos Clássicos
exog_vars = ['const', 'ln_Bartik_Tech', 'VAB_Industria_Volume', 'Stringency_Index']

# Pooled OLS
mod_pooled = PooledOLS(df['ln_Produtividade'], df[exog_vars])
res_pooled = mod_pooled.fit()

# Fixed Effects
mod_fe = PanelOLS(df['ln_Produtividade'], df[exog_vars], entity_effects=True)
res_fe = mod_fe.fit()

# Random Effects
mod_re = RandomEffects(df['ln_Produtividade'], df[exog_vars])
res_re = mod_re.fit()

print("\n--- Teste F de Poolability (Fixed Effects vs Pooled OLS) ---")
print(f"F-statistic: {res_fe.f_pooled.stat:.4f}")
print(f"P-value:     {res_fe.f_pooled.pval:.4f}")
if res_fe.f_pooled.pval < 0.05:
    print("Conclusão: Rejeitamos H0. Fixed Effects é superior ao Pooled OLS.")
else:
    print("Conclusão: Não rejeitamos H0. Pooled OLS é adequado.")

print("\n--- Teste de Hausman (Fixed Effects vs Random Effects) ---")
b_fe = res_fe.params.drop('const', errors='ignore')
b_re = res_re.params.drop('const', errors='ignore')
cov_fe = res_fe.cov.drop(index='const', columns='const', errors='ignore')
cov_re = res_re.cov.drop(index='const', columns='const', errors='ignore')

try:
    df_hausman = len(b_fe)
    diff = b_fe - b_re
    cov_diff = cov_fe - cov_re
    hausman_stat = diff.T @ np.linalg.inv(cov_diff) @ diff
    pval_hausman = stats.chi2.sf(hausman_stat, df_hausman)
    print(f"Chi-Square: {hausman_stat:.4f}")
    print(f"P-value:    {pval_hausman:.4f}")
    if pval_hausman < 0.05:
        print("Conclusão: Rejeitamos H0. Fixed Effects é preferível a Random Effects.")
    else:
        print("Conclusão: Não rejeitamos H0. Random Effects é preferível.")
except Exception as e:
    print("Não foi possível calcular o teste de Hausman (provável matriz de covariância não definida positivamente). Erro:", e)
    print("Assumiremos Fixed Effects por precaução com endogeneidade do modelo.")

print("\n=== SUMMARY DO MODELO VENCEDOR (FIXED EFFECTS - EM NÍVEL) ===")
print(res_fe.summary)
