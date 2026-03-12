"""
Aula - Exercicios de Pandas DataFrame
Como usar:
1) Leia o enunciado de cada bloco.
2) Complete o codigo onde estiver RESOLUCAO.
3) Rode o arquivo e valide os resultados.

Requisito:
- Instalar pandas: pip install pandas

Regra da aula:
- Pense no DataFrame como uma planilha.
- Resolva um exercicio por vez.
"""
# -------------------------------------------------
# BLOCO 1: criar DataFrame e inspecionar estrutura
# -------------------------------------------------
import pandas as pd
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
df_dados_vendas = pd.DataFrame(dados_vendas)
print(df_dados_vendas.head(5))
print(df_dados_vendas.shape)
print(df_dados_vendas.dtypes)

# -------------------------------------------------
# BLOCO 2: selecionar colunas e linhas
# -------------------------------------------------

# Exercicio 2:
# a) Mostre apenas as colunas "mes" e "vendas"
# b) Mostre somente a primeira linha
# c) Mostre as linhas de indice 2 ate 4

# RESOLUCAO: complete aqui
print(df_dados_vendas[["mes", "vendas"]])
print(df_dados_vendas.head(1))
print(df_dados_vendas.iloc[2:5])

# -------------------------------------------------
# BLOCO 3: filtros com condicoes de negocio
# -------------------------------------------------

# Exercicio 3:
# a) Filtre vendas acima de 12000
# b) Filtre apenas a filial "Centro"
# c) Filtre vendas acima de 11000 na filial "Norte"

# RESOLUCAO: complete aqui
print(df_dados_vendas[df_dados_vendas["vendas"] > 12000])
print(df_dados_vendas[df_dados_vendas["filial"] == "Centro"])
print(df_dados_vendas[(df_dados_vendas["vendas"] > 11000) & (df_dados_vendas["filial"] == "Norte")])

# -------------------------------------------------
# BLOCO 4: novas colunas e metricas
# -------------------------------------------------

# Exercicio 4:
# a) Crie a coluna "ticket_medio" = vendas / clientes
# b) Crie a coluna "meta_batida" com True para vendas >= 13000
# c) Mostre apenas "filial", "mes", "ticket_medio", "meta_batida"

# RESOLUCAO: complete aqui
df_dados_vendas["ticket_medio"] = df_dados_vendas["vendas"] / df_dados_vendas["clientes"]
df_dados_vendas["meta_batida"] = df_dados_vendas["vendas"] >= 13000
print(df_dados_vendas[["filial", "mes", "ticket_medio", "meta_batida"]])
# -------------------------------------------------
# BLOCO 5: agregacao com groupby
# -------------------------------------------------

# Exercicio 5:
# a) Calcule total de vendas por filial
# b) Calcule media de clientes por mes
# c) Descubra a filial com maior total de vendas

# RESOLUCAO: complete aqui
total_vendas_filial = df_dados_vendas.groupby("filial")["vendas"].sum()
print(total_vendas_filial)

media_clientes = df_dados_vendas.groupby("mes")["clientes"].mean()
print(media_clientes)

filial_maior_vendas = total_vendas_filial.idxmax()
print(filial_maior_vendas)
# -------------------------------------------------

# BLOCO 6: ordenacao e ranking
# -------------------------------------------------

# Exercicio 6:
# a) Ordene df_vendas por "vendas" em ordem decrescente
# b) Pegue os 3 maiores resultados de vendas
# c) Mostre um ranking com "filial", "mes", "vendas"

# RESOLUCAO: complete aqui
ranking_vendas = df_dados_vendas.sort_values(by="vendas", ascending=False)
print(ranking_vendas)

print(ranking_vendas.head(3))

ranking_filial_mes_vendas = df_dados_vendas[["filial", "mes", "vendas"]].sort_values(by="vendas", ascending=False)
print(ranking_filial_mes_vendas)
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

# identificando filiais
print(df_dados_vendas[["filial"]]) # apenas duas filais: Centro e Norte

# gerando resumo
resumo_filial = df_dados_vendas.groupby("filial").agg(
    total_vendas=pd.NamedAgg(column="vendas", aggfunc="sum"),
    media_ticket_medio=pd.NamedAgg(column="ticket_medio", aggfunc="mean"),
    total_clientes=pd.NamedAgg(column="clientes", aggfunc="sum")
).reset_index()
print(resumo_filial)

# exibindo melhor desempenho
resumo_filial_ordenado = resumo_filial.sort_values(by="total_vendas", ascending=False)
print(resumo_filial_ordenado)

# definindo melhor desempenho e exebindo resultado
filial_melhor_desempenho = resumo_filial_ordenado.iloc[0]["filial"]
print(filial_melhor_desempenho)

# ===========================================================
# PARTE 1 – Estrutura lista + dicionário
# ===========================================================

dados_list_dict = [{
   "Column A":[1, 2, 3],
   "Column B":[4, 5, 6],
   "Column C":[7, 8, 9]
}]


# -----------------------------------------------------------
# EXERCÍCIO 1 – Explorando a estrutura
# -----------------------------------------------------------

# 1. Qual é o tipo de dados_list_dict?
# 2. Qual é o tipo do primeiro elemento?
# 3. Como acessar a lista da "Column A"?
# 4. Como acessar o segundo elemento da "Column C"?

# RESPONDA AQUI:
print(type(dados_list_dict)) # lista
print(type(dados_list_dict[0])) # dicionário
print(dados_list_dict[0]["Column A"])
print(dados_list_dict[0]["Column C"][1])
# -----------------------------------------------------------
# EXERCÍCIO 2 – Convertendo para DataFrame
# -----------------------------------------------------------

# 1. Converta dados_list_dict[0] em um DataFrame chamado df1
# 2. Mostre:
#    - shape
#    - tipos das colunas
# 3. Calcule:
#    - soma de cada coluna
#    - média de cada coluna

# RESOLVA AQUI:
#Craindo o DataFrame
df1 = pd.DataFrame(dados_list_dict[0])
print(df1)
# mostrando shape e tipos
print(df1.shape)
print(df1.dtypes)

# calculando soma e média
print(df1.sum())
print(df1.mean())
# -----------------------------------------------------------
# EXERCÍCIO 3 – Criando novas colunas
# -----------------------------------------------------------

# No df1:
# 1. Crie coluna "Total" = soma das colunas
# 2. Crie coluna "Media" = média por linha
# 3. Filtre linhas onde Total > 10

# RESOLVA AQUI:
#criando a coluna Total
df1["total"] = df1.sum(axis=1)
# criando a coluna Media
df1["media"] = df1.mean(axis=1)
print(df1)
# filtrando linhas onde Total > 10
df1_filtrado = df1[df1["total"] > 10]
print(df1_filtrado)
# -----------------------------------------------------------

# EXERCÍCIO 4 – Conversões estruturais
# -----------------------------------------------------------

# 1. Converta df1 para:
#    - lista de dicionários [ {linha1}, {linha2}, {linha3} ]
#    - dicionário de listas { coluna1: [valores], coluna2: [valores] }
# Dica:
# orient="records":
#   Cada elemento representa uma linha.
#   Estrutura ideal para APIs e JSON.

# orient="list":
#   Cada chave representa uma coluna.
#   Estrutura colunar, útil para reconstruir DataFrame.


# RESOLVA AQUI:
# criando a lista de dicionários
lista_dicionarios = df1.to_dict(orient="records")
print(lista_dicionarios)
# criando o dicionário de listas 
dicionario_listas = df1.to_dict(orient="list")  
print(dicionario_listas)
# -----------------------------------------------------------
# EXERCÍCIO 5 – Trabalhando com lista
# -----------------------------------------------------------

# 1. Transforme a coluna "Column A" em uma lista chamada lista_a.
# 2. Multiplique cada elemento da lista por 10.
# 3. Crie uma nova coluna chamada "Column A x10" com essa nova lista.

# RESOLVA AQUI:
lista_a = df1["Column A"].tolist()
print(lista_a)
# multiplicando cada elemento por 10
lista_10x = [x * 10 for x in lista_a]
# incorporando a nova lista ao dataframe
df1["Column A x10"] = lista_10x
print(df1)
# ===========================================================
# BASE DE DADOS

dados = [
    {"id_pais": 0, "nome_pais": "Brasil", "id_produto": 101, "descricao": "Produto A",
     "tipo_operacao": "Exportação", "tipo_periodo": "Mensal", "periodo": "2023-01", "valor": 5000},

    {"id_pais": 0, "nome_pais": "Brasil", "id_produto": 102, "descricao": "Produto B",
     "tipo_operacao": "Exportação", "tipo_periodo": "Mensal", "periodo": "2023-01", "valor": 3000},

    {"id_pais": 1, "nome_pais": "Argentina", "id_produto": 101, "descricao": "Produto A",
     "tipo_operacao": "Exportação", "tipo_periodo": "Mensal", "periodo": "2023-02", "valor": 4000},

    {"id_pais": 1, "nome_pais": "Argentina", "id_produto": 102, "descricao": "Produto B",
     "tipo_operacao": "Exportação", "tipo_periodo": "Mensal", "periodo": "2023-02", "valor": 6000},

    {"id_pais": 0, "nome_pais": "Brasil", "id_produto": 101, "descricao": "Produto A",
     "tipo_operacao": "Exportação", "tipo_periodo": "Mensal", "periodo": "2023-03", "valor": 7000},
]
# ===========================================================



# ===========================================================
# PARTE 1 – EXPLORAÇÃO INICIAL
# ===========================================================

# Exercício 1
# 1. Qual o tipo da variável dados?
# 2. Quantos registros existem?
# 3. Quais são as chaves do primeiro dicionário?
# 4. Liste todos os países existentes (sem repetição).

# RESOLVA AQUI:
print(type(dados)) # lista
print(len(dados)) # 5 registros
print(list(dados[0].keys())) # chaves do primeiro dicionário
print(set([registro["nome_pais"] for registro in dados])) # países sem repetição
# ===========================================================
# PARTE 2 – CONVERSÃO PARA DATAFRAME
# ===========================================================

# Exercício 2
# 1. Converta dados para DataFrame chamado df
# 2. Mostre shape, tipos e primeiras linhas
# 3. Converta a coluna periodo para datetime

# RESOLVA AQUI:
# convertendo para DataFrame
df = pd.DataFrame(dados)
print(df)
# mostrando shape, tipos e primeiras linhas
print(df.shape)
print(df.dtypes)
print(df.head())
# convertendo a coluna periodo para datetime
df["periodo"] = pd.to_datetime(df["periodo"])
print(df.dtypes)

# ===========================================================
# PARTE 3 – FILTROS E ORDENAÇÃO
# ===========================================================

# Exercício 3 – Filtros
# 1. Filtre apenas Brasil
# 2. Filtre apenas Produto A
# 3. Filtre valor > 4000
# 4. Combine Brasil + Produto A

# RESOLVA AQUI:
# filtrando apenas Brasil
df_brasil = df[df["nome_pais"] == "Brasil"]
print(df_brasil)
# filtrando apenas Produto A
df_produto_a = df[df["descricao"] == "Produto A"]
print(df_produto_a)
# filtrando valor > 4000
df_valor_maior_4000 = df[df["valor"] > 4000]
print(df_valor_maior_4000)
# combinando Brasil + Produto A
df_brasil_produto_a = df[(df["nome_pais"] == "Brasil") & (df["descricao"] == "Produto A")]
print(df_brasil_produto_a)

# Exercício 4 – Ordenação
# 1. Ordene por valor crescente
# 2. Ordene por valor decrescente
# 3. Ordene por periodo e depois por valor

# RESOLVA AQUI:
# ordenando por valor crescente
df_ordenado_crescente = df.sort_values(by="valor", ascending=True)
print(df_ordenado_crescente)
# ordenando por valor decrescente
df_ordenado_decrescente = df.sort_values(by="valor", ascending=False)
print(df_ordenado_decrescente)
# ordenando por periodo e depois por valor
df_ordenado_periodo_valor = df.sort_values(by=["periodo", "valor"], ascending=[True, True])
print(df_ordenado_periodo_valor)


# ===========================================================
# PARTE 4 – AGREGAÇÕES
# ===========================================================

# Exercício 5 – GroupBy Simples
# 1. Total exportado por país
# 2. Total exportado por produto
# 3. Média por país
# 4. Quantidade de operações por país

# RESOLVA AQUI:
# total exportado por país
total_exportado_pais = df.groupby("nome_pais")["valor"].sum()
print(total_exportado_pais)
# total exportado por produto
total_exportado_produto = df.groupby("descricao")["valor"].sum()
print(total_exportado_produto)
# média por país
media_por_pais = df.groupby("nome_pais")["valor"].mean()
print(media_por_pais)
# quantidade de operações por país
quantidade_operacoes_pais = df.groupby("nome_pais").size()
print(quantidade_operacoes_pais)

# Exercício 6 – GroupBy Múltiplo
# Agrupe por nome_pais e descricao
# Calcule soma, média e contagem

# Explique em comentário o que essa tabela representa

# RESOLVA AQUI:
# agrupando por nome_pais e descricao, calculando soma, média e contagem
agrupamento_multiplo = df.groupby(["nome_pais", "descricao"]).agg(  
    total_valor=pd.NamedAgg(column="valor", aggfunc="sum"),
    media_valor=pd.NamedAgg(column="valor", aggfunc="mean"),
    contagem_operacoes=pd.NamedAgg(column="valor", aggfunc="count")
).reset_index()
print(agrupamento_multiplo)
# A tabela representa o total exportado, a média de valor a quantidade exportada para cada combinação de país e produto. Ou seja, ela mostra o desempenho de cada produto em cada país, permitindo comparar qual produto teve o melhor desempenho em valor total de operações por país.


# ===========================================================
# PARTE 5 – PIVOT TABLE
# ===========================================================

# Exercício 7 – Pivot por Produto
# Linhas: periodo
# Colunas: descricao
# Valores: soma de valor

# Responda:
# 1. Qual produto vendeu mais?
# 2. Qual mês teve maior valor total?
# 3. Existe mês sem venda?

# RESOLVA AQUI:
# produto que vendeu mais
pivot_produto = df.pivot_table(index="periodo", columns="descricao", values="valor", aggfunc="sum", fill_value=0)
print(pivot_produto)
total_vendas_produto = pivot_produto.sum()
produto_mais_vendido = total_vendas_produto.idxmax()
print(produto_mais_vendido)
# mês com maior valor total
pivot_produto["total"] = pivot_produto.sum(axis=1)
mes_maior_valor_total = pivot_produto["total"].idxmax()
print(mes_maior_valor_total)
# verificando se existe mês sem venda
meses_sem_venda = pivot_produto[pivot_produto["total"] == 0].index
print(meses_sem_venda)  

# Exercício 8 – Pivot por País
# Linhas: periodo
# Colunas: nome_pais
# Valores: soma de valor

# Explique o que podemos interpretar dessa tabela

# RESOLVA AQUI:
pivot_pais = df.pivot_table(index="periodo", columns="nome_pais", values="valor", aggfunc="sum", fill_value=0)
print(pivot_pais)
# A tabela pivot por país permite comparar o desempenho de cada país em termos de valor exportado ao longo do tempo. Sendo assim, é possível observar tendencias de crescimento ou declínio nas exportações ao longo dos meses, o que nos ajuda a identificar sazonalidades, oportunidades de mercado e desafios.


# ===========================================================
# PARTE 6 – FEATURE ENGINEERING
# ===========================================================

# Exercício 9
# 1. Extraia ano e mês da coluna periodo
# 2. Crie coluna valor_mil (valor / 1000)
# 3. Calcule crescimento percentual por produto mês a mês

# RESOLVA AQUI:
# extraçao de ano e mês
df["ano"] = df["periodo"].dt.year
df["mes"] = df["periodo"].dt.month
print(df[["periodo", "ano", "mes"]])
# criando coluna valor_mil
df["valor_mil"] = df["valor"] / 1000
print(df[["valor", "valor_mil"]])
# calculo do crescimento percentual por produto mês a mês
df = df.sort_values(by=["descricao", "periodo"])
df["crescimento_percentual"] = df.groupby("descricao")["valor"].pct_change()
print(df[["descricao", "periodo", "valor", "crescimento_percentual"]])

# ===========================================================
# PARTE 7 – QUALIDADE DE DADOS
# ===========================================================

# Exercício 10
# 1. Verifique valores nulos
# 2. Verifique valores negativos
# 3. Verifique duplicatas

# RESOLVA AQUI:

# verificando a existencia de valores nulos
print(df.isnull().sum())


# verificando a existencia de valores negativos
print(df[df["valor"] < 0])
# verificando a existencia de duplicatas
print(df[df.duplicated()])


