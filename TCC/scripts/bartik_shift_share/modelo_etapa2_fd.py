import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("=== INICIANDO ETAPA 2: MODELAGEM EM DIFERENÇAS E DIAGNÓSTICOS ===")

# 1. Carregamento e Transformação
df = pd.read_csv('/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/painel_bartik.csv')
df = df.dropna(subset=['Bartik_Tech_it']).copy()
df['Period'] = pd.PeriodIndex(df['Trimestre'].str.replace('q', 'Q', case=False), freq='Q').to_timestamp()
df = df.set_index(['Setor', 'Period'])

# Logs
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])
df['ln_Bartik_Tech'] = np.log(df['Bartik_Tech_it'])

# Diferenciação
df['d_ln_Produtividade'] = df.groupby(level='Setor')['ln_Produtividade'].diff()
df['d_ln_Bartik_Tech'] = df.groupby(level='Setor')['ln_Bartik_Tech'].diff()

# Dropar as primeiras linhas que ficaram com NA após diff()
df = df.dropna(subset=['d_ln_Produtividade', 'd_ln_Bartik_Tech'])
df['const'] = 1

# 2. Estimação do Modelo em Diferenças
exog_vars = ['const', 'd_ln_Bartik_Tech', 'VAB_Industria_Volume', 'Stringency_Index']
mod_fd = PanelOLS(df['d_ln_Produtividade'], df[exog_vars], entity_effects=True)
res_fd = mod_fd.fit()

print("\n=== SUMMARY DO MODELO EM PRIMEIRA DIFERENÇA (FD) ===")
print(res_fd.summary)

# 3. Extração dos Resíduos e Testes de Diagnóstico
resids = res_fd.resids

print("\n--- TESTES DE DIAGNÓSTICO DOS RESÍDUOS ---")

# 3.1 Heterocedasticidade (Breusch-Pagan)
# Como linearmodels droppa o index no design matrix em certas chamadas, alinhamos perfeitamente
exog_matrix = df[exog_vars]
bp_test = het_breuschpagan(resids, exog_matrix)
print(f"1. Teste de Breusch-Pagan (Heterocedasticidade)")
print(f"   LM Statistic: {bp_test[0]:.4f}")
print(f"   LM p-value:   {bp_test[1]:.4f}")
if bp_test[1] < 0.05:
    print("   Conclusão: Rejeitamos H0. Há evidências de heterocedasticidade.")
else:
    print("   Conclusão: Não rejeitamos H0. Resíduos homocedásticos.")

# 3.2 Autocorrelação Serial (Durbin-Watson)
dw_stat = durbin_watson(resids)
print(f"\n2. Teste Durbin-Watson (Autocorrelação Serial)")
print(f"   Estatística DW: {dw_stat:.4f}")
if dw_stat < 1.5:
    print("   Conclusão: Indícios de autocorrelação positiva forte.")
elif dw_stat > 2.5:
    print("   Conclusão: Indícios de autocorrelação negativa forte.")
else:
    print("   Conclusão: Perto de 2. Sem evidências fortes de autocorrelação de 1ª ordem.")

# 3.3 Dependência Transversal (Pesaran CD Test)
# Reformular os resíduos para T x N
res_wide = resids.unstack('Setor')
T = len(res_wide)
N = len(res_wide.columns)

# Matriz de correlação dos resíduos cross-section
corr_matrix = res_wide.corr()

# Extrair as correlações pairwise (abaixo da diagonal principal)
rho_ij = []
for i in range(N):
    for j in range(i+1, N):
        rho_ij.append(corr_matrix.iloc[i, j])

pesaran_cd = np.sqrt(2 * T / (N * (N - 1))) * np.sum(rho_ij)
pval_pesaran = 2 * (1 - stats.norm.cdf(abs(pesaran_cd)))

print(f"\n3. Teste CD de Pesaran (Dependência Transversal - Cross-Sectional Dependence)")
print(f"   CD Statistic: {pesaran_cd:.4f}")
print(f"   p-value:      {pval_pesaran:.4f}")
if pval_pesaran < 0.05:
    print("   Conclusão: Rejeitamos H0. Há presença de DEPENDÊNCIA TRANSVERSAL (Cross-Sectional Dependence).")
    print("   (Choques contemporâneos não observados afetam os setores simultaneamente).")
else:
    print("   Conclusão: Não rejeitamos H0. Sem dependência transversal.")
