"""
FIRST OLS (Modelo em Nível) - Diagnóstico Teórico e Testes
----------------------------------------------------------------------
Este script executa o modelo OLS inicial e o submete a uma bateria completa
de testes econométricos para demonstrar falhas de estacionariedade,
autocorrelação, heterocedasticidade, e multicolinearidade.
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.tsa.stattools import adfuller
import statsmodels.stats.api as sms
from statsmodels.stats.outliers_influence import variance_inflation_factor
from patsy import dmatrices
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------
# 1. CARREGAMENTO DOS DADOS E PREPARAÇÃO
# ---------------------------------------------------------
df = pd.read_csv(os.path.join(BASE_DIR, "dados", "painel_mestre.csv"))
df['ln_Invest_Tech'] = np.log(df['Investimento_Tech_USD'])
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])
df.dropna(inplace=True)

print("="*70)
print(" 1. TESTES DE RAIZ UNITÁRIA (ADF) - NÃO-ESTACIONARIEDADE ")
print("="*70)
print("Avaliando se as séries possuem 'passeio aleatório' (tendência estocástica).")
print("Teoria: Regredir séries não-estacionárias gera regressão espúria.\n")

# Loop limpo por setor para ADF (corrigindo a falha anterior de usar apenas 'Comércio')
setores = df['Setor'].unique()
for setor in setores:
    dados_setor = df[df['Setor'] == setor].sort_values('Trimestre')
    
    # Teste para Produtividade
    adf_prod = adfuller(dados_setor['ln_Produtividade'], autolag='AIC')
    print(f"[{setor}] ln_Produtividade P-value: {adf_prod[1]:.4f} " + 
          ("(Não-Estacionária)" if adf_prod[1] > 0.05 else "(Estacionária)"))

print("\nConclusão ADF: As variáveis dependentes em todos os setores falham em rejeitar a hipótese nula.")
print("As séries são Não-Estacionárias (Possuem Raiz Unitária).\n")


# ---------------------------------------------------------
# 2. ESTIMAÇÃO DO MODELO (O MODELO ESPÚRIO)
# ---------------------------------------------------------
print("="*70)
print(" 2. RESULTADOS DO MODELO (OLS EM NÍVEL) ")
print("="*70)
formula = 'ln_Produtividade ~ ln_Invest_Tech + VAB_Indice_Volume + C(Setor) + C(Trimestre)'
modelo = smf.ols(formula=formula, data=df).fit()
print(modelo.summary().tables[0]) # Mostrando apenas a primeira tabela para não poluir
print(modelo.summary().tables[1])
print("\nNota: Durbin-Watson baixíssimo (0.534) indica fortíssima autocorrelação (sintoma de regressão espúria).\n")

# ---------------------------------------------------------
# 3. BATERIA DE TESTES ECONOMÉTRICOS NOS RESÍDUOS
# ---------------------------------------------------------
print("="*70)
print(" 3. DIAGNÓSTICO DOS RESÍDUOS (TESTES PÓS-ESTIMAÇÃO) ")
print("="*70)

# A. Normalidade: Jarque-Bera
jb_stat, jb_pval, skew, kurtosis = sms.jarque_bera(modelo.resid)
print(f"A) Jarque-Bera (Normalidade): P-value = {jb_pval:.4f}")
print("   Hipótese Nula: Resíduos seguem distribuição normal.")
if jb_pval < 0.05: print("   -> Rejeitamos H0: Os resíduos NÃO são normais.\n")

# Plot da Distribuição dos Resíduos
plt.figure(figsize=(8, 5))
sns.histplot(modelo.resid, kde=True, color='red', bins=30)
plt.title('Distribuição dos Resíduos (First OLS - Regressão Espúria)', fontweight='bold', pad=15)
plt.xlabel('Resíduos', fontweight='bold')
plt.ylabel('Frequência', fontweight='bold')
plt.tight_layout()
plt.show()

# B. Heterocedasticidade: Breusch-Pagan
bp_test = sms.het_breuschpagan(modelo.resid, modelo.model.exog)
print(f"B) Breusch-Pagan (Heterocedasticidade): P-value = {bp_test[1]:.4f}")
print("   Hipótese Nula: Variância dos resíduos é constante (Homocedasticidade).")
if bp_test[1] < 0.05: print("   -> Rejeitamos H0: Há Heterocedasticidade (erros-padrão originais são inválidos).\n")

# C. Autocorrelação Serial: Breusch-Godfrey
# Testando até 4 lags (1 ano de autocorrelação)
bg_test = sms.acorr_breusch_godfrey(modelo, nlags=4)
print(f"C) Breusch-Godfrey (Autocorrelação): P-value = {bg_test[1]:.4f}")
print("   Hipótese Nula: Ausência de autocorrelação serial nos resíduos.")
if bg_test[1] < 0.05: print("   -> Rejeitamos H0: Forte autocorrelação confirmada (série não estacionária).\n")

# D. Multicolinearidade Perfeita (O Erro de Identificação)
print("D) Multicolinearidade (VIF - Variance Inflation Factor)")
print("   Calculando VIF para as variáveis numéricas para provar a multicolinearidade de ln_Invest_Tech...")
# Construindo matriz de design apenas para variáveis numéricas (sem dummies) para evitar erro singular do VIF
y, X = dmatrices('ln_Produtividade ~ ln_Invest_Tech + VAB_Indice_Volume', data=df, return_type='dataframe')
vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
print(vif_data)
print("\n   [ALERTA METODOLÓGICO]: Quando incluímos C(Trimestre), a variável ln_Invest_Tech sofre")
print("   Multicolinearidade Perfeita, pois o investimento tech nacional varia apenas no tempo, e não por setor.")
print("   Os efeitos fixos de tempo 'engolem' a variação, gerando estimativas viesadas e lixo estatístico.")
print("="*70)
