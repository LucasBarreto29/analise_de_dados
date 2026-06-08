import pandas as pd
import os

# Caminhos base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_DIR = os.path.join(BASE_DIR, "dados")

ARQUIVO_PAINEL = os.path.join(DADOS_DIR, "painel_mestre.csv")
ARQUIVO_STRINGENCY = os.path.join(DADOS_DIR, "Stringency_index.csv")
ARQUIVO_SAIDA = os.path.join(DADOS_DIR, "painel_mestre_v2.csv")

print("="*60)
print(" PREPARANDO PAINEL MESTRE V2 (INCLUINDO STRINGENCY INDEX) ")
print("="*60)

# 1. Carregar Painel Mestre
print("Lendo painel mestre original...")
df_painel = pd.read_csv(ARQUIVO_PAINEL)

# 2. Carregar e Processar Stringency Index
print("Lendo Stringency Index (isso pode demorar alguns segundos, arquivo grande)...")
# Como o arquivo é grande e só precisamos do Brasil, podemos otimizar a leitura
chunks = pd.read_csv(ARQUIVO_STRINGENCY, chunksize=50000, low_memory=False, sep=';')
df_bra_list = []
for chunk in chunks:
    bra_chunk = chunk[chunk['CountryCode'] == 'BRA']
    if not bra_chunk.empty:
        df_bra_list.append(bra_chunk)

df_stringency = pd.concat(df_bra_list, ignore_index=True)

# 3. Tratamento de Datas e Agregação Trimestral
print("Processando datas e agregando por trimestre...")
# O formato de data padrão do OxCGRT é YYYYMMDD numérico
df_stringency['Date'] = pd.to_datetime(df_stringency['Date'], format='%Y%m%d')
df_stringency['Trimestre_pd'] = df_stringency['Date'].dt.to_period('Q')

# Converter o formato do trimestre para o mesmo do painel (ex: 2020q1)
df_stringency['Trimestre'] = df_stringency['Trimestre_pd'].dt.year.astype(str) + "q" + df_stringency['Trimestre_pd'].dt.quarter.astype(str)

# Agregação pela média trimestral do Stringency Index
# Usamos a coluna StringencyIndex_Average
stringency_trimestral = df_stringency.groupby('Trimestre')['StringencyIndex_Average'].mean().reset_index()
stringency_trimestral.rename(columns={'StringencyIndex_Average': 'Stringency_Index'}, inplace=True)

# 4. Merge das Bases
print("Realizando merge com o painel mestre...")
df_final = pd.merge(df_painel, stringency_trimestral, on='Trimestre', how='left')

# Preencher NAs com 0 (períodos antes do Covid não tinham restrições)
df_final['Stringency_Index'] = df_final['Stringency_Index'].fillna(0)

# Opcional: Para limpeza, podemos remover a dummy antiga de Covid ou mantê-la apenas para histórico
# Vamos manter para não quebrar compatibilidade retroativa caso algo acesse as colunas antigas, 
# mas não usaremos ela nos novos modelos.

# 5. Salvar Novo Dataset
df_final.to_csv(ARQUIVO_SAIDA, index=False)
print(f"Novo painel mestre salvo com sucesso em: {ARQUIVO_SAIDA}")
print(f"Total de linhas: {len(df_final)}")
print("="*60)
