import pandas as pd
import numpy as np
import requests
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

print("=== INICIANDO ETAPA 6: TESTE DA CURVA EM J (4 LAGS E CÂMBIO) ===")

# 1. Extração do Câmbio (BCB SGS - 3698: Dólar comercial média mensal)
print("1. Buscando dados do Banco Central (SGS 3698)...")
url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.3698/dados?formato=json'
response = requests.get(url)
if response.status_code == 200:
    df_cambio = pd.DataFrame(response.json())
    df_cambio['data'] = pd.to_datetime(df_cambio['data'], format='%d/%m/%Y')
    df_cambio['valor'] = df_cambio['valor'].astype(float)
    
    # Agregar para Trimestre
    df_cambio['Trimestre'] = df_cambio['data'].dt.year.astype(str) + 'q' + df_cambio['data'].dt.quarter.astype(str)
    cambio_trimestral = df_cambio.groupby('Trimestre')['valor'].mean().reset_index()
    cambio_trimestral.rename(columns={'valor': 'Cambio_BRL_USD'}, inplace=True)
else:
    raise Exception(f"Erro ao buscar dados do BCB: {response.status_code}")

# 2. Carregamento e Transformação Básica do Painel
print("2. Carregando e mesclando o painel...")
df = pd.read_csv('/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/painel_bartik.csv')
df = df.dropna(subset=['Bartik_Tech_it']).copy()

# Merge do câmbio
df = pd.merge(df, cambio_trimestral, on='Trimestre', how='left')

# Configurar index
df['Period'] = pd.PeriodIndex(df['Trimestre'].str.replace('q', 'Q', case=False), freq='Q').to_timestamp()
df = df.set_index(['Setor', 'Period'])

# Transformações em Log
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])
df['ln_Bartik_Tech'] = np.log(df['Bartik_Tech_it'])
df['ln_Cambio'] = np.log(df['Cambio_BRL_USD'])

# Diferenciação
df['d_ln_Produtividade'] = df.groupby(level='Setor')['ln_Produtividade'].diff()
df['d_ln_Bartik_Tech'] = df.groupby(level='Setor')['ln_Bartik_Tech'].diff()
df['d_ln_Cambio'] = df.groupby(level='Setor')['ln_Cambio'].diff()

# Criação de 4 Lags para a Curva em J
df['d_ln_Bartik_Tech_lag1'] = df.groupby(level='Setor')['d_ln_Bartik_Tech'].shift(1)
df['d_ln_Bartik_Tech_lag2'] = df.groupby(level='Setor')['d_ln_Bartik_Tech'].shift(2)
df['d_ln_Bartik_Tech_lag3'] = df.groupby(level='Setor')['d_ln_Bartik_Tech'].shift(3)
df['d_ln_Bartik_Tech_lag4'] = df.groupby(level='Setor')['d_ln_Bartik_Tech'].shift(4)

# Dropna final para 4 lags
colunas_necessarias = [
    'd_ln_Produtividade', 'd_ln_Bartik_Tech', 
    'd_ln_Bartik_Tech_lag1', 'd_ln_Bartik_Tech_lag2', 
    'd_ln_Bartik_Tech_lag3', 'd_ln_Bartik_Tech_lag4',
    'VAB_Industria_Volume', 'd_ln_Cambio'
]
df_final = df.dropna(subset=colunas_necessarias).copy()
df_final['const'] = 1

# 3. Estimação do Modelo Dinâmico
print("3. Estimando o Modelo Dinâmico (4 Lags + Driscoll-Kraay)...")
exog_vars = [
    'const', 'd_ln_Bartik_Tech', 
    'd_ln_Bartik_Tech_lag1', 'd_ln_Bartik_Tech_lag2', 
    'd_ln_Bartik_Tech_lag3', 'd_ln_Bartik_Tech_lag4',
    'VAB_Industria_Volume', 'd_ln_Cambio'
]
mod_final = PanelOLS(df_final['d_ln_Produtividade'], df_final[exog_vars], entity_effects=False)

res_final = mod_final.fit(cov_type='kernel')

print("\n================================================================================")
print("     RESULTADO FINAL: TESTE DA CURVA EM J (1 ANO / 4 LAGS / DRISCOLL-KRAAY)     ")
print("================================================================================")
print(res_final.summary)

# 4. Teste de Wald
wald = res_final.wald_test(formula="d_ln_Bartik_Tech + d_ln_Bartik_Tech_lag1 + d_ln_Bartik_Tech_lag2 + d_ln_Bartik_Tech_lag3 + d_ln_Bartik_Tech_lag4 = 0")

print("\n================================================================================")
print("               TESTE DE WALD (EFEITO ANUAL ACUMULADO DA TECNOLOGIA)             ")
print("================================================================================")
print("Hipótese Nula (H0): O efeito acumulado após 1 ano (Choque Contemporâneo + 4 Lags) é zero.")
print(f"Estatística F: {wald.stat:.4f}")
print(f"p-valor:       {wald.pval:.4f}")

if wald.pval < 0.05:
    print("\nConclusão: Rejeitamos H0. O choque tem IMPACTO ACUMULADO SIGNIFICATIVO na produtividade.")
else:
    print("\nConclusão: Não rejeitamos H0. O impacto acumulado do choque tecnológico é ESTATISTICAMENTE NULO após 1 ano de maturação.")
