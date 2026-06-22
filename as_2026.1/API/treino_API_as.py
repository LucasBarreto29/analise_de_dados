import requests
import pandas as pd

# =============================================================================
# SIMULADO — APIs com IPEA e Laboratório de Finanças
# Token Laboratório de Finanças (válido até ~2025):
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2OTQyMDE1LCJpYXQiOjE3NzQzNTAwMTUsImp0aSI6ImI3M2UyZGUyMmNkYTQ1ZWQ5ZmI2ZWZhYTAwZGM4N2I3IiwidXNlcl9pZCI6IjExNSJ9.BYwtttiHVt8EVA_653elnaGNcPAHdaWjlec9pusQLu7I"
BASE_URL_LAB = "https://laboratoriodefinancas.com/api/v2"
BASE_URL_IPEA = "http://www.ipeadata.gov.br/api/odata4/Metadados/"
# =============================================================================


# (1,5) QUESTÃO 1 — IPEA: Descobrindo séries de inflação por faixa de renda
# O IPEA disponibiliza metadados de todas as suas séries econômicas.
# Acesse o endpoint de metadados do IPEA e transforme o retorno em um DataFrame.
# A partir dele, filtre apenas as séries cuja fonte (FNTSIGLA) seja "IPEA"
# e cujo nome da série (SERNOME) contenha a palavra "inflação" (sem diferenciar maiúsculas).
# Quantas séries atendem a esses dois critérios simultaneamente?

# Construindo o DataFrame
# Passo 1: Definir a URL do ENDPOINT
url = "http://www.ipeadata.gov.br/api/odata4/Metadados/"

# Passo 2: Fazer a requisição utilizando requests
response = requests.get(url)

# Passo 3: Verificar status
print(response.status_code) # resultado foi 200. OK.

# Passo 4: Extrair os dados em fomato json
dados = response.json()["value"] # sempre usar ["value"] ao trabalhar com API do IPEA

# Passo 5: Transformar os dados extraídos em um data frame
df_ipea = pd.DataFrame(dados)

# Encontrando a série
# Similar a aplicar um filtro comum
serie_ipea = df_ipea[df_ipea['FNTSIGLA'] == "IPEA"]
serie_inflacao = serie_ipea[serie_ipea['SERNOME'].str.contains(r"inflação", case= False)]
# Contando exatamente quantas séries antendem aos critérios estabelecidos
print(f"Existe um total de {serie_inflacao['SERNOME'].count()} séries que atendem aos critérios de seleção. São elas: {serie_inflacao['SERNOME'].unique()}")

# (1,5) QUESTÃO 2 — IPEA: Acessando e analisando uma série temporal
# A Fipe divulga pelo IPEA a série do IPC (Índice de Preços ao Consumidor) anual.
# Nos metadados, essa série tem FNTSIGLA == "Fipe" e SERNOME contém "taxa de inflação".
# Identifique o SERCODIGO dessa série.
# Acesse a API de valores usando o endpoint:
#   f"http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{codigo}')"
# Construa um DataFrame com as colunas VALDATA e VALVALOR.
# Em qual ano foi registrada a maior taxa de inflação? Exiba a data e o valor.
serie_fipe = df_ipea[df_ipea['FNTSIGLA'] == "Fipe"]
serie_ipc = serie_fipe[serie_fipe['SERNOME'].str.contains(r"taxa de inflação", case= False)]
print(serie_fipe[["SERNOME", "SERCODIGO"]])

codigo_ipc = 'FIPE_FIPE0001'
url2 = f"http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{codigo_ipc}')"
response = requests.get(url2)
print(response.status_code)
dados2 = response.json()["value"]
df_ipc = pd.DataFrame(dados2)[["VALDATA", "VALVALOR"]]
maior_valor = df_ipc.loc[df_ipc['VALVALOR'].idxmax()]

# (1,5) QUESTÃO 3 — Lab de Finanças: Rendimento comparado
# Usando a API do Laboratório de Finanças (endpoint: /preco/corrigido),
# calcule e compare o rendimento de PETR4 e ITUB4 ao longo de 2024
# (de 2024-01-02 até 2024-12-30).
# Qual das duas ações rendeu mais? Exiba o rendimento de cada uma em percentual (%).
# Dica: rendimento = (preço_fim / preço_ini) - 1


# (1,5) QUESTÃO 4 — Lab de Finanças: Análise setorial do Planilhão
# Acesse o Planilhão (endpoint: /bolsa/planilhao) na data base 2024-04-01.
# Calcule a mediana do P/L (coluna: "pl") por setor ("setor").
# Exiba os 5 setores com maior mediana de P/L, em ordem decrescente.
# Ignore setores onde o P/L mediano seja negativo.


# (1,5) QUESTÃO 5 — Lab de Finanças: Screening de ações
# Ainda usando o Planilhão de 2024-04-01, monte um screening com os seguintes filtros:
#   - Setor: "financeiro"
#   - Dividend Yield (coluna: "dy") maior que 5%  →  dy > 0.05
#   - P/VP (coluna: "pvp") menor que 2
# Exiba os tickers que passam em todos os critérios, ordenados pelo maior DY.


# (1,5) QUESTÃO 6 — Lab de Finanças: Magic Formula adaptada por setor
# Com os dados do Planilhão de 2024-04-01, aplique a Magic Formula
# (usando ROIC e Earning Yield, colunas: "roic" e "earning_yield")
# MAS desta vez monte uma carteira de 5 ações exclusivamente do setor "energia".
# Ranqueie dentro do setor (rank crescente para ambos os indicadores),
# some os ranks e selecione as 5 melhores (menor rank_final).
# Exiba os tickers escolhidos e o setor confirmado.
