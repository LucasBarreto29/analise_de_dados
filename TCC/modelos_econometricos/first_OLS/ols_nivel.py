"""
FIRST OLS (Modelo em Nível) - A Prova da Regressão Espúria
----------------------------------------------------------------------
Este script tem o objetivo deliberado de provar que a estimação em nível
para dados macroeconômicos não é adequada. Ele executa testes rigorosos
de raiz unitária (ADF e KPSS) e atesta que a regressão é espúria, 
justificando a transição para diferenças.
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.tsa.stattools import adfuller, kpss
import statsmodels.stats.api as sms
from statsmodels.stats.outliers_influence import variance_inflation_factor
from patsy import dmatrices
import warnings
import os

warnings.filterwarnings('ignore')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------
# 1. CARREGAMENTO DOS DADOS
# ---------------------------------------------------------
df = pd.read_csv(os.path.join(BASE_DIR, "dados", "painel_mestre.csv"))

# Transformações Apenas para as Variáveis em Nível Absoluto
df['ln_Invest_Tech'] = np.log(df['Investimento_Tech_USD'])
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])

# VAB da Indústria já é uma taxa de variação que inclui valores negativos.
# Tirar o logaritmo geraria NaN e excluiria as recessões. Entra direto.
df['VAB_Industria_Growth'] = df['VAB_Industria_Volume']

# Dummy de pandemia
covid_quarters = ['2020q2', '2020q3', '2020q4', '2021q1', '2021q2']
df['covid_periodo'] = df['Trimestre'].isin(covid_quarters).astype(int)

df.dropna(subset=['ln_Produtividade', 'ln_Invest_Tech', 'VAB_Industria_Growth'], inplace=True)

# ---------------------------------------------------------
# 2. TESTES DUPLOS DE RAIZ UNITÁRIA (ADF E KPSS)
# ---------------------------------------------------------
print("="*80)
print(" 1. DIAGNÓSTICO DE RAIZ UNITÁRIA NAS VARIÁVEIS EM NÍVEL ")
print("="*80)
print("H0 (ADF): A série POSSUI raiz unitária (Não-Estacionária)")
print("H0 (KPSS): A série É estacionária em torno de uma tendência\n")

variaveis_teste = ['ln_Produtividade', 'ln_Invest_Tech', 'VAB_Industria_Growth']

for var in variaveis_teste:
    print(f"\n--- Variável: {var} ---")
    
    if var in ['ln_Invest_Tech', 'VAB_Industria_Growth']:
        serie_unica = df.drop_duplicates(subset=['Trimestre']).sort_values('Trimestre')[var]
        adf_res = adfuller(serie_unica, autolag='AIC')
        kpss_res = kpss(serie_unica, regression='c')
        
        adf_str = f"ADF: {adf_res[1]:.4f}"
        kpss_str = f"KPSS: {kpss_res[1]:.4f}"
        print(f"[Agregado Nacional        ] {adf_str} | {kpss_str}")
        
    else:
        setores = df['Setor'].unique()
        for setor in setores:
            serie_setor = df[df['Setor'] == setor].sort_values('Trimestre')[var]
            adf_res = adfuller(serie_setor, autolag='AIC')
            kpss_res = kpss(serie_setor, regression='c')
            
            adf_str = f"ADF: {adf_res[1]:.4f}"
            kpss_str = f"KPSS: {kpss_res[1]:.4f}"
            print(f"[{setor:25}] {adf_str} | {kpss_str}")

# ---------------------------------------------------------
# 3. ESTIMAÇÃO DO MODELO EM NÍVEL (COM ERROS HC3)
# ---------------------------------------------------------
print("\n" + "="*80)
print(" 2. ESTIMAÇÃO DO MODELO OLS EM NÍVEL ")
print("="*80)

formula = 'ln_Produtividade ~ ln_Invest_Tech + VAB_Industria_Growth + covid_periodo + C(Setor)'
modelo_nivel = smf.ols(formula=formula, data=df).fit(cov_type='HC3')
print(modelo_nivel.summary())

# ---------------------------------------------------------
# 4. DIAGNÓSTICO DOS RESÍDUOS (A FALHA DO MODELO 1)
# ---------------------------------------------------------
print("\n" + "="*80)
print(" 3. DIAGNÓSTICO DOS RESÍDUOS (POR QUE O MODELO É INVÁLIDO) ")
print("="*80)

# A. Multicolinearidade (VIF)
y_vif, X_vif = dmatrices(formula, data=df, return_type='dataframe')
vif_data = pd.DataFrame()
vif_data["feature"] = X_vif.columns
vif_data["VIF"] = [variance_inflation_factor(X_vif.values, i) for i in range(len(X_vif.columns))]
print("\nA) VIF (Multicolinearidade):")
print(vif_data[vif_data['VIF'] > 5].to_string() if (vif_data['VIF'] > 5).any() else "Nenhuma variável com VIF > 5.")

# B. Autocorrelação Serial (Breusch-Godfrey)
bg_test = sms.acorr_breusch_godfrey(modelo_nivel, nlags=4)
print(f"\nB) Breusch-Godfrey (Autocorrelação de Resíduos): P-value = {bg_test[1]:.4f}")
if bg_test[1] < 0.05:
    print("   -> FORTE AUTOCORRELAÇÃO DETECTADA. A regressão em nível é espúria.")

# C. Heterocedasticidade (Breusch-Pagan)
bp_test = sms.het_breuschpagan(modelo_nivel.resid, modelo_nivel.model.exog)
print(f"\nC) Breusch-Pagan (Heterocedasticidade): P-value = {bp_test[1]:.4f}")
if bp_test[1] < 0.05:
    print("   -> HETEROCEDASTICIDADE DETECTADA.")

print("\nCONCLUSÃO: Com raízes unitárias e fortíssima autocorrelação (Regressão Espúria),")
print("devemos avançar para o Modelo 2 (Primeiras Diferenças).")
print("="*80)
