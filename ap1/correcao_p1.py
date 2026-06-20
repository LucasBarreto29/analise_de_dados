import pandas as pd
import requests
# Chama dataset
df = pd.read_csv(r"ncr_ride_bookings.csv")
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
filtro = df["Booking Status"] == "Completed"
status_completo = df.loc[filtro, "Booking Status"]
contagem_completo = status_completo.count()
print(contagem_completo)
# Resposta: 930000
# (0,5) 2 - Qual a proporção em relação ao total de corridas?
total_corridas = df["Booking Status"].count()
proporcao = contagem_completo /total_corridas
print(proporcao)
# Resposta: 0.62
# (0,5) 3 - Calcule a média da Distância ("Ride Distance") percorrida por cada Tipo de veículo.
df["Ride Distance"] = df["Ride Distance"].astype(float)
agrupamento_distancia = df.groupby(["Vehicle Type"])["Ride Distance"].mean()
# Resposta:
print(agrupamento_distancia)
# (0,5) 4 - Qual o Metodo de Pagamento ("Payment Method") mais utilizado pelas bicicletas ("Bike") ?
bicicleta = df.loc[df["Vehicle Type"] == "Bike", "Payment Method"].max()
print(bicicleta)
# Resposta: Uber Wallet
# (0,5) 5 - Qual o valor total arrecadado ("Booking Value") apenas das corridas Completed?
valor_Arrecadado = df.loc[df["Booking Status"] == "Completed", "Booking Value"]
print(valor_Arrecadado.sum())
#Resposta: 47260574.0
# (0,5) 6 - E qual o ticket médio ("Booking Value") dessas corridas Completed?
ticket_medio = valor_Arrecadado.mean()
print(ticket_medio)
# Resposta
# (1,5) 7 - O IPEA disponibiliza uma API pública com diversas séries econômicas. 
# Para encontrar a série de interesse, é necessário primeiro acessar o endpoint de metadados.
# Acesse o endpoint de metadados: "http://www.ipeadata.gov.br/api/odata4/Metadados";
# Transforme em um DataFrame;
url = "http://www.ipeadata.gov.br/api/odata4/Metadados/"
response = requests.get(url)
response.status_code
dados = response.json()["value"]
df = pd.DataFrame(dados)
# Filtre para encontrar as séries da Fipe relacionadas a venda de imoveis (“vendas - Brasil”).
# Dica: 
# Utilize a coluna FNTSIGLA para encontrar a serie da Fipe;
# Utilize a coluna SERNOME para encontrar as vendas de imoveis no Brasil;
serie_fipe = df.loc[df["FNTSIGLA"] == "Fipe"]
vendas_imoveis_brasil = serie_fipe.loc[df["SERNOME"].str.contains(r"vendas - Brasil", case=False),:]
# (1,5) 8 -  Descubra qual é o código da série correspondente (coluna: SERCODIGO).
CODIGO_ENCONTRADO = 'FIPE12_VENBR12'
# Usando o código encontrado, acesse a API de valores: f"http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{CODIGO_ENCONTRADO}')"
url_2 = "http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='FIPE12_VENBR12')"
response = requests.get(url_2)
response.status_code
# Construa um DataFrame através da chave 'value' do retorno da api
dados = response.json()["value"]
df = pd.DataFrame(dados)
# Selecione apenas as colunas datas (VALDATA) e os valores (VALVALOR).
selecao_data_Valor = df.loc[:, ["VALDATA", "VALVALOR"]]
# Exiba a Data e o Valor que teve o valor maximo de vendas.
maximo_vendas = selecao_data_Valor.loc[selecao_data_Valor["VALVALOR"] == selecao_data_Valor["VALVALOR"].max(), :]
print(maximo_vendas)
# (1,5) 9 - Descubra quanto rendeu a VALE no ano de 2025
base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2OTQyMDE1LCJpYXQiOjE3NzQzNTAwMTUsImp0aSI6ImI3M2UyZGUyMmNkYTQ1ZWQ5ZmI2ZWZhYTAwZGM4N2I3IiwidXNlcl9pZCI6IjExNSJ9.BYwtttiHVt8EVA_653elnaGNcPAHdaWjlc9pusQLu7I"
params = {"ticker": "VALE3", "data_ini": "2001-01-01", "data_fim": "2026-12-31"}
response = requests.get(
    f"{base_url}/preco/corrigido",
    headers={"Authorization": f"Bearer {token}"},
    params=params,
)
dados= response.json()
df = pd.DataFrame(dados)
preco_ini = float(df[df["data"]=="2025-01-02"]["fechamento"].iloc[0])
preco_fim = float(df[df["data"]=="2025-12-30"]["fechamento"].iloc[0])
rendimento = preco_fim / preco_ini - 1
#Resposta:
print(rendimento)
# (1,5) 10 - Você tem acesso à API do Laboratório de Finanças, que fornece dados do Planilhão em formato JSON. 
# Selecione a empresa do setor de "tecnologia" que apresenta o maior ROE (Return on Equity) na data base 2024-04-01.
base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2OTQyMDE1LCJpYXQiOjE3NzQzNTAwMTUsImp0aSI6ImI3M2UyZGUyMmNkYTQ1ZWQ5ZmI2ZWZhYTAwZGM4N2I3IiwidXNlcl9pZCI6IjExNSJ9.BYwtttiHVt8EVA_653elnaGNcPAHdaWjlc9pusQLu7I"
response = requests.get(
    f"{base_url}/bolsa/planilhao",
    headers={"Authorization": f"Bearer {token}"},
    params={"data_base": "2024-04-01"},
)
dados= response.json()
df = pd.DataFrame(dados)
# Exiba APENAS AS COLUNAS "ticker", "setor" e o "roe"
selecao = df.loc[:, ["ticker", "setor", "roe"]]
setor_tecnologia = selecao.loc[selecao["setor"] == "tecnologia"]
roe_maximo = setor_tecnologia['roe'].max()
#Resposta:
print(roe_maximo)

# (1,5) 11 - Faça a Magic Formula através dos indicadores Return on Capital (roc) e Earning Yield (ey) no dia 2024-04-01.
# Monte uma carteira de investimento com 10 ações baseado na estratégia Magic Formula.
base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2OTQyMDE1LCJpYXQiOjE3NzQzNTAwMTUsImp0aSI6ImI3M2UyZGUyMmNkYTQ1ZWQ5ZmI2ZWZhYTAwZGM4N2I3IiwidXNlcl9pZCI6IjExNSJ9.BYwtttiHVt8EVA_653elnaGNcPAHdaWjlc9pusQLu7I"
response = requests.get(
    f"{base_url}/bolsa/planilhao",
    headers={"Authorization": f"Bearer {token}"},
    params={"data_base": "2024-04-01"},
)
dados= response.json()
df = pd.DataFrame(dados)
df2 = df[["ticker","setor", "roic","earning_yield"]]
df2["rank_roic"] = df2["roic"].rank()
df2["rank_earning_yield"] = df2["earning_yield"].rank()
df2["rank_final"] = (df2["rank_roic"] + df2["rank_earning_yield"] ) / 2
df3 = df2.sort_values("rank_final", ascending=True)
carteira = df3.head(10)
print(carteira["ticker"].tolist())
#Resposta
# (1,5) 12 - Quantos setores ("setor") tem essa carteira formada por 10 ações?
print(carteira["setor"].nunique())
# Se quiser saber quais os nomes do setores
print(carteira["setor"].unique().tolist())
