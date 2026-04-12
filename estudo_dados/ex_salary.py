# Importando bibliotecas
import pandas as pd
import openpyxl #necessário para ler os arquivos excel


# Criando o Df
df = pd.read_excel("salary.xlsx")
print(df)

# Quantas linhas e colunas tem o dataset
print(df.shape[0]) # linhas  | 14838
print(df.shape[1]) # Colunas  | 12

#  Calculando a media salarial
media_salarial = df["salary_in_usd"].mean()
print(f"A média salarial é de USD {media_salarial:.2f}")

# Maior salário
maior_salario = df["salary_in_usd"].max()
print(f"O maior saláriro é de USD {maior_salario}")

# Menor Salário
menor_salario = df["salary_in_usd"].min()
print(f"O menor salarío é de USD {menor_salario}")

# Criando um Df com apenas com as colunas job_title, salary, company_location, company_size, remote_ratio
df_novo = df[['job_title', 'salary_in_usd', 'company_location', 'company_size', 'remote_ratio']]
print(df_novo)

# Qual é o maior e menor salário de um “Data Scientist”? Onde fica essas empresas?
# Filtrando apenas para a profissão
df_ds = df_novo[df_novo['job_title'] == "Data Scientist"]
print(df_ds)

# Maior salário para DS
maior_salario_ds = df_ds['salary_in_usd'].max()
print(maior_salario_ds)

# Menor Salário para DS
menor_salario_ds = df_ds['salary_in_usd'].min()
print(menor_salario_ds)

# Loc da empresa que paga o maior salário
empresa_maior_salario_ds = df_ds.loc[df_ds['salary_in_usd'].idxmax(), 'company_location']
print(empresa_maior_salario_ds)

# Loc da empresa que paga o menor salário
empresa_menor_salario_ds = df_ds.loc[df_ds['salary_in_usd'].idxmin(), 'company_location']
print(empresa_menor_salario_ds)

# Calculando a profissão com a maior média salarial

media_salarial_profissao = df_novo.groupby('job_title')['salary_in_usd'].mean()
print(media_salarial_profissao.round(2))

# Profissões com a maior e menor média salarial, respectivamente

profissao_maior_media_salario = media_salarial_profissao.idxmax()
maior_media_salario = media_salarial_profissao.max()
print(f"A profissão com a maior média salarial é '{profissao_maior_media_salario}' com média de USD {maior_media_salario:.2f}")

profissao_menor_media_salario = media_salarial_profissao.idxmin()
menor_media_salario = media_salarial_profissao.min()
print(f"A profissão com a menor média salarial é '{profissao_menor_media_salario}' com média de USD {menor_media_salario.round(2)}")

# Profissões com remuneração acima da média
profissao_acima = media_salarial_profissao[media_salarial_profissao > media_salarial]
print(profissao_acima.index.to_list())

# Qual a localização com a maior média salarial
media_por_local = df_novo.groupby('company_location')['salary_in_usd'].mean()
loc_maior_media = media_por_local.idxmax()
print(f"O país com a maior média salarial é '{loc_maior_media}' com USD '{media_por_local.max().round()}'")

# Profissões que existem no Brasil
df_brasil = df_novo[df_novo['company_location'] == "BR"]
print(df_brasil['job_title'].unique().tolist())

# Qual a média salarial do Brasil
media_salarial_brasil = df_brasil['salary_in_usd'].mean()
print(f"A média salarial no Brasil é de USD {media_salarial_brasil.round(2)}")

# Quantas profissões existem no Brasil
num_profissoes_brasil = df_brasil['job_title'].nunique()
print(f"Há um total de {num_profissoes_brasil} profissioes no Brasil")

# Em média qual profissão tem um salário melhor?
media_salarial_profissao_br = df_brasil.groupby('job_title')['salary_in_usd'].mean()
maior_media_salario_br = media_salarial_profissao_br.max()
profissao_maior_media_salario_br = media_salarial_profissao_br.idxmax()
print(f"A profissão com a maior média salarial no Brasil é a de {profissao_maior_media_salario_br}, que conta com um salário média de USD {maior_media_salario_br}")

# Quantas profissões tem no EUA que trabalham em empresas grandes?

filtro_us = df_novo[(df_novo['company_location'] == "US") & (df_novo['company_size'] == "L")]
profissoes_eua_trabalham_em_grandes_empresas = filtro_us['job_title'].unique().tolist()
num_profissoes_eua_trabalham_em_grandes_empresas = len(profissoes_eua_trabalham_em_grandes_empresas)
print(f"Nos Estados Unidos há um total de {num_profissoes_eua_trabalham_em_grandes_empresas} de profissões que trabalham em grandes empresas")

# Qual a média salarial das empresas méida no Canada
filtro_ca = df_novo[(df_novo['company_location'] == "CA") & (df_novo['company_size'] == "M")]
media_salarial_ca = filtro_ca['salary_in_usd'].mean()
print(f"A média salarial das empresas canadenses de médio porte é: USD {media_salarial_ca.round(2)}")

# Qual o país com o maior número de profissões?
profissoes_por_pais = df_novo.groupby('company_location')['job_title'].nunique()
pais_mais_profissoes = profissoes_por_pais.idxmax()
print(f" O país com o maior número de profissões é o {pais_mais_profissoes} com {profissoes_por_pais.max()} profissões a todo")

# Qual o país com o menor número de profissões?
pais_menos_profissoes = profissoes_por_pais.idxmin()
print(f" O país com o menor número de profissões é o {pais_menos_profissoes} com {profissoes_por_pais.min()} profissão a todo")

# Em média, qual das modalidades de trabalho tem o salario maior?

media_remoto = df_novo[df_novo['remote_ratio'] == 100]['salary_in_usd'].mean()
media_hibrido = df_novo[df_novo['remote_ratio'] == 50]['salary_in_usd'].mean()
media_presencial = df_novo[df_novo['remote_ratio'] == 0]['salary_in_usd'].mean()

print(f"A média salarial do trabalho remoto é de USD {media_remoto.round(2)}")
print(f"A média salarial do trabalho hibrido é de USD {media_hibrido.round(2)}")
print(f"A média salarial do trabalho presencial é de USD {media_presencial.round(2)}")

# Qual o páis com maior numero de profissoes trabalhando 100% remoto?
df_remoto = df_novo[df_novo['remote_ratio'] == 100]
profissionais_remotos_por_pais = df_remoto.groupby('company_location')['job_title'].nunique()
pais_com_mais_trabalhadores_remotos = profissionais_remotos_por_pais.idxmax()
print(f"O país com maior número de trablhadores remotos é o {pais_com_mais_trabalhadores_remotos}, com {profissionais_remotos_por_pais.max()} trabalhadores remotos")





