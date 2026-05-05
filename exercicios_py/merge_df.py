import requests
import pandas as pd

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgwNTcxMDUxLCJpYXQiOjE3Nzc5NzkwNTEsImp0aSI6IjZhNGQxOGUyODA2OTQ2NGE5ZGQzNDBlZDI3NDNiMmQxIiwidXNlcl9pZCI6IjEwNyJ9.BuMpADCf5YFdepxv9iyXIgmWgWdonPtLrk8b_fWevWM"
params = {"ticker": "ibov", "data_ini": "2000-01-01", "data_fim": "2025-12-31"}
resp = requests.get(
    f"{base_url}/preco/diversos",
    headers={"Authorization": f"Bearer {token}"},
    params=params,
)
dados = resp.json()
ibov = pd.DataFrame(dados)

#Dolar
params_dolar = {"ticker": "usd_brl", "data_ini": "2000-01-01", "data_fim": "2025-12-31"}
resp_dolar = requests.get(
    f"{base_url}/preco/diversos",
    headers={"Authorization": f"Bearer {token}"},
    params=params_dolar,
)
dados_dolar = resp_dolar.json()
dolar = pd.DataFrame(dados_dolar)

# Garantir que os campos sejam do tipo Datatime
ibov["data"] = pd.to_datetime(ibov["data"])
dolar["data"] = pd.to_datetime(dolar["data"])
# Selecionar apenas o preço de fechamento
ibov = ibov[["data", "fechamento"]]
dolar = dolar[["data", "fechamento"]]
# Renomeia as colunas
ibov = ibov.rename(columns={"fechamento":"ibov"})
dolar = dolar.rename(columns={"fechamento":"dolar"})
# Transforma em float
ibov["ibov"] = ibov["ibov"].astype(float)
dolar["dolar"] = dolar["dolar"].astype(float)
# Merge entre os dois df através do campo data
df = pd.merge(ibov, dolar, on="data", how="inner")
# Correlação
df[["ibov","dolar"]].corr()

# Datas
datas = pd.date_range("2000-01-01", "2025-12-31", freq="B")
df_base = pd.DataFrame({"data":datas})
df_base = pd.merge(df_base, ibov, on= "data", how="left")
df_base = pd.merge(df_base, dolar, on= "data", how="left")
# Tratamento de dados faltantes
df_base.isna().sum()
df_base.dropna()
df_base.ffill() # forward fill
df_base.bfill() # backward fill
#
df["ret_ibov"] = df["ibov"].pct_change()
df["ret_dolar"] = df["dolar"].pct_change()

# Correlação
import seaborn as sn
corr = df[["ret_ibov", "ret_dolar"]].corr()
sn.heatmap(corr, annot=True)
# Histograma
sn.histplot(df["ret_ibov"], kde=True)
# Boxplot
sn.boxplot(df["ret_ibov"])
# Lineplot
sn.lineplot(df["ret_ibov"])
