import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

print("=== INICIANDO ETAPA 4: MODELO DEFINITIVO COM 2 LAGS E DRISCOLL-KRAAY ===")

# 1. Carregamento e Transformação Básica
df = pd.read_csv('/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/painel_bartik.csv')
df = df.dropna(subset=['Bartik_Tech_it']).copy()
df['Period'] = pd.PeriodIndex(df['Trimestre'].str.replace('q', 'Q', case=False), freq='Q').to_timestamp()
df = df.set_index(['Setor', 'Period'])

df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])
df['ln_Bartik_Tech'] = np.log(df['Bartik_Tech_it'])

df['d_ln_Produtividade'] = df.groupby(level='Setor')['ln_Produtividade'].diff()
df['d_ln_Bartik_Tech'] = df.groupby(level='Setor')['ln_Bartik_Tech'].diff()

# 2. Criação dos 2 Lags
df['d_ln_Bartik_Tech_lag1'] = df.groupby(level='Setor')['d_ln_Bartik_Tech'].shift(1)
df['d_ln_Bartik_Tech_lag2'] = df.groupby(level='Setor')['d_ln_Bartik_Tech'].shift(2)

# Amostra rigorosamente balanceada (drop dos primeiros 2 trimestres de cada setor)
colunas_necessarias = [
    'd_ln_Produtividade', 'd_ln_Bartik_Tech', 
    'd_ln_Bartik_Tech_lag1', 'd_ln_Bartik_Tech_lag2',
    'VAB_Industria_Volume', 'Stringency_Index'
]
df_final = df.dropna(subset=colunas_necessarias).copy()
df_final['const'] = 1

# 3. Estimação do Modelo Definitivo
exog_vars = ['const', 'd_ln_Bartik_Tech', 'd_ln_Bartik_Tech_lag1', 'd_ln_Bartik_Tech_lag2', 'VAB_Industria_Volume', 'Stringency_Index']
mod_final = PanelOLS(df_final['d_ln_Produtividade'], df_final[exog_vars], entity_effects=False)

# Aplicação do Driscoll-Kraay (cov_type='kernel')
res_final = mod_final.fit(cov_type='kernel')

print("\n================================================================================")
print("             RESULTADO DO MODELO DEFINITIVO - DRISCOLL-KRAAY / 2 LAGS           ")
print("================================================================================")
print(res_final.summary)

# 4. Teste de Wald (Efeito Líquido Acumulado)
# Queremos testar se d_ln_Bartik_Tech + d_ln_Bartik_Tech_lag1 + d_ln_Bartik_Tech_lag2 = 0
wald = res_final.wald_test(formula="d_ln_Bartik_Tech + d_ln_Bartik_Tech_lag1 + d_ln_Bartik_Tech_lag2 = 0")

print("\n================================================================================")
print("                   TESTE DE WALD (EFEITO ACUMULADO DA TECNOLOGIA)               ")
print("================================================================================")
print("Hipótese Nula (H0): O efeito acumulado da adoção tecnológica nos 3 trimestres é zero.")
print(f"Estatística F: {wald.stat:.4f}")
print(f"p-valor:       {wald.pval:.4f}")

if wald.pval < 0.05:
    print("\nConclusão: Rejeitamos H0. O choque tecnológico TEM UM IMPACTO ACUMULADO SIGNIFICATIVO na produtividade.")
else:
    print("\nConclusão: Não rejeitamos H0. O impacto acumulado do choque tecnológico é ESTATISTICAMENTE NULO.")
    print("O efeito negativo imediato pode ser compensado ou dissipado nos trimestres subsequentes.")
