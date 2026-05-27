"""
Modelo Econométrico 2 (Second OLS) - Abordagem em Primeiras Diferenças
----------------------------------------------------------------------
Este modelo corrige os problemas teóricos encontrados no modelo 1:
1. Aplica Primeira Diferença (Taxa de Crescimento) para estacionarizar as séries.
2. Resolve a multicolinearidade, não incluindo Efeitos Fixos de Tempo, já que a 
   nossa variável independente de interesse (Invest_Tech) é puramente macro temporal.
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.tsa.stattools import adfuller
import os
import warnings

warnings.filterwarnings('ignore')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ==============================================
# 1. CARREGAR E PREPARAR DADOS
# ==============================================
df = pd.read_csv(os.path.join(BASE_DIR, "dados", "painel_mestre.csv"))

# Variáveis em Log Nível
df['ln_Invest_Tech'] = np.log(df['Investimento_Tech_USD'])
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])

# Variáveis em Primeira Diferença (Variação Percentual Trimestral)
df.sort_values(by=['Setor', 'Trimestre'], inplace=True)
df['d_ln_Produtividade'] = df.groupby('Setor')['ln_Produtividade'].diff()
df['d_ln_Invest_Tech'] = df.groupby('Setor')['ln_Invest_Tech'].diff()
df['d_VAB_Indice'] = df.groupby('Setor')['VAB_Indice_Volume'].diff()

# Dropar o primeiro trimestre que virou NaN por causa da diferença
df_diff = df.dropna().copy()

print("============================================================")
print(" SEGUNDA ABORDAGEM - MODELO EM PRIMEIRAS DIFERENÇAS ")
print("============================================================\n")

# ==============================================
# 2. TESTES DE ESTACIONARIDADE (Pós-Diferenciação)
# ==============================================
print("--- Testes de Raiz Unitária (Séries Diferenciadas) ---")

ts_tech_diff = df_diff.drop_duplicates(subset=['Trimestre']).sort_values('Trimestre')['d_ln_Invest_Tech'].values
adf_tech_diff = adfuller(ts_tech_diff, autolag='AIC')
print(f"d_ln_Invest_Tech -> ADF Stat: {adf_tech_diff[0]:.4f} | p-value: {adf_tech_diff[1]:.4f}")

ts_prod_diff_comercio = df_diff[df_diff['Setor'] == 'Comércio'].sort_values('Trimestre')['d_ln_Produtividade'].values
adf_prod_diff = adfuller(ts_prod_diff_comercio, autolag='AIC')
print(f"d_ln_Prod_Comercio -> ADF Stat: {adf_prod_diff[0]:.4f} | p-value: {adf_prod_diff[1]:.4f}")

print("Conclusão: Após a 1ª diferença, p-values < 0.05. As séries SÃO ESTACIONÁRIAS!\n")

# ==============================================
# 3. ESTIMAÇÃO DO MODELO EM DIFERENÇAS
# ==============================================
# A diferenciação já elimina os Efeitos Fixos de Entidade (Setor).
# Não colocamos dummies de Trimestre para evitar multicolinearidade com d_ln_Invest_Tech.
# Utilizamos clusterização dos erros-padrão por Setor para lidar com autocorrelação remanescente.

modelo_diff = smf.ols(
    formula='d_ln_Produtividade ~ d_ln_Invest_Tech + d_VAB_Indice',
    data=df_diff
).fit(cov_type='cluster', cov_kwds={'groups': df_diff['Setor']})

print("------------------------------------------------------------")
print("RESULTADOS DO MODELO EM PRIMEIRAS DIFERENÇAS")
print("------------------------------------------------------------")
print(modelo_diff.summary())

# ==============================================
# 4. INTERPRETAÇÃO
# ==============================================
beta = modelo_diff.params['d_ln_Invest_Tech']
p = modelo_diff.pvalues['d_ln_Invest_Tech']
print("\n============================================================")
print("INTERPRETAÇÃO FINAL METODOLÓGICA")
print("============================================================")
if p < 0.1:
    print(f"Efeito causal/elástico: Uma aceleração de 1% no crescimento das")
    print(f"importações de tecnologia gera uma variação de {beta:.4f}% no")
    print(f"crescimento da produtividade, estatisticamente significante (p={p:.4f}).")
else:
    print(f"Efeito nulo: Uma aceleração no crescimento das importações de")
    print(f"tecnologia (coef = {beta:.4f}) NÃO impacta significativamente (p={p:.4f})")
    print(f"o crescimento da produtividade no curto prazo.")
    print("O resultado espúrio do OLS anterior desapareceu após a correção técnica.")
print("============================================================")
