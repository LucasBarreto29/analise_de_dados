# O dataset NCR Ride Bookings contém registros de corridas urbanas realizadas em regiões da National Capital Region (NCR), que abrange Delhi, Gurgaon, Noida, Ghaziabad, Faridabad e áreas próximas.
# Utilize os arquivos : ncr_ride_bookings.csv para resolver as questoes.
# Principais informaçoes no dataset:
# Date → Data da corrida
# Time → Horário da corrida
# Booking ID → Identificador da corrida
# Booking Status → Status da corrida
# Customer ID → Identificador do cliente
# Vehicle Type → Tipo de veículo
# Pickup Location → Local de embarque
# Drop Location → Local de desembarque
# Booking Value → Valor da corrida
# Ride Distance → Distância percorrida
# Driver Ratings → Avaliação do motorista
# Customer Rating → Avaliação do cliente
# Payment Method → Método de pagamento
# Questões:
# (0,5) 1 - Quantas corridas estão com Status da Corrida como Completada ("Completed") no dataset? 
# Importando biblioteca pandas
import pandas as pd

# Lendo o arquivo CSV
df = pd.read_csv('/Users/lucas/Desktop/analise_dados/analise_de_dados/ap1/ncr_ride_bookings - cópia.csv')

# Criando o filtro
filtro_status = df[df["Booking Status"] == "Completed"]
corridas_completadas = len(filtro_status)
print(f"{corridas_completadas} corridas estão com Status da Corrida como completada") # 93000 corridas completadas ao todo

# (0,5) 2 - Qual a proporção em relação ao total de corridas?
total_corridas = len(df)
proporcao = (corridas_completadas/total_corridas) * 100
print(f"A proporção das corridas completadas em relação ao total de corridas é de {proporcao}%") # 62%


# (0,5) 3 - Calcule a média da Distância ("Ride Distance") percorrida por cada Tipo de veículo.
media_distancia_percorrida = df.groupby("Vehicle Type")["Ride Distance"].mean()
print(media_distancia_percorrida.round(2))


# (0,5) 4 - Qual o Metodo de Pagamento ("Payment Method") mais utilizado pelas bicicletas ("Bike") ?
df_bike = df[df["Vehicle Type"] == "Bike"]
metodo_mais_usado = df_bike["Payment Method"].value_counts().idxmax()
metodo_mais_usado

# (0,5) 5 - Qual o valor total arrecadado ("Booking Value") apenas das corridas Completed?
valor_arrecadado = filtro_status['Booking Value'].sum()
print(f"Valor total arrecadado das corridas completadas: R$ {valor_arrecadado:,.2f}")

# (0,5) 6 - E qual o ticket médio ("Booking Value")dessas corridas Completed?
ticket_medio_corridas_completadas = valor_arrecadado/corridas_completadas
print(f"Ticket médio das corridas completadas: R$ {ticket_medio_corridas_completadas:.2f}")
#ou
ticket_medio = filtro_status["Booking Value"].mean()
print(f"Ticket médio das corridas completadas: R$ {ticket_medio:.2f}")

# (1,5) 7 - O IPEA disponibiliza uma API pública com diversas séries econômicas. 
# Para encontrar a série de interesse, é necessário primeiro acessar o endpoint de metadados.
# Acesse o endpoint de metadados: "http://www.ipeadata.gov.br/api/odata4/Metadados";
# Transforme em um DataFrame;
# Filtre para encontrar as séries da Fipe relacionadas a venda de imoveis (“vendas - Brasil”).
# Dica: 
# Utilize a coluna FNTSIGLA para encontrar a serie da Fipe;
# Utilize a coluna SERNOME para encontrar as vendas de imoveis no Brasil;

import pandas as pd
import requests   # precisamos dessa biblioteca para acessar API

# 1. Acessar o endpoint de metadados
url_metadados = "http://www.ipeadata.gov.br/api/odata4/Metadados"
response = requests.get(url_metadados)

# 2. Transformar o JSON em DataFrame
data = response.json()
df_metadados = pd.DataFrame(data['value'])

# 3. Filtrar as séries da FIPE de vendas de imóveis no Brasil
fipe_vendas = df_metadados[
    (df_metadados['FNTSIGLA'] == 'FIPE') & 
    (df_metadados['SERNOME'].str.contains('vendas - Brasil', case=False))
]

print("Séries encontradas:")
print(fipe_vendas[['SERCODIGO', 'SERNOME']])

# (1,5) 8 -  Descubra qual é o código da série correspondente (coluna: SERCODIGO).
# CODIGO_ENCONTRADO=''
# Usando o código encontrado, acesse a API de valores: f"http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{CODIGO_ENCONTRADO}')"
# Construa um DataFrame através da chave 'value' do retorno da api
# Selecione apenas as colunas datas (VALDATA) e os valores (VALVALOR).
# Exiba a Data e o Valor que teve o valor maximo de vendas.
# Questão 8
CODIGO_ENCONTRADO = "COLE_AQUI_O_CODIGO_DA_QUESTAO_7"   # ← Troque por o código que apareceu na Q7

url = f"http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{CODIGO_ENCONTRADO}')"

response = requests.get(url)

df_valores = pd.DataFrame(response.json()['value'])

# Selecionar só as colunas pedidas
df_valores = df_valores[['VALDATA', 'VALVALOR']]

# Encontrar o valor máximo
linha_maxima = df_valores.loc[df_valores['VALVALOR'].idxmax()]

print("Data e valor máximo de vendas:")
print(linha_maxima)

# (1,5) 9 - Descubra quanto rendeu a VALE no ano de 2025
# base_url = "https://laboratoriodefinancas.com/api/v2"
# token = "SEU_JWT"
# params = {"ticker": "VALE3", "data_ini": "2001-01-01", "data_fim": "2026-12-31"}
# response = requests.get(
#     f"{base_url}/preco/corrigido",
#     headers={"Authorization": f"Bearer {token}"},
#     params=params,
# )
# Questão 9 - Quanto rendeu a VALE no ano de 2025
import pandas as pd
import requests

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "SEU_JWT"   # token

params = {
    "ticker": "VALE3",
    "data_ini": "2025-01-01",
    "data_fim": "2025-12-31"
}

response = requests.get(
    f"{base_url}/preco/corrigido",
    headers={"Authorization": f"Bearer {token}"},
    params=params
)
df_vale = pd.DataFrame(response.json())
df_vale = df_vale.sort_values(by='data')
        
preco_inicial = df_vale['preco_fechamento'].iloc[0]   # ou a coluna correta que vier
preco_final   = df_vale['preco_fechamento'].iloc[-1]
        
retorno = (preco_final / preco_inicial) - 1
        
print(f"Preço inicial (2025): R$ {preco_inicial:.2f}")
print(f"Preço final   (2025): R$ {preco_final:.2f}")
print(f"Retorno total da VALE3 em 2025: {retorno:.4f} ou {retorno*100:.2f}%")

# (1,5) 10 - Você tem acesso à API do Laboratório de Finanças, que fornece dados do Planilhão em formato JSON. 
# Selecione a empresa do setor de "tecnologia" que apresenta o maior ROE (Return on Equity) na data base 2024-04-01.
# Exiba APENAS AS COLUNAS "ticker", "setor" e o "roe"
# base_url = "https://laboratoriodefinancas.com/api/v2"
# token = "SEU_JWT"
# response = requests.get(
#     f"{base_url}/bolsa/planilhao",
#     headers={"Authorization": f"Bearer {token}"},
#     params={"data_base": "2026-04-01"},
# )


# (1,5) 11 - Faça a Magic Formula através dos indicadores Return on Capital (roc) e Earning Yield (ey) no dia 2024-04-01.
# Monte uma carteira de investimento com 10 ações baseado na estratégia Magic Formula.
# base_url = "https://laboratoriodefinancas.com/api/v2"
# token = "SEU_JWT"
# response = requests.get(
#     f"{base_url}/bolsa/planilhao",
#     headers={"Authorization": f"Bearer {token}"},
#     params={"data_base": "2026-04-01"},
# )


# (1,5) 12 - Quantos setores ("setor") tem essa carteira formada por 10 ações?
