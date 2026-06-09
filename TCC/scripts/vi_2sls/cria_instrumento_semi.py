import pandas as pd
import numpy as np
import os

# Caminhos Base
BASE_DIR = "/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC"
DADOS_DIR = os.path.join(BASE_DIR, "dados")
FRED_FILE = os.path.join(DADOS_DIR, "ppi_semi.csv")
PAINEL_BARTIK = os.path.join(DADOS_DIR, "painel_bartik_fixo_diff.csv")
OUT_FILE = os.path.join(DADOS_DIR, "painel_2sls_investimento.csv")

print("="*60)
print(" CRIANDO PAINEL DE VARIÁVEIS INSTRUMENTAIS (2SLS) ")
print("="*60)

# 1. Carga e Agregação do FRED
print("1. Processando arquivo bruto do FRED (Semicondutores)...")
df_fred = pd.read_csv(FRED_FILE)
df_fred.rename(columns={'PCU33443344': 'PPI_Semi_Bruto'}, inplace=True)

# Converter data para formato Trimestral
df_fred['observation_date'] = pd.to_datetime(df_fred['observation_date'])
df_fred['Trimestre'] = df_fred['observation_date'].dt.year.astype(str) + 'q' + df_fred['observation_date'].dt.quarter.astype(str)

# Agregação Trimestral (Média Mensal)
df_semi_trim = df_fred.groupby('Trimestre')['PPI_Semi_Bruto'].mean().reset_index()

# 2. Transformação do Choque Global
print("2. Calculando o Choque de Preços (Primeira Diferença do Log)...")
# Garantir ordenação temporal baseada no Trimestre
df_semi_trim['Period'] = pd.PeriodIndex(df_semi_trim['Trimestre'].str.replace('q', 'Q', case=False), freq='Q').to_timestamp()
df_semi_trim = df_semi_trim.sort_values('Period')

# Log e Diff
df_semi_trim['ln_PPI_Semi'] = np.log(df_semi_trim['PPI_Semi_Bruto'])
df_semi_trim['d_ln_PPI_Semi'] = df_semi_trim['ln_PPI_Semi'].diff()

# Filtrar apenas as colunas úteis para o merge
df_instrumento = df_semi_trim[['Trimestre', 'd_ln_PPI_Semi']].dropna()

# 3. Integração Segura com o Painel Existente
print("3. Carregando Painel Base (Bartik Fixo Diff)...")
df_painel = pd.read_csv(PAINEL_BARTIK)

print("4. Realizando Merge Temporal...")
df_final = pd.merge(df_painel, df_instrumento, on='Trimestre', how='left')

# Drop NA para garantir matriz de estimação limpa
print("5. Removendo NAs resultantes do pareamento...")
df_final = df_final.dropna(subset=['d_ln_PPI_Semi', 'd_ln_Produtividade', 'Impacto_tech_setor', 'd_ln_Cambio', 'VAB_Industria_Volume'])

# 6. Salvar
df_final.to_csv(OUT_FILE, index=False)

print("\n--- AMOSTRA DO NOVO PAINEL (2SLS) ---")
print(df_final[['Setor', 'Trimestre', 'Impacto_tech_setor', 'd_ln_PPI_Semi']].head())
print(f"\nTotal de Observações Válidas: {len(df_final)}")
print(f"Salvo com sucesso em: {OUT_FILE}")
