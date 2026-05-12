import seaborn as sns
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

df = sns.load_dataset("tips")
df.info()

# Regressão linear simples
# X = total_bill
# Y = tip
x = df['total_bill']
y = df['tip']
# Adiciona o interecepto
x = sm.add_constant(x)
modelo = sm.OLS(y,x).fit()
print(modelo.summary())
# plot
sns.lmplot(data=df, x="total_bill", y="tip")
modelo.params
modelo.pvalues
modelo.df_model
modelo.rsquared
# Regressão linear múltipla

x = df[['total_bill', 'size']]
y = df['tip']
# Adiciona o interecepto
x = sm.add_constant(x)
modelo = sm.OLS(y,x).fit()
print(modelo.summary())
df['tip'] - modelo.predict() # Distância exata entre a linha e o observado

from statsmodels.tsa.ar_model import AutoReg
import requests
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
x = ibov['fechamento'].astype("float")
# Modelo AR - Autorregressivo para séries temporais
modelo = AutoReg(x, lags=2).fit()
print(modelo.summary())
