# O dataset LOGCP - base_tickets_manutencao_historico.xlsx contém o histórico de incidentes da empresa.
# Através da importantação dos dados através da biblioteca pandas, responda as perguntas abaixo.
# 1 - (1,0) Quantos tickets foram (utilize a coluna "des_status"):
#    - Abertos?
#    - Concluídos?
#    - Cancelados?
# 2 - (1,0) Qual a taxa de conclusão dos tickets em relação ao total?
# 3 - (1,0) Qual categoria tem mais tickets(utilize a coluna "des_categoria")?
# 4 - (1,0) Qual categoria tem maior numero de de cancelamento?

# 5 - (1,0) Quanto rendeu a VALE3 nos ultimos 5 anos entre 2020 e 2025?
# base_url = "https://laboratoriodefinancas.com/api/v2"
# token = "SEU_JWT"
# params = {"ticker": "VALE3", "data_ini": "2001-01-01", "data_fim": "2026-12-31"}
# response = requests.get(
#     f"{base_url}/preco/corrigido",
#     headers={"Authorization": f"Bearer {token}"},
#     params=params,
# )

# 6 - (1,0) A BrasilAPI disponibiliza informações da tabela FIPE, incluindo marcas, modelos e preços de veículos.
# Acesse o endpoint de marcas da FIPE para o tipo de veículo carros.
# import requests
# import pandas as pd
# tipoVeiculo = "carros"
# api = f"https://brasilapi.com.br/api/fipe/marcas/v1/{tipoVeiculo}"
# Transforme em DataFrame e acha o codigo BYD através da coluna "nome"
# Use esse código para acessar o endpoint de modelos da marca BYD.
# codigoMarca=""
# api = f"https://brasilapi.com.br/api/fipe/veiculos/v1/{tipoVeiculo}/{codigoMarca}"
# Construa um DataFrame com os modelos disponíveis.
# Responda: quantos modelos de veículos BYD estão cadastrados na FIPE?

# 7 - (1,0) O Banco Mundial disponibiliza uma API pública com diversos indicadores econômicos. 
# O código do indicador NY.GDP.PCAP.CD corresponde ao PIB per capita (em dólares correntes).
# Usando Python e a biblioteca requests para acessar a API e pandas para manipulação dos dados:
# Acesse o indicador "NY.GDP.PCAP.CD" e o pais "BRA".
# url = f"https://api.worldbank.org/v2/country/{pais}/indicator/{indicador}?format=json"
# Construa um DataFrame atraves do segundo elemento da lista do retorno
# Selecione apenas as colunas anos (date) e os valores de PIB per capita (value).
# Identifique em qual ano o Brasil apresentou o menor PIB per capita e mostre o respectivo valor.


# 8 - (1,0) - Faça um ranking das 30 melhores empresas baseado nos indicadores Return on Equity (roe) e Dividend Yield (dividend_yield) no dia 2024-04-01.
# Faça uma média entre o ranking das empresas com maior ROE e o ranking das empresas com maior dividend_yield
# base_url = "https://laboratoriodefinancas.com/api/v2"
# token = "SEU_JWT"
# response = requests.get(
#     f"{base_url}/bolsa/planilhao",
#     headers={"Authorization": f"Bearer {token}"},
#     params={"data_base": "2026-04-01"},
# )

# 9 - (1,0) Quantos setores ("setor") tem essa carteira formada por 30 ações?


# 10 - (1,0) 11 - Você tem acesso à API do Laboratório de Finanças, que fornece dados do Planilhão em formato JSON. 
# Selecione a empresa do setor de "varejo" que apresenta o maior endividamento na data base 2024-04-01.
# Exiba APENAS AS COLUNAS "ticker", "setor", "preco", "endividamento"
# base_url = "https://laboratoriodefinancas.com/api/v2"
# token = "SEU_JWT"
# response = requests.get(
#     f"{base_url}/bolsa/planilhao",
#     headers={"Authorization": f"Bearer {token}"},
#     params={"data_base": "2026-04-01"},
# )


# 11 - (1,0) O IPEA disponibiliza uma API pública com diversas séries econômicas.
# Para localizar uma série de interesse, é necessário acessar primeiro o endpoint de metadados.
# Acesse o endpoint de metadados:
# "http://www.ipeadata.gov.br/api/odata4/Metadados"
# Transforme o retorno em um DataFrame.
# Filtre para encontrar as séries do IBGE relacionadas à taxa de desemprego no Brasil.
# Dica:
# - Utilize a coluna FNTSIGLA para encontrar as séries do "IBGE";
# - Utilize a coluna SERNOME para encontrar as séries relacionadas a "Taxa de desemprego - cor negra"


# 12 - (1,0) Descubra qual é o código da série correspondente (coluna: SERCODIGO).
# CODIGO_ENCONTRADO = ''
# Usando o código encontrado, acesse a API de valores:
# f"http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{CODIGO_ENCONTRADO}')"
# Construa um DataFrame a partir da chave 'value' do retorno da API.
# Selecione apenas as colunas de data (VALDATA) e valor (VALVALOR).
# Exiba a Data e o Valor em que a taxa de desemprego atingiu o maior valor da série.

# RESOLUÇÃO

# QUESTÃO 1
# importando biblioteca pandas e openpyxl
import pandas as pd
import openpyxl

# Criando o Df
df = pd.read_excel("/Users/lucas/Library/Mobile Documents/com~apple~CloudDocs/Desktop/analise_dados/analise_de_dados/LOGCP_-_base_tickets_manutencao_historico.xlsx")

# Abertos
abertos = len(df[df['des_status'] == 'open']) # Contagem
print(f"Foram abertos {abertos} tickets")

# Concluídos
concluidos = len(df[df['des_status'] == 'solved'])
print(f"Foram concluidos {concluidos} tickets")

# Cancelados
cancelados = len(df[df['des_status'] == 'pending'])
print(f"Foram cancelados {cancelados} tickets")

# QUESTÃO 2
# Calculando a taxa de conclusão dos tickets
# Já temos o filtro para os tickets concluidos ("concluidos"), mas ainda não contamos o total de tickets
# Total de tickets
total_tickets = len(df)

tx_conclusao = (concluidos/total_tickets)*100 # Calculo taxa de conclusao
print(f"A taxa de conclusão de tickets em relação ao total é de {tx_conclusao: .2f}%") 

# QUESTÃO 3
tickets_por_categoria = df.groupby('des_categoria')['des_status'].count()
categoria_mais_tickets = tickets_por_categoria.idxmax()
tickets_max = tickets_por_categoria.max()
print(f"A categoria que tem mais tickets é {categoria_mais_tickets}, com {tickets_max} tickets")

# QUESTÃO 4
# Criando filtro cancelamento
df_cancelamento = df[df['des_status'] == 'pending']
cancelamento_por_categoria = df_cancelamento.groupby('des_categoria')['des_status'].count()
cancelamento_max = cancelamento_por_categoria.max()
categoria_mais_cancelamento = cancelamento_por_categoria.idxmax()
print(f"A categoria que tem maior número de cancelamentos é {categoria_mais_cancelamento}, com {cancelamento_max} cancelamentos")

# QUESTÃO 5
# Importando biblioteca necessária
import requests

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4MTUzMzk4LCJpYXQiOjE3NzU1NjEzOTgsImp0aSI6ImQzOTYzNmNjMmJmYzRjYzE4NDczMTFhYTRhYjJjY2MzIiwidXNlcl9pZCI6IjEwNyJ9.bpVmLSb0WwTzdCtGrap03LxGKwFOvp8VWlL3cH62f80"   # token

params = {
    "ticker": "VALE3",
    "data_ini": "2020-01-01",
    "data_fim": "2025-12-31"
}

response = requests.get(
    f"{base_url}/preco/corrigido",
     headers={"Authorization": f"Bearer {token}"},
     params=params,
)
response.status_code

df_vale = pd.DataFrame(response.json())
df_vale = df_vale.sort_values(by='data')
        
preco_inicial = df_vale['fechamento'].iloc[0]   
preco_final = df_vale['fechamento'].iloc[-1]
        
print(f"Retorno VALE: {preco_final/preco_inicial - 1:.2%}")

# QUESTÃO 8

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4MTUzMzk4LCJpYXQiOjE3NzU1NjEzOTgsImp0aSI6ImQzOTYzNmNjMmJmYzRjYzE4NDczMTFhYTRhYjJjY2MzIiwidXNlcl9pZCI6IjEwNyJ9.bpVmLSb0WwTzdCtGrap03LxGKwFOvp8VWlL3cH62f80"
resp = requests.get(
    f"{base_url}/bolsa/planilhao",
    headers={"Authorization": f"Bearer {token}"},
    params={"data_base": "2021-04-01"},
)

dados= resp.json()
df_carteira = pd.DataFrame(dados)
df2 = df_carteira[["ticker","roe","dividend_yield", "setor"]]
df2["rank_roe"] = df2["roe"].rank(ascending=False)
df2["rank_p_dy"] = df2["dividend_yield"].rank(ascending=False)
df2["rank_final"] = (df2["rank_roe"] + df2["rank_p_dy"] ) / 2
carteira = df2.sort_values("rank_final", ascending=False)['ticker'][:30].tolist()
print(carteira)

# QUESTÃO 9 
carteira_final = carteira
quantidade_setores = carteira_final['setor'].nunique()
print(f"A carteira conta com um total de {quantidade_setores} setores")


# QUESTÃO 10
base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4MTUzMzk4LCJpYXQiOjE3NzU1NjEzOTgsImp0aSI6ImQzOTYzNmNjMmJmYzRjYzE4NDczMTFhYTRhYjJjY2MzIiwidXNlcl9pZCI6IjEwNyJ9.bpVmLSb0WwTzdCtGrap03LxGKwFOvp8VWlL3cH62f80"
response = requests.get(
     f"{base_url}/bolsa/planilhao",
     headers={"Authorization": f"Bearer {token}"},
     params={"data_base": "2026-04-01"},
 )

# QUESTÃO 11
# Acessar o endpoint de metadados
url_metadados = "http://www.ipeadata.gov.br/api/odata4/Metadados"
response_ipea = requests.get(url_metadados)
response_ipea.status_code

# Transformar o JSON em DataFrame
data_ipea = response_ipea.json()
df_metadados = pd.DataFrame(data_ipea)

# Filtrar as séries do IBGE para taxa de desmprego
ibge_desemprego = df_metadados[
    (df_metadados['FNTSIGLA'] == 'IBGE') & 
    (df_metadados['SERNOME'].str.contains('Taxa de desemprego - cor negra', case=False))
]
print(data_ipea[['SERCODIGO', 'SERNOME']])

# QUESTÃO 12
CODIGO_ENCONTRADO = "" 

url = f"http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{CODIGO_ENCONTRADO}')"

response = requests.get(url)

df_valores = pd.DataFrame(response.json()['value'])

# Selecionar só as colunas pedidas
df_valores = df_valores[['VALDATA', 'VALVALOR']]

# Encontrar o valor máximo
linha_maxima = df_valores.loc[df_valores['VALVALOR'].idxmax()]

print("Data e valor máximo de vendas:")
print(linha_maxima)