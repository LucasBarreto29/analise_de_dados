# Responda as perguntas utilizando comandos em python e utilizando o dataset 'salary.xlsx' que está na pasta 'analise_de_dados'.
# Para isso, utilize a biblioteca pandas para ler o arquivo e realizar as análises necessárias.
import pandas as pd


# Quantas linhas e quantas colunas tem o dataset?
df = pd.read_excel("analise_de_dados/salary.xlsx")
print(df.shape) # O dataset tem 14.838 linhas e 12 colunas.

# Qual a média salarial? Qual é o maior salário? O menor salário?
print(f"Média salarial: R$ {df['salary'].mean():.2f}")
print(f"Maior salário: R$ {df['salary'].max():.2f}")
print(f"Menor salário: R$ {df['salary'].min():.2f}")

# Crie um df com apenas as colunas job_title, salary, company_location, company_size, remote_ratio
df_colunas = df[["job_title", "salary", "company_location", "company_size", "remote_ratio"]]
print(df_colunas.head())

# Qual é o maior e menor salário de um “Data Scientist”? Onde fica essas empresas?
data_scientist = df[df["job_title"] == "Data Scientist"]
print(f"Maior salário de Data Scientist: R$ {data_scientist['salary'].max():.2f}") # R$ 30.400.000,00
print(f"Menor salário de Data Scientist: R$ {data_scientist['salary'].min():.2f}") # R$ 16.000,00
#localização das empresas
print(data_scientist["company_location"].unique())

# Qual a profissão com a maior média salarial? E a menor?
profissao_media_salarial = df.groupby("job_title")["salary"].mean()
print(f"Profissão com a maior média salarial: {profissao_media_salarial.idxmax()} (R$ {profissao_media_salarial.max():.2f})")
print(f"Profissão com a menor média salarial: {profissao_media_salarial.idxmin()} (R$ {profissao_media_salarial.min():.2f})")

# Quais as profissões com a média salarial maior que a média geral?
media_geral = df["salary"].mean()
profissoes_acima_media = profissao_media_salarial[profissao_media_salarial > media_geral]
print("Profissões com média salarial maior que a média geral:")
print(profissoes_acima_media)


# Qual a localização com maior média salarial?
localizacao_media_salarial = df.groupby("company_location")["salary"].mean()
print(f"Localização com maior média salarial: {localizacao_media_salarial.idxmax()} (R$ {localizacao_media_salarial.max():.2f})")   


# Quais as profissões que existem no Brasil (BR)?
profissoes_brasil = df[df["company_location"] == "BR"]["job_title"].unique()
print("Profissões que existem no Brasil (BR):")
print(profissoes_brasil)


# Qual a média salarial no Brasil?
media_brasil = df[df["company_location"] == "BR"]["salary"].mean()
print(f"Média salarial no Brasil: R$ {media_brasil:.2f}")

# Quantas profissões existem no Brasil?
num_profissoes_brasil = len(profissoes_brasil)
print(f"Quantidade de profissões no Brasil: {num_profissoes_brasil}")

# Qual a profissão que mais ganha no Brasil?
profissao_mais_ganha_brasil = df[df["company_location"] == "BR"].groupby("job_title")["salary"].mean().idxmax()
print(f"Profissão que mais ganha no Brasil: {profissao_mais_ganha_brasil}")

# Quantas profissões tem nos US e que trabalham em empresas grandes (L)?
profissoes_us_large = df[(df["company_location"] == "US") & (df["company_size"] == "L")]["job_title"].unique()
print(f"Quantidade de profissões nos US em empresas grandes (L): {len(profissoes_us_large)}")

# Qual é a média salarial das empresas médias (M) na Canada (CA)?
media_salarial_ca_medium = df[(df["company_location"] == "CA") & (df["company_size"] == "M")]["salary"].mean()
print(f"Média salarial das empresas médias (M) no Canadá (CA): R$ {media_salarial_ca_medium:.2f}")  

# Qual é o país com mais profissões? E qual é o mais com menos?
paises_profissoes = df.groupby("company_location")["job_title"].nunique()
print(f"País com mais profissões: {paises_profissoes.idxmax()} ({paises_profissoes.max()} profissões)")
print(f"País com menos profissões: {paises_profissoes.idxmin()} ({paises_profissoes.min()} profissões)")

# Quem ganha mais que trabalha remoto, presencial ou híbrido?
media_remoto = df[df["remote_ratio"] == 100]["salary"].mean()
media_presencial = df[df["remote_ratio"] == 0]["salary"].mean()
media_hibrido = df[(df["remote_ratio"] > 0) & (df["remote_ratio"] < 100)]["salary"].mean()
print(f"Média salarial para trabalho remoto: R$ {media_remoto:.2f}")
print(f"Média salarial para trabalho presencial: R$ {media_presencial:.2f}")
print(f"Média salarial para trabalho híbrido: R$ {media_hibrido:.2f}")

# Qual o país com maior numero de profissões trabalhando 100% remoto?
profissoes_remoto = df[df["remote_ratio"] == 100].groupby("company_location")["job_title"].nunique()
print(f"País com maior número de profissões trabalhando 100% remoto: {profissoes_remoto.idxmax()} ({profissoes_remoto.max()} profissões)")  