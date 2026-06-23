# =============================================================================
# NOTA METODOLÓGICA — MERGE DE DataFrames COM PANDAS
# Baseada no arquivo Merge_df.py
# =============================================================================


# -----------------------------------------------------------------------------
# 1. O QUE É O MERGE E QUANDO USAR
# -----------------------------------------------------------------------------
# O merge é a operação de unir dois DataFrames com base em uma coluna em comum.
# É equivalente ao JOIN do SQL.
#
# Use merge quando:
#   - Dois DataFrames compartilham uma coluna (ex: "data", "código", "id")
#   - Você quer cruzar as informações dessas duas fontes numa única tabela
#
# Sintaxe padrão:
#   df = pd.merge(df_esquerda, df_direita, on="coluna_chave", how="tipo")


# -----------------------------------------------------------------------------
# 2. TIPOS DE JOIN — how=
# -----------------------------------------------------------------------------
# O parâmetro how define quais linhas são mantidas no resultado:
#
#   how="inner"  → apenas as linhas com chave em AMBOS os DataFrames
#                  Linhas sem correspondência são descartadas.
#
#   how="left"   → TODAS as linhas do DataFrame da esquerda são mantidas.
#                  Se não houver correspondência no da direita, aparece NaN.
#
#   how="right"  → TODAS as linhas do DataFrame da direita são mantidas.
#                  Se não houver correspondência no da esquerda, aparece NaN.
#
#   how="outer"  → TODAS as linhas de AMBOS os DataFrames são mantidas.
#                  NaN onde não houver correspondência em qualquer lado.
#
# Resumo visual (A = esquerda, B = direita):
#   inner  → A ∩ B   (interseção)
#   left   → A inteiro + o que bater em B
#   right  → B inteiro + o que bater em A
#   outer  → A ∪ B   (união)


# -----------------------------------------------------------------------------
# 3. PRÉ-PROCESSAMENTO ANTES DO MERGE — ETAPA OBRIGATÓRIA
# -----------------------------------------------------------------------------
# Antes de fazer o merge, é preciso garantir que as colunas estejam
# no formato correto. O fluxo padrão observado na aula é:
#
#   1. Converter a coluna-chave para o tipo correto (ex: datetime):
#      df["data"] = pd.to_datetime(df["data"])
#      ↳ Dados vindos de APIs chegam como string. Se os tipos forem diferentes
#        entre os dois DataFrames, o pandas não reconhece as chaves como iguais.
#
#   2. Selecionar apenas as colunas necessárias:
#      df = df[["data", "fechamento"]]
#      ↳ Descarta colunas desnecessárias antes de unir.
#
#   3. Renomear colunas com nomes repetidos:
#      df.rename(columns={"fechamento": "ibov"})
#      ↳ Se os dois DataFrames tiverem uma coluna com o mesmo nome,
#        o pandas criaria "fechamento_x" e "fechamento_y" — confuso.
#        Renomear antes resolve isso.
#
#   4. Converter colunas numéricas para float:
#      df["ibov"] = df["ibov"].astype(float)
#      ↳ Valores numéricos também podem chegar como string via API.


# -----------------------------------------------------------------------------
# 4. PADRÃO DE BASE COMPLETA DE DATAS (left com âncora)
# -----------------------------------------------------------------------------
# Quando o objetivo é ter uma série contínua (sem lacunas de dias),
# o padrão é criar um DataFrame âncora com todos os dias do período
# e usar merges left para incorporar os dados:
#
#   datas = pd.date_range(start="2000-01-01", end="2025-12-31", freq="B")
#   df_base = pd.DataFrame({"data": datas})          # âncora com todos os dias úteis
#   df_base = pd.merge(df_base, ibov,  on="data", how="left")  # incorpora ibov
#   df_base = pd.merge(df_base, dolar, on="data", how="left")  # incorpora dolar
#
# Por que left e não inner?
#   O inner descartaria os dias sem cotação. O left preserva todos os dias
#   do df_base (a âncora) e preenche com NaN onde não há dado — permitindo
#   tratar as ausências depois com ffill, bfill ou dropna.
#
# freq="B" — Business days: gera apenas dias úteis (segunda a sexta).
# Não confundir com freq="D", que inclui finais de semana.


# -----------------------------------------------------------------------------
# 5. TRATAMENTO DE VALORES FALTANTES APÓS O MERGE
# -----------------------------------------------------------------------------
# Após um merge left/right/outer, é comum surgir NaN. As opções são:
#
#   df.isna().sum()   → conta os NaN por coluna (diagnóstico)
#   df.dropna()       → remove as linhas com NaN
#   df.ffill()        → forward fill: preenche com o último valor anterior
#   df.bfill()        → backward fill: preenche com o próximo valor seguinte
#
# ATENÇÃO: esses métodos NÃO alteram o DataFrame original.
# Sempre atribua o resultado de volta:
#   ERRADO: df.ffill()
#   CERTO:  df = df.ffill()
#
# Qual usar em séries financeiras?
#   ffill é o padrão — se não houve negociação hoje, o preço válido
#   é o último preço conhecido (ontem, ou o último dia útil anterior).


# -----------------------------------------------------------------------------
# 6. ANÁLISE PÓS-MERGE — RETORNOS E CORRELAÇÃO
# -----------------------------------------------------------------------------
# Com os dados unidos, o fluxo de análise padrão é:
#
#   # Calcular retorno percentual diário
#   df["ret_ibov"]  = df["ibov"].pct_change()
#   df["ret_dolar"] = df["dolar"].pct_change()
#
#   # Correlação entre os retornos
#   corr = df[["ret_ibov", "ret_dolar"]].corr()
#   sn.heatmap(corr, annot=True)
#
# pct_change() calcula (valor_hoje - valor_ontem) / valor_ontem.
# Trabalha-se com retornos (e não preços) porque retornos são comparáveis
# entre ativos de escalas diferentes (ibov em pontos, dólar em reais).


# -----------------------------------------------------------------------------
# 7. ERROS COMUNS
# -----------------------------------------------------------------------------
# - Esquecer de converter a coluna-chave para datetime antes do merge:
#   resultado: merge vazio ou incorreto, pois "2024-01-02" (str) ≠ Timestamp
#
# - Não renomear colunas com nomes iguais antes do merge:
#   resultado: pandas cria "fechamento_x" e "fechamento_y" automaticamente
#
# - Não salvar o resultado do merge numa variável:
#   ERRADO: pd.merge(ibov, dolar, on="data", how="inner")
#   CERTO:  df = pd.merge(ibov, dolar, on="data", how="inner")
#
# - Não salvar o resultado de ffill/dropna/bfill:
#   ERRADO: df.ffill()
#   CERTO:  df = df.ffill()
