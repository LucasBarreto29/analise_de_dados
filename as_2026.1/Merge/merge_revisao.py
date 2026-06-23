import pandas as pd

# =============================================================================
# EXERCÍCIO DE REVISÃO — MERGE COM PANDAS
# Professor: escreva suas respostas onde indicado e rode o arquivo para testar.
# Pode chamar o professor a qualquer momento se tiver dúvidas!
# =============================================================================


# =============================================================================
# PARTE 1 — Entendendo os tipos de join (responda nos comentários abaixo)
# =============================================================================

# Considere as tabelas:
#
#   df_petroleo:                  df_dolar:
#   data       | preco            data       | cotacao
#   -----------|--------          -----------|---------
#   2024-01-02 | 75.3             2024-01-02 | 4.85
#   2024-01-03 | 76.1             2024-01-03 | 4.90
#   2024-01-04 | 74.8             2024-01-05 | 4.88
#   2024-01-05 | 73.2
#
# Obs: 2024-01-04 só existe no df_petroleo. 2024-01-05 existe nos dois.

# Questão 1a) Quantas linhas teria o resultado com how="inner"? Quais datas apareceriam?
# Sua resposta: Teria apenas três linhas e as datas que apareceriam seriam 2024-01-02, 2024-01-03 e 2024-01-5

# Questão 1b) Com how="left"? O que aconteceria com o dia 2024-01-04?
# Sua resposta: Ele estaria presente no resultado final, mas o valor para o dolar seria nulo

# Questão 1c) Com how="right"? O que mudaria?
# Sua resposta: O df voltaria a ter tres linhas e as datas do dolar seriam preservadas 


# =============================================================================
# PARTE 2 — Colocando a mão na massa
# =============================================================================

# Crie os dois DataFrames manualmente conforme a tabela acima
df_petroleo = pd.DataFrame({
    "data": pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]),
    "preco": [75.3, 76.1, 74.8, 73.2]
})

df_dolar = pd.DataFrame({
    "data": pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-05"]),
    "cotacao": [4.85, 4.90, 4.88]
})

# Questão 2a) Faça um merge inner entre df_petroleo e df_dolar pela coluna "data"
#             e salve em uma variável chamada df_inner. Imprima o resultado.
# Seu código:
df_inner = pd.merge(df_petroleo, df_dolar, on="data", how="inner")
print(df_inner)

# Questão 2b) Faça um merge left e salve em df_left. Imprima o resultado.
#             O que aparece na linha do dia 2024-01-04?
# Seu código:
df_left = pd.merge(df_petroleo, df_dolar, on="data", how="left")
print(df_left) # O df_dolar não possui as informações da data 2024-01-04, então ele aparece como NaN

# Questão 2c) Existe algum valor faltante no df_left? Use um método do pandas para verificar.
# Seu código:
print(df_left.isnull().sum()) # existe um valor nulo no df_left, na coluna cotacao


# =============================================================================
# PARTE 3 — Simulando o mundo real (igual ao Merge_df.py)
# =============================================================================

# Contexto: você quer montar uma base com TODOS os dias úteis de jan/2024,
# e cruzar com os preços disponíveis de petróleo e dólar.
# Nem todo dia útil tem cotação (feriados, ausência de dado, etc).

# Questão 3a) Crie um DataFrame chamado df_base com todos os dias úteis de
#             01/01/2024 até 31/01/2024. Use pd.date_range com freq="B".
# Dica: freq="B" = Business days (dias úteis)
# Seu código:
datas = pd.date_range(start="2024-01-01", end="2024-01-31", freq="B")
df_base = pd.DataFrame({"data": datas})

# Questão 3b) Faça um merge LEFT de df_base com df_petroleo pela coluna "data".
#             Por que usamos left aqui e não inner?
# Resposta nos comentários + código:
# A utilização do left aqui é feita porque nós queremos preservar as datas do df_base
df_base = pd.merge(df_base, df_petroleo, on="data", how="left")

# Questão 3c) Agora faça um segundo merge LEFT incorporando o df_dolar ao resultado anterior.
# Seu código:
df_base = pd.merge(df_base, df_dolar, on="data", how="left")
print(df_base)

# Questão 3d) Quantos valores faltantes existem em cada coluna? Use .isna().sum()
# Seu código:
print(df_base.isnull().sum())
# Há 19 valores nulos na coluna preço e 20 na coluna cotacao

# Questão 3e) DESAFIO: Preencha os valores faltantes usando forward fill (ffill).
#             Qual é a lógica econômica por trás dessa escolha?
# Resposta nos comentários + código:
# Lógica econômica: quando não há negociação num dia, assume-se o último preço conhecido
df_base = df_base.ffill()
