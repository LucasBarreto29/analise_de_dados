import sidrapy
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_DIR = os.path.join(BASE_DIR, "dados")

print("Baixando VAB da Indústria (Tabela 5932, Setor 90691) do IBGE SIDRA...")

# Extração da Indústria - total (90691)
df_raw = sidrapy.get_table(
    table_code="5932",
    territorial_level="1",
    ibge_territorial_code="all",
    variable="6564",
    period="all",
    classifications={"11255": "90691"}
)

df_raw.columns = df_raw.iloc[0]
df = df_raw.iloc[1:].reset_index(drop=True)

# Padronizando colunas
for col in df.columns:
    if 'Trimestre (Código)' in col or 'Trimestre (código)' in col:
        df.rename(columns={col: 'Trimestre_Cod'}, inplace=True)
    elif 'Valor' == col:
        df.rename(columns={col: 'VAB_Industria_Volume'}, inplace=True)

df_clean = df[['Trimestre_Cod', 'VAB_Industria_Volume']].copy()
df_clean = df_clean[df_clean['Trimestre_Cod'] >= '201201']
df_clean['VAB_Industria_Volume'] = pd.to_numeric(df_clean['VAB_Industria_Volume'], errors='coerce')

# Convertendo 201201 para 2012q1
def parse_trimestre(cod):
    ano = cod[:4]
    tri = cod[-1]
    return f"{ano}q{tri}"

df_clean['Trimestre'] = df_clean['Trimestre_Cod'].apply(parse_trimestre)
df_clean.drop(columns=['Trimestre_Cod'], inplace=True)

# Salvar o arquivo isolado por segurança
caminho_ind = os.path.join(DADOS_DIR, "vab_industria_ibge.csv")
df_clean.to_csv(caminho_ind, index=False)
print(f"VAB da Indústria salvo em: {caminho_ind}")

# Fazer o merge no painel mestre
caminho_painel = os.path.join(DADOS_DIR, "painel_mestre.csv")
df_painel = pd.read_csv(caminho_painel)

# Caso a coluna já exista de alguma tentativa anterior, vamos removê-la para não duplicar
if 'VAB_Industria_Volume' in df_painel.columns:
    df_painel.drop(columns=['VAB_Industria_Volume'], inplace=True)

# Merge
df_painel = df_painel.merge(df_clean, on='Trimestre', how='left')

# Sobrescrever o painel mestre
df_painel.to_csv(caminho_painel, index=False)
print("Painel mestre atualizado com sucesso com o VAB_Industria_Volume.")
