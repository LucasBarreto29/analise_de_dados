# LISTA DE EXERCÍCIOS – ANÁLISE DE DADOS COM PANDAS Dataset: Ranking
# Mundial de Universidades (notas.csv)

import pandas as pd

# ============================================================
# EXPLORAÇÃO INICIAL (EDA BÁSICA)
# ============================================================

# Exercício 1 – Conhecendo o Dataset 
# 1. Quantas linhas e colunas existem?

df_csv = pd.read_csv('/Users/lucas/Desktop/analise_dados/analise_de_dados/notas.csv')
print(df_csv.shape)

# 2. Quais são os tipos de dados?
 
print(df_csv.dtypes)

# 3. Existe coluna com valores ausentes?

df_null = df_csv.isnull().sum()
print(df_null[df_null > 0])

# 4. Qual é o período de anos disponível?

print(df_csv['year'].min(), df_csv['year'].max())

# 5. Quantos países diferentes existem?

print(df_csv['country'].nunique())

# Exercício 2 – Estatísticas Gerais 
# 1. Média do score 
# 2. Maior score 
# 3.Menor score 
# 4. Média do score por ano 
# 5. Desvio padrão do score

print(df_csv['score'].mean())
print(df_csv['score'].max())
print(df_csv['score'].min())
print(df_csv.groupby('year')['score'].mean())
print(df_csv['score'].std())

# ============================================================
# FILTROS E SELEÇÕES
# ============================================================

# Exercício 3 – Top Universidades 
# 1. Mostre as 10 melhores universidades do mundo (menor world_rank) 

world_top_10 = df_csv.nsmallest(10, 'world_rank')
print(world_top_10[['institution', 'country', 'score', 'year']])

# 2. Mostre as 5 melhores universidades do Brasil (se existirem)

brazil_top_5 = df_csv[df_csv['country'] == 'Brazil'].nsmallest(5, 'world_rank')
print(brazil_top_5[['institution', 'country', 'score', 'year']])

# 3. Mostre universidades com score maior que 90
 
above_90 = df_csv[df_csv['score'] > 90]
print(above_90[['institution', 'country', 'score', 'year']])

# 4. Mostre universidades dos EUA com score maior que 80

eua_above_80 = df_csv[(df_csv['country'] == 'USA') & (df_csv['score'] > 80)]
print(eua_above_80[['institution', 'country', 'score', 'year']])

# Exercício 4 – Seleção Avançada 
# 1. Mostre apenas as colunas: institution,
# country e score
 
selected_columns = df_csv[['institution', 'country', 'score']]
print(selected_columns)

# 2. Mostre universidades entre rank 50 e 100 

rank_50_100 = df_csv[(df_csv['world_rank'] >= 50) & (df_csv['world_rank'] <= 100)]
print(rank_50_100[['institution', 'country', 'score', 'year']])

# 3. Mostre universidades cujo país é “United Kingdom”

uk_universities = df_csv[df_csv['country'] == 'United Kingdom']
print(uk_universities[['institution', 'country', 'score', 'year']])

# ============================================================ PARTE 3 –
# MISSING VALUES
# ============================================================

# Exercício 5 – Valores Ausentes 
# 1. Quantos valores nulos existem na coluna broad_impact? 

print(df_csv['broad_impact'].isnull().sum()) # Existem 200 valores nulos na coluna broad_impact.

# 2. Qual percentual do dataset é nulo? 

total_rows = len(df_csv)
print(f"Percentual de valores nulos: {df_csv['broad_impact'].isnull().sum() / total_rows * 100:.2f}%") # 9.09% do dataset é nulo na coluna broad_impact.

# 3. Remova linhas com broad_impact nulo
df_no_null = df_csv.dropna(subset=['broad_impact'])
print(df_no_null.shape) # Após remover as linhas com broad_impact nulo, o dataset tem 1980 linhas e 7 colunas.
# 4. Preencha valores nulos com a média 

broad_impact_mean = df_csv['broad_impact'].mean()
df_filled = df_csv.copy()
df_filled['broad_impact'] = df_filled['broad_impact'].fillna(broad_impact_mean)
print(df_filled['broad_impact'].isnull().sum())
# 5. Compare a média antes e depois do preenchimento

print(f"Média antes do preenchimento: {broad_impact_mean:.2f}")
print(f"Média depois do preenchimento: {df_filled['broad_impact'].mean():.2f}") # A média antes do preenchimento é a mesma que a média depois do preenchimento, porque os valores nulos foram preenchidos com a média original, o que não altera a média geral da coluna.


# ============================================================ PARTE 4 –
# GROUPBY (ANÁLISE POR PAÍS E ANO)
# ============================================================

# Exercício 6 – Análise por País 
# 1. Média do score por país 
# 2. País com maior média de score 
# 3. Quantidade de universidades por país 
# 4. Top 10 países com mais universidades

# média do score por país
score_by_country = df_csv.groupby('country')['score'].mean()
print(score_by_country)

# país com maior média de score
best_country = score_by_country.idxmax()
print(f"País com maior média de score: {best_country} ({score_by_country[best_country]:.2f})")

# quantidade de universidades por país
universities_by_country = df_csv['country'].value_counts()
print(universities_by_country)

# top 10 países com mais universidades
top_10_countries = universities_by_country.head(10)
print(top_10_countries)

# Exercício 7 – Análise por Ano 
# 1. Média do score por ano 
# 2. Qual ano teve maior média? 
# 3. Faça um gráfico da evolução do score médio ao longo do tempo

# calculando a média de score por ano
score_by_year = df_csv.groupby('year')['score'].mean()
print(score_by_year)    

# ano com maior média de score
best_year = score_by_year.idxmax()
print(f"Ano com maior média de score: {best_year} ({score_by_year[best_year]:.2f})")

# gráfico da evolução do score médio ao longo do tempo
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 5))
plt.plot(score_by_year.index, score_by_year.values, marker='o')
plt.title('Evolução do Score Médio ao Longo do Tempo')
plt.xlabel('Ano')
plt.ylabel('Score Médio')
plt.grid()
plt.show()