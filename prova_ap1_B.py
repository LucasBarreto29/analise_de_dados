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