"""
MQO com Efeitos Fixos (First OLS)
----------------------------------
Variável dependente (Y): Produtividade_Hora_Habitual (FGV)
Variável independente (X): Investimento_Tech_USD (Comex Stat)
Controle: VAB_Indice_Volume (IBGE Contas Nacionais)
Efeitos Fixos: por Setor (entidade) e por Trimestre (tempo)

Estimado via LSDV (Least Squares Dummy Variables).
A constante (Intercept) representa a categoria de referência
do setor (APU), com todos os demais setores expressos
como desvios em relação a ela.
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import os
import warnings
warnings.filterwarnings('ignore')

# Caminho relativo ao próprio script (funciona independente de onde é chamado)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ==============================================
# 1. CARREGAR E PREPARAR
# ==============================================
df = pd.read_csv(os.path.join(BASE_DIR, "dados", "painel_mestre.csv"))

df['ln_Invest_Tech']   = np.log(df['Investimento_Tech_USD'])
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])
df['Setor']      = df['Setor'].astype('category')
df['Trimestre']  = df['Trimestre'].astype('category')

print("="*60)
print("       MQO COM EFEITOS FIXOS (LSDV) — PAINEL")
print("="*60)
print(f"\n→ Setores:              {df['Setor'].nunique()}")
print(f"→ Trimestres:           {df['Trimestre'].nunique()}")
print(f"→ Observações totais:   {len(df)}\n")

# ==============================================
# 2. MODELO 1 — Efeitos Fixos de Setor
# ==============================================
# A constante (Intercept) está incluída por padrão pelo statsmodels.
# C(Setor) cria dummies para todos os setores menos um (APU = referência).
# O Intercept captura o nível médio da produtividade do setor de referência.
modelo1 = smf.ols(
    formula='ln_Produtividade ~ ln_Invest_Tech + VAB_Indice_Volume + C(Setor)',
    data=df
).fit(cov_type='HC3')

print("-"*60)
print("MODELO 1: EF de Setor (sem EF de Tempo)")
print("-"*60)
print(modelo1.summary())

# ==============================================
# 3. MODELO 2 — Two-Way FE (Setor + Tempo)
# ==============================================
# Aqui o Intercept continua presente e absorve a dupla referência:
# setor APU no trimestre 2012q1.
modelo2 = smf.ols(
    formula='ln_Produtividade ~ ln_Invest_Tech + VAB_Indice_Volume + C(Setor) + C(Trimestre)',
    data=df
).fit(cov_type='HC3')

print("\n" + "-"*60)
print("MODELO 2: Two-Way FE (Setor + Tempo)")
print("-"*60)
print(modelo2.summary())

# ==============================================
# 4. INTERPRETAÇÃO DO MODELO 2
# ==============================================
beta = modelo2.params['ln_Invest_Tech']
p    = modelo2.pvalues['ln_Invest_Tech']
sig  = '***' if p < 0.01 else ('**' if p < 0.05 else ('*' if p < 0.1 else 'não significativo'))

print("\n" + "="*60)
print("INTERPRETAÇÃO DO MODELO 2 (Two-Way FE)")
print("="*60)
print(f"→ Elasticidade Tech: {beta:.4f} ({sig})")
if p < 0.1:
    print(f"  Um aumento de 1% no investimento em importações de TI")
    print(f"  está associado a uma variação de {beta:.4f}% na produtividade")
    print(f"  dos setores de serviços, controlando por VAB e EF.")
else:
    print("  O coeficiente não é estatisticamente significativo.")
print("\n[FIM DO TESTE]\n")
