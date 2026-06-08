import pandas as pd
import os

# Configurar caminhos relativos ao diretório TCC
base_dir = "/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC"
dados_dir = os.path.join(base_dir, "dados")

# 1. Leitura das Bases
print("Lendo bases de dados...")
painel_mestre = pd.read_csv(os.path.join(dados_dir, "painel_mestre.csv"))
emprego = pd.read_csv(os.path.join(dados_dir, "emprego_setores.csv"))

# 2. Construção do Share Dinâmico
print("Calculando Share_it...")
# emprego já tem as colunas: Trimestre, Setor, Estoque, Estoque_Nacional
emprego['Share_it'] = emprego['Estoque'] / emprego['Estoque_Nacional']

# Verificar se a soma dos shares <= 1 para cada trimestre
soma_shares = emprego.groupby('Trimestre')['Share_it'].sum()
if (soma_shares > 1.01).any():
    print("Aviso: Soma dos shares > 1 encontrado em alguns trimestres. Verifique o Estoque_Nacional.")

# Merge com o painel principal
print("Fazendo merge com o painel mestre...")
painel = pd.merge(painel_mestre, emprego[['Trimestre', 'Setor', 'Share_it']], on=['Trimestre', 'Setor'], how='left')

# Verificar NaNs no Share
if painel['Share_it'].isnull().any():
    print(f"Atenção: {painel['Share_it'].isnull().sum()} observações com Share_it nulo.")

# 3. Variável de Bartik
print("Calculando Bartik_Tech_it...")
painel['Bartik_Tech_it'] = painel['Investimento_Tech_USD'] * painel['Share_it']

# 4. Integração do Stringency Index
print("Processando Stringency Index...")
oxford_path = os.path.join(dados_dir, "Stringency_index.csv")

# O arquivo pode ser grande e separado por ponto-e-vírgula. Puxamos apenas as colunas necessárias para economizar memória.
cols_to_use = ['CountryCode', 'Date', 'StringencyIndex_Average']
df_ox = pd.read_csv(oxford_path, sep=';', usecols=cols_to_use, low_memory=False)

# Filtrar Brasil
df_ox_br = df_ox[df_ox['CountryCode'] == 'BRA'].copy()
df_ox_br['StringencyIndex_Average'] = pd.to_numeric(df_ox_br['StringencyIndex_Average'].str.replace(',', '.') if df_ox_br['StringencyIndex_Average'].dtype == 'object' else df_ox_br['StringencyIndex_Average'])

# Converter datas para trimestres (ex: 2020q1)
df_ox_br['Date'] = pd.to_datetime(df_ox_br['Date'].astype(str), format='%Y%m%d')
df_ox_br['Trimestre'] = df_ox_br['Date'].dt.year.astype(str) + 'q' + df_ox_br['Date'].dt.quarter.astype(str)

# Média trimestral
stringency = df_ox_br.groupby('Trimestre')['StringencyIndex_Average'].mean().reset_index()

# Merge no painel
painel = pd.merge(painel, stringency, on='Trimestre', how='left')

# Preencher NAs fora do período pandêmico com 0.0
painel['StringencyIndex_Average'] = painel['StringencyIndex_Average'].fillna(0.0)

# Renomear para padronizar
painel.rename(columns={'StringencyIndex_Average': 'Stringency_Index'}, inplace=True)

# 5. Exportação e Verificações Finais
out_path = os.path.join(dados_dir, "painel_bartik.csv")
painel.to_csv(out_path, index=False)

print("\n=== Verificações Finais ===")
print(painel[['Trimestre', 'Setor', 'Share_it', 'Bartik_Tech_it', 'Stringency_Index']].head())
print("\nValores Nulos na Variável Bartik:")
print(painel['Bartik_Tech_it'].isnull().sum())
print("\nMédias do Stringency Index (exemplo pandêmico vs normal):")
print(painel.groupby('Trimestre')['Stringency_Index'].mean().head(2))
print(painel.groupby('Trimestre')['Stringency_Index'].mean().tail(2))
print(f"\nArquivo salvo com sucesso em: {out_path}")
