import pandas as pd
import numpy as np
import requests
import warnings
warnings.filterwarnings('ignore')

print("=== INICIANDO CRIAÇÃO DO PAINEL DE CAPITAL HUMANO ===")

# Passo 1: Carga dos Dados Base e de Mão de Obra
print("1. Carregando dados base e de TI...")
df_base = pd.read_csv('/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/painel_bartik.csv')
# Fica apenas com colunas essenciais da base para o merge
df_base = df_base[['Setor', 'Trimestre', 'Produtividade_Hora_Habitual']].drop_duplicates()

df_ti = pd.read_csv('/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/estoque_ti_setores.csv')

df_merged = pd.merge(df_base, df_ti, on=['Setor', 'Trimestre'], how='inner')


# Passo 2: Integração do Índice FGV
print("2. Carregando Índice de Capital Humano FGV...")
fgv_path = '/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/indice_de_capital_humano-ich_4t2025_1 - cópia.xlsx'
# Pulamos as primeiras 7 linhas para pegar o header correto (na linha 7 original, que é index 7 no skip)
df_fgv = pd.read_excel(fgv_path, sheet_name='ICH', skiprows=7)
df_fgv = df_fgv.rename(columns={df_fgv.columns[0]: 'Trimestre', df_fgv.columns[2]: 'Capital_Humano_FGV'})
df_fgv = df_fgv[['Trimestre', 'Capital_Humano_FGV']].dropna()

# Padronizar 'Trimestre' para lower case (ex: 2012q1)
df_fgv['Trimestre'] = df_fgv['Trimestre'].astype(str).str.lower().str.strip()

df_merged = pd.merge(df_merged, df_fgv, on='Trimestre', how='inner')

# Passo 3: Extração e Integração da Selic Anualizada
print("3. Buscando a Taxa Selic Anualizada (SGS 4189)...")
url_selic = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4189/dados?formato=json'
response = requests.get(url_selic)
if response.status_code == 200:
    df_selic = pd.DataFrame(response.json())
    df_selic['data'] = pd.to_datetime(df_selic['data'], format='%d/%m/%Y')
    df_selic['valor'] = df_selic['valor'].astype(float)
    
    # Agregar para Trimestre (média)
    df_selic['Trimestre'] = df_selic['data'].dt.year.astype(str) + 'q' + df_selic['data'].dt.quarter.astype(str)
    selic_trimestral = df_selic.groupby('Trimestre')['valor'].mean().reset_index()
    selic_trimestral.rename(columns={'valor': 'Selic'}, inplace=True)
else:
    raise Exception(f"Erro ao buscar Selic: {response.status_code}")

df_merged = pd.merge(df_merged, selic_trimestral, on='Trimestre', how='inner')

# Passo 4: Exportação
print("4. Selecionando colunas e exportando...")
cols = ['Setor', 'Trimestre', 'Produtividade_Hora_Habitual', 'Estoque_TI_Setor', 'Capital_Humano_FGV', 'Selic']
df_final = df_merged[cols]

output_path = '/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/painel_capital_humano_completo.csv'
df_final.to_csv(output_path, index=False)

print("\n--- AMOSTRA DO NOVO PAINEL ---")
print(df_final.head())

print("\n--- INFORMAÇÕES DO DATASET ---")
print(df_final.info())
print("\nConcluído com sucesso!")
