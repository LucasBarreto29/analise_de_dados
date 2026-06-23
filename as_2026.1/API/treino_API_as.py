import requests
import pandas as pd

# =============================================================================
# SIMULADO — APIs com IPEA e Laboratório de Finanças
# Token Laboratório de Finanças (válido até ~2025):
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTgxMzcxNDE2NiwiaWF0IjoxNzgyMTc4MTY2LCJqdGkiOiJlMjIyOTAzY2YzNGU0MjJlYmY3NDY4OWE3MGFhMDg3ZiIsInVzZXJfaWQiOiIxNTQifQ.lxqhEgHrgN0gMYHJBhODqmTFv_UHsCffRWDC0oTjrwQ"
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
params = {"ticker": "PETR4", "data_ini": "2024-01-02", "data_fim": "2024-12-30"}
response = requests.get(
    f"{BASE_URL_LAB}/preco/corrigido",
    headers={"Authorization": f"Bearer {TOKEN}"},
    params=params,
    verify=False
)
print(response.status_code)

dados3 = response.json()
df_lab = pd.DataFrame(dados3)
print(df_lab)

preco_ini = float(df_lab[df_lab["data"] == '2024-01-02']["fechamento"].iloc[0])
preco_fim = float(df_lab[df_lab["data"] == '2024-12-30']["fechamento"].iloc[0])

rendimento_petr4 = ((preco_fim/preco_ini) - 1)*100
print(f"{rendimento_petr4:.2f}%")

params2 = {"ticker": "ITUB4", "data_ini": "2024-01-02", "data_fim": "2024-12-30"}
response2 = response = requests.get(
    f"{BASE_URL_LAB}/preco/corrigido",
    headers={"Authorization": f"Bearer {TOKEN}"},
    params=params2,
    verify=False
)
print(response2.status_code)

dados4 = response2.json()
df_lab2 = pd.DataFrame(dados4)

preco_ini2 = float(df_lab2[df_lab2["data"] == '2024-01-02']["fechamento"].iloc[0])
preco_fim2 = float(df_lab2[df_lab2["data"] == '2024-12-30']["fechamento"].iloc[0])

rendimento_itub4 = ((preco_fim2/preco_ini2) -1 ) *100
print(f"{rendimento_itub4:.2f}%")
