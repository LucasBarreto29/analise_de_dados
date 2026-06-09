import pandas as pd
import numpy as np
import os
import requests

# Caminhos base
BASE_DIR = "/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC"
DADOS_DIR = os.path.join(BASE_DIR, "dados")
PAINEL_MESTRE = os.path.join(DADOS_DIR, "painel_mestre.csv")
EMPREGO = os.path.join(DADOS_DIR, "emprego_setores.csv")
ARQUIVO_SAIDA = os.path.join(DADOS_DIR, "painel_bartik_fixo_diff.csv")

print("="*60)
print(" CRIANDO PAINEL BARTIK COM SHARE FIXO (2012q1) E DIFERENÇAS ")
print("="*60)

# 1. Obter Taxa de Câmbio (BCB SGS 3698)
print("1. Extraindo Taxa de Câmbio do BCB (SGS 3698)...")
url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.3698/dados?formato=json&dataInicial=01/01/2012&dataFinal=31/12/2024"
response = requests.get(url)
cambio = pd.DataFrame(response.json())
cambio['data'] = pd.to_datetime(cambio['data'], format='%d/%m/%Y')
cambio['valor'] = pd.to_numeric(cambio['valor'])
cambio['Trimestre'] = cambio['data'].dt.year.astype(str) + 'q' + cambio['data'].dt.quarter.astype(str)
cambio_trimestral = cambio.groupby('Trimestre')['valor'].mean().reset_index()
cambio_trimestral.rename(columns={'valor': 'Cambio_BRL_USD'}, inplace=True)

# 2. Ler Bases de Dados
print("2. Lendo Bases de Dados Originais...")
df_mestre = pd.read_csv(PAINEL_MESTRE)
df_emprego = pd.read_csv(EMPREGO)

# Merge do Câmbio no Painel Mestre
df_mestre = pd.merge(df_mestre, cambio_trimestral, on='Trimestre', how='left')

# 3. Criar Share Fixo (Base = 2012q1)
print("3. Calculando e Fixando o Share de TI em 2012q1...")
df_emprego['Share_temp'] = df_emprego['Estoque'] / df_emprego['Estoque_Nacional']
# Filtrar apenas 2012q1
share_2012q1 = df_emprego[df_emprego['Trimestre'] == '2012q1'][['Setor', 'Share_temp']].copy()
share_2012q1.rename(columns={'Share_temp': 'Share_2012q1'}, inplace=True)

# Merge do Share Fixo em todos os trimestres
df_painel = pd.merge(df_mestre, share_2012q1, on='Setor', how='left')

# Garantir a ordenação temporal correta antes de diferenciar
df_painel['Period'] = pd.PeriodIndex(df_painel['Trimestre'].str.replace('q', 'Q', case=False), freq='Q').to_timestamp()
df_painel = df_painel.sort_values(by=['Setor', 'Period'])

# 4. Transformações Logarítmicas
print("4. Aplicando Logaritmos...")
df_painel['ln_Produtividade'] = np.log(df_painel['Produtividade_Hora_Habitual'])
df_painel['ln_Tech_Nacional'] = np.log(df_painel['Investimento_Tech_USD'])
df_painel['ln_Cambio'] = np.log(df_painel['Cambio_BRL_USD'])

# 5. Primeiras Diferenças
print("5. Calculando Primeiras Diferenças (Crescimento Percentual)...")
df_painel['d_ln_Produtividade'] = df_painel.groupby('Setor')['ln_Produtividade'].diff()
df_painel['d_ln_Tech_Nacional'] = df_painel.groupby('Setor')['ln_Tech_Nacional'].diff()
df_painel['d_ln_Cambio'] = df_painel.groupby('Setor')['ln_Cambio'].diff()

# 6. Criação do Bartik Fixo Verdadeiro
print("6. Construindo o Instrumento Bartik ('Impacto_tech_setor')...")
# Formula teórica: Share Constante * Variação do Shift
df_painel['Impacto_tech_setor'] = df_painel['Share_2012q1'] * df_painel['d_ln_Tech_Nacional']

# 7. Seleção de Colunas e Limpeza
print("7. Limpeza e Exportação...")
cols_finais = [
    'Setor', 'Trimestre', 'Period',
    'd_ln_Produtividade', 'Impacto_tech_setor', 
    'd_ln_Cambio', 'VAB_Industria_Volume', 'Share_2012q1'
]

df_final = df_painel[cols_finais].copy()
df_final = df_final.dropna(subset=['d_ln_Produtividade', 'Impacto_tech_setor', 'd_ln_Cambio', 'VAB_Industria_Volume'])

# Salvar
df_final.to_csv(ARQUIVO_SAIDA, index=False)

print(f"\n--- AMOSTRA DO PAINEL FINAL (PRIMEIRAS DIFERENÇAS) ---")
print(df_final.head())
print(f"\nTotal de Observações Válidas: {len(df_final)}")
print(f"Salvo com sucesso em: {ARQUIVO_SAIDA}")
