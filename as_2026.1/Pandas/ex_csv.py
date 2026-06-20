# LISTA DE EXERCÍCIOS – ANÁLISE DE DADOS COM PANDAS Dataset: Ranking
# Mundial de Universidades (notas.csv)

# ============================================================
# EXPLORAÇÃO INICIAL (EDA BÁSICA)
# ============================================================

# Exercício 1 – Conhecendo o Dataset 
# 1. Quantas linhas e colunas existem?
# 2. Quais são os tipos de dados? 
# 3. Existe coluna com valores ausentes?
# 4. Qual é o período de anos disponível? 
# 5. Quantos países diferentes
# existem?

# Exercício 2 – Estatísticas Gerais 
# 1. Média do score 
# 2. Maior score 
# 3.Menor score 
# 4. Média do score por ano 
# 5. Desvio padrão do score

# ============================================================
# FILTROS E SELEÇÕES
# ============================================================

# Exercício 3 – Top Universidades 
# 1. Mostre as 10 melhores universidades do mundo (menor world_rank) 
# 2. Mostre as 5 melhores universidades do Brasil (se existirem) 
# 3. Mostre universidades com score maior que 90 
# 4. Mostre universidades dos EUA com score maior que 80

# Exercício 4 – Seleção Avançada 
# 1. Mostre apenas as colunas: institution,
# country e score 
# 2. Mostre universidades entre rank 50 e 100 
# 3. Mostre universidades cujo país é “United Kingdom”

# ============================================================ PARTE 3 –
# MISSING VALUES
# ============================================================

# Exercício 5 – Valores Ausentes 
# 1. Quantos valores nulos existem na coluna broad_impact? 
# 2. Qual percentual do dataset é nulo? 
# 3. Remova linhas com broad_impact nulo 
# 4. Preencha valores nulos com a média 
# 5. Compare a média antes e depois do preenchimento

# ============================================================ PARTE 4 –
# GROUPBY (ANÁLISE POR PAÍS E ANO)
# ============================================================

# Exercício 6 – Análise por País 
# 1. Média do score por país 
# 2. País com maior média de score 
# 3. Quantidade de universidades por país 
# 4. Top 10 países com mais universidades

# Exercício 7 – Análise por Ano 
# 1. Média do score por ano 
# 2. Qual ano teve maior média? 
# 3. Faça um gráfico da evolução do score médio ao longo do tempo


# ============================================================
# RESOLUÇÃO
# ============================================================

# Exercício 1
# 1.
import pandas as pd
# Criando o df
df = pd.read_csv('notas.csv')
# Inspeciando a estrutura do DF — Quantas linhas e colunas existem?
linhas, colunas = df.shape
print(f"O dataframe possui {linhas} linhas e {colunas} colunas")

#2.
print(f"O df é composto por dados dos tipos: {df.dtypes}")

#3. 
# contando os valores nulos por coluna
print(print(df.isnull().sum()))

#4.
df_ano = df['year'] # Isolando a coluna com a informação necessária
print(f'A nossa base de dados é composta por {df_ano.nunique()} anos, {df_ano.unique()}') # Separação entre número de anos e quais são os anos.

#5.
df_paises = df['country'] # isolando a base de informação necessária
print(f"O nosso dataframe é composto por {df_paises.nunique()} países") # Entrega exatamente quantos — numero inteiro
print(f"Os países presentes são: {df_paises.unique()}") # Entrega a composição — lista

# Exercício 2
#1. 
# calculando a média do Score 
media_score = df['score'].mean()
print(f"A média do Score é: {media_score}")

#2.
# Isolando o maior Score
maior_score = df['score'].max()
print(f" O maior score é de: {maior_score}")

#3.
# Isolando o menor Score
menor_score = df['score'].min()
print(f"O menor Score é de: {menor_score}")

#4.
# Como a questão nos pede por ano é necessário usar o groupby para isolar o cada componente da coluna
media_score_ano = df.groupby('year')['score'].mean()
print(f" A média do Score por ano é de: {media_score_ano}")

#5.
# Calculando o desvio padrão do score
dp_score = df['score'].std()
print(f"o desvio padrão do score é: {dp_score:.2f}")

# Exercício 3
#1.
# Classificando as 10 melhores universidades
df_rank = df[['world_rank', 'institution','quality_of_education']].sort_values(by="world_rank", ascending= True)
print(f"As 10 melhores universidades do mundo são: {df_rank.head(10)}")

#2.
# Criando um DF isolado para o Brasil, já ordenado
df_brasil = df[df['country']== 'Brazil'].sort_values(by='world_rank', ascending= True)
print(f"As melhores universidades do Brasil são: {df_brasil.head(5)}")

#3. 
# Aqui basta utilizar o DF préexistente e filtrar para instituições com uma pontuação acima de 90
# Pode ser feito aplicando filtro ou diretamente pela função print

# Aplicando filtro primeiro
filtro_score = df[df['score'] > 90]
print(f"{filtro_score[['institution', 'score', 'year', 'country']]}")

# Diretamente pelo print
print(f"{df[df['score'] > 90]}")

#4.
# Aqui será necessário aplicar um filtro duplo — utilizar '&'
filtro_usa_score = df[(df['country']== 'USA') & (df['score'] > 80)]
print(f" As universidades americanas com score acima de 80 são: {filtro_usa_score}")

# Exercício 4.
#1.
# Mostrar apenas as colunas determinadas pelo enunciado pode ser feito apenas utilizando a função print
print(df[['institution', 'country', 'score']])

#2.
# Aqui é preciso utilizar um filtro duplo
# O primeiro é utilizado para selecionar as universidades com score igual ou maior a 50
# O segundo filtro será utilizando para selecionar as universidades com score igual ou menor a 100

filtro_50_100 = df[(df['world_rank'] >= 50) & (df['world_rank'] <= 100)]
print(filtro_50_100)

#3.
# Aqui vamos usar um filtro único para filtrar univesidades em determinada região
# Ao imprimir e resultado vamos restrinigir apenas a universidades e ao país respectivo

filtro_uk = df[df['country']== 'United Kingdom']
print(f" Aqui estão todas as universidades cituadas no reino unido: {filtro_uk[['institution', 'country']]}")

# Exercício 5
#1.
print(f"Valores nulos em broad impact: {df['broad_impact'].isnull().sum()}")

#2. 
# Basta dividir o número de valores nulos pela quantidade total de dados do data set
percentual_nulo = (df['broad_impact'].isnull().sum()/df.size) * 100
print(f" O percentual de valores nulos neste dataset é de: {percentual_nulo:.2f}%")

#3.
# Para remover os valores nulos de 'broad impact' nós vamos utilizar a função 'dropna()'
df_sem_nulos = df.dropna(subset=['broad_impact'])
print(df_sem_nulos)

#4.
# Calcuando a média antes do preenchimento
media_antes = df['broad_impact'].mean()
df['broad_impact'] = df['broad_impact'].fillna(media_antes) # preenchendo os valores nulos do dataset com a média utilizando a função fillna

#5.
# Comparando as médias
media_depois = df['broad_impact'].mean()
print(media_antes)
print(media_depois)

# Exercício 6
#1.
score_por_pais = df.groupby('country')['score'].mean()
print(score_por_pais)

#2.
maior_media_score = score_por_pais.idxmax()
print(maior_media_score)
print(score_por_pais[maior_media_score])

#3. e 4.
universidades_por_pais = df.groupby('country')['institution'].count()
universidades_por_pais = universidades_por_pais.sort_values(ascending= False)
print(universidades_por_pais.head(10))

# Exercício 7
#1. A lógica é muito similar a questão 6 — utilizaremos a função gruopby
filtro_score_pais = df.groupby('year')['score'].mean()
print(filtro_score_pais)

#2. Basta usar a função a 'idxmax' no filtro
ano_maior_score = filtro_score_pais.idxmax()
print(f"o ano com o maior score médio é: {ano_maior_score}")

#3.
# importar biblioteca necessário
import matplotlib.pyplot as plt
filtro_score_pais.plot(kind='line', marker='o', title='Evolução do Score Médio por Ano')
plt.xlabel('Ano')
plt.ylabel('Score Médio')
plt.tight_layout()
plt.show()


