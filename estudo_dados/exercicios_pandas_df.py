"""
Aula - Exercicios de Pandas DataFrame
Como usar:
1) Leia o enunciado de cada bloco.
2) Complete o codigo onde estiver RESOLUCAO.
3) Rode o arquivo e valide os resultados com print.

Requisito:
- Instalar pandas: pip install pandas

Regra da aula:
- Pense no DataFrame como uma planilha.
- Resolva um exercicio por vez.
"""

import pandas as pd


# -------------------------------------------------
# BLOCO 1: criar DataFrame e inspecionar estrutura
# -------------------------------------------------

dados_vendas = {
    "mes": ["Jan", "Jan", "Fev", "Fev", "Mar", "Mar"],
    "filial": ["Centro", "Norte", "Centro", "Norte", "Centro", "Norte"],
    "vendas": [12000, 9500, 13500, 10200, 14100, 11000],
    "clientes": [210, 180, 225, 190, 235, 205],
}

# Exercicio 1:
# a) Crie o DataFrame df_vendas usando dados_vendas
# b) Mostre as 5 primeiras linhas
# c) Mostre o formato (linhas, colunas)
# d) Mostre os tipos de dados das colunas



# RESOLUCAO: complete aqui

# A)
df_vendas = pd.DataFrame(dados_vendas)

# B)
print(df_vendas.head())

# C)
df_vendas.shape

# D)
df_vendas.dtypes

# -------------------------------------------------
# BLOCO 2: selecionar colunas e linhas
# -------------------------------------------------

# Exercicio 2:
# a) Mostre apenas as colunas "mes" e "vendas"
# b) Mostre somente a primeira linha
# c) Mostre as linhas de indice 2 ate 4

# RESOLUCAO: complete aqui
# A)
print(df_vendas[["mes", "vendas"]])

# B)
print(df_vendas.iloc[0])

# C)
print(df_vendas.iloc[2:5])

# -------------------------------------------------
# BLOCO 3: filtros com condicoes de negocio
# -------------------------------------------------

# Exercicio 3:
# a) Filtre vendas acima de 12000
# b) Filtre apenas a filial "Centro"
# c) Filtre vendas acima de 11000 na filial "Norte"

# RESOLUCAO: complete aqui

# A)
df_filtro = df_vendas[df_vendas["vendas"] > 12000]
print(df_filtro)

# B) 
df_filtro_filial = df_vendas[df_vendas["filial"] == "Centro"]
print(df_filtro_filial)

# C)
df_filtro_filial_vendas = df_vendas[df_vendas["vendas"] > 11000] & df_vendas[df_vendas["filial"] == "Norte"]


# -------------------------------------------------
# BLOCO 4: novas colunas e metricas
# -------------------------------------------------

# Exercicio 4:
# a) Crie a coluna "ticket_medio" = vendas / clientes
# b) Crie a coluna "meta_batida" com True para vendas >= 13000
# c) Mostre apenas "filial", "mes", "ticket_medio", "meta_batida"

# RESOLUCAO: complete aqui
# A)
df_vendas["ticket_medio"] = df_vendas["vendas"]/df_vendas["clientes"]
print(df_vendas)

# B)
df_vendas["meta_batida"] = df_vendas["vendas"] >= 130000
print(df_vendas)

# C)
print(df_vendas[["filial", "mes", "ticket_medio", "meta_batida"]])

# -------------------------------------------------
# BLOCO 5: agregacao com groupby
# -------------------------------------------------

# Exercicio 5:
# a) Calcule total de vendas por filial

# b) Calcule media de clientes por mes

# c) Descubra a filial com maior total de vendas

# RESOLUCAO: complete aqui

total_vendas = df_vendas.groupby("filial")["vendas"].sum()
print(total_vendas)

media_clientes = df_vendas.groupby("mes")["clientes"].mean()
print(media_clientes)

mais_vendas = total_vendas.idxmax()
print(mais_vendas)

# -------------------------------------------------
# BLOCO 6: ordenacao e ranking
# -------------------------------------------------

# Exercicio 6:
# a) Ordene df_vendas por "vendas" em ordem decrescente
# b) Pegue os 3 maiores resultados de vendas
# c) Mostre um ranking com "filial", "mes", "vendas"

# RESOLUCAO: complete aqui
df_vendas_ordenado = df_vendas.sort_values(by="vendas", ascending = False)
print(df_vendas_ordenado)

print(df_vendas_ordenado.head(3))

df_rank = df_vendas_ordenado[["filial", "mes", "vendas"]].copy()
df_rank["ranking"] = df_rank["vendas"].rank(ascending=False, method="min").astype(int)
print(df_rank)

# -------------------------------------------------
# BLOCO 7: desafio final de analise
# -------------------------------------------------

# Exercicio 7 (desafio):
# 1) Gere um resumo por filial com:
#    - total_vendas
#    - media_ticket_medio
#    - total_clientes
# 2) Ordene o resumo por total_vendas (desc)
# 3) Exiba qual filial teve melhor desempenho geral

# RESOLUCAO: complete aqui


# ---------------------
# CHECKLIST DE REVISAO
# ---------------------
#
# [ ] Sei criar um DataFrame com dicionario
# [ ] Sei selecionar colunas e linhas
# [ ] Sei filtrar dados com condicoes
# [ ] Sei criar novas colunas no DataFrame
# [ ] Sei agregar dados com groupby
# [ ] Sei ordenar e criar ranking

