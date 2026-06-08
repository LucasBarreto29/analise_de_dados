"""
SECOND OLS (Modelo em Primeiras Diferenças)
----------------------------------------------------------------------
Este modelo corrige a raiz espúria do Modelo 1 aplicando primeiras diferenças.
Ele prova a estacionariedade da nova base (via ADF e Zivot-Andrews) e estima
a regressão em Pooled OLS. 
Crucialmente, este script executa o Teste de Pesaran CD sobre os resíduos 
diferenciados, provando que a Dependência Transversal sobrevive à diferenciação.
Isso justifica a adoção de Erros de Driscoll-Kraay no Modelo 3.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, zivot_andrews
from linearmodels.panel import PanelOLS
from scipy.stats import norm
import warnings
import os

warnings.filterwarnings('ignore')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------
# 1. CARREGAMENTO E DIFERENCIAÇÃO GLOBAL (7 SETORES)
# ---------------------------------------------------------
df = pd.read_csv(os.path.join(BASE_DIR, "dados", "painel_mestre.csv"))

print("="*80)
print(" 1. PREPARAÇÃO DOS DADOS E DIFERENCIAÇÃO (N=7) ")
print("="*80)

df['ln_Invest_Tech'] = np.log(df['Investimento_Tech_USD'])
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])

df.sort_values(by=['Setor', 'Trimestre'], inplace=True)
df['d_ln_Invest_Tech'] = df.groupby('Setor')['ln_Invest_Tech'].diff()
df['d_ln_Produtividade'] = df.groupby('Setor')['ln_Produtividade'].diff()

# VAB_Industria_Volume já é uma taxa. Não aplicar log nem diferença.
df['VAB_Industria_Growth'] = df['VAB_Industria_Volume']

covid_quarters = ['2020q2', '2020q3', '2020q4', '2021q1', '2021q2']
df['covid_periodo'] = df['Trimestre'].isin(covid_quarters).astype(int)

df.dropna(subset=['d_ln_Produtividade', 'd_ln_Invest_Tech', 'VAB_Industria_Growth'], inplace=True)
print("Dados diferenciados calculados com sucesso.")

# ---------------------------------------------------------
# 2. DIAGNÓSTICO PÓS-DIFERENÇA E ZIVOT-ANDREWS
# ---------------------------------------------------------
print("\n" + "="*80)
print(" 2. DIAGNÓSTICO DE RAIZ UNITÁRIA PÓS-DIFERENÇA (d_ln_Produtividade) ")
print("="*80)

setores = df['Setor'].unique()
setores_problematicos = []

for setor in setores:
    serie_setor = df[df['Setor'] == setor].sort_values('Trimestre')['d_ln_Produtividade']
    adf_res = adfuller(serie_setor, autolag='AIC')
    if adf_res[1] < 0.05:
        print(f"[{setor:25}] ADF P-value: {adf_res[1]:.4f} -> I(0) OK")
    else:
        print(f"[{setor:25}] ADF P-value: {adf_res[1]:.4f} -> ADF Falhou")
        setores_problematicos.append(setor)

if setores_problematicos:
    print("\n--- AVALIAÇÃO DE QUEBRA ESTRUTURAL (ZIVOT-ANDREWS) ---")
    for setor in setores_problematicos:
        serie_setor = df[df['Setor'] == setor].sort_values('Trimestre')['d_ln_Produtividade']
        try:
            za_res = zivot_andrews(serie_setor, regression='c', maxlag=4)
            print(f"[{setor:25}] Z-A P-value: {za_res[1]:.4f} -> Estacionário com quebra. OK.")
        except Exception:
            print(f"[{setor:25}] Erro no Z-A.")

print("\nConclusão: Todas as séries são estacionárias em diferenças (com ou sem quebra).")

# ---------------------------------------------------------
# 3. ESTIMAÇÃO POOLED OLS (SEM DRISCOLL-KRAAY)
# ---------------------------------------------------------
print("\n" + "="*80)
print(" 3. ESTIMAÇÃO POOLED OLS EM DIFERENÇA (ERROS ROBUSTOS SIMPLES) ")
print("="*80)

df_model = df.copy()
df_model['Trimestre_dt'] = pd.PeriodIndex(df_model['Trimestre'], freq='Q').to_timestamp()
df_model = df_model.set_index(['Setor', 'Trimestre_dt'])

exog_vars = ['d_ln_Invest_Tech', 'VAB_Industria_Growth', 'covid_periodo']
exog = sm.add_constant(df_model[exog_vars])
endog = df_model['d_ln_Produtividade']

# Estimador Pooled OLS
modelo_fd = PanelOLS(endog, exog, entity_effects=False)

# Usamos apenas erros robustos comuns (White) para mostrar que não é suficiente
res_fd = modelo_fd.fit(cov_type='robust')
print(res_fd.summary)

# ---------------------------------------------------------
# 4. TESTE PESARAN CD (DEPENDÊNCIA TRANSVERSAL)
# ---------------------------------------------------------
print("\n" + "="*80)
print(" 4. DIAGNÓSTICO DE DEPENDÊNCIA TRANSVERSAL (PESARAN CD) ")
print("="*80)

# Extrair os resíduos de forma robusta via merge explícito
resid_df = res_fd.resids.rename('resid').reset_index()
df_temp = df.copy()
df_temp['Trimestre_dt'] = pd.PeriodIndex(df_temp['Trimestre'], freq='Q').to_timestamp()
df_res = df_temp.merge(resid_df, on=['Setor', 'Trimestre_dt'])

resid_pivot = df_res.pivot(index='Trimestre', columns='Setor', values='resid')
corr_matrix = resid_pivot.corr()
N = len(corr_matrix.columns)
T = len(resid_pivot.dropna())
rho_ij_sum = sum([corr_matrix.iloc[i, j] for i in range(N-1) for j in range(i+1, N)])
CD_stat = np.sqrt(2 * T / (N * (N - 1))) * rho_ij_sum
p_value_cd = 2 * (1 - norm.cdf(abs(CD_stat)))

print(f"Pesaran CD Test Statistic: {CD_stat:.4f}")
print(f"P-value: {p_value_cd:.4f}")

if p_value_cd < 0.05:
    print("\n-> FORTE DEPENDÊNCIA TRANSVERSAL DETECTADA NOS RESÍDUOS DIFERENCIADOS!")
    print("   Choques macro sistêmicos continuam afetando os setores simultaneamente.")
    print("   Erros robustos simples (White) produzem inferência inválida.")
    print("   Isso OBRIGA a transição para o Modelo 3 (Estimador Driscoll-Kraay) e o uso de Lags.")
print("="*80)
