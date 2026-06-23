# =============================================================================
# NOTA METODOLÓGICA — CONSUMO DE APIs COM PYTHON
# Baseada no simulado treino_API_as.py
# =============================================================================

# -----------------------------------------------------------------------------
# 1. FLUXO PADRÃO DE CONSUMO DE UMA API
# -----------------------------------------------------------------------------
# Todo consumo de API segue a mesma sequência de 5 passos:
#
#   1. Definir a URL do endpoint
#   2. Fazer a requisição com requests.get()
#   3. Verificar o status (200 = OK)
#   4. Extrair os dados em JSON com response.json()
#   5. Transformar em DataFrame com pd.DataFrame()
#
# Exemplo mínimo:
#   url = "https://alguma-api.com/dados"
#   response = requests.get(url)
#   print(response.status_code)       # checar antes de continuar
#   dados = response.json()
#   df = pd.DataFrame(dados)


# -----------------------------------------------------------------------------
# 2. API PÚBLICA vs API COM AUTENTICAÇÃO
# -----------------------------------------------------------------------------
# API pública (ex: IPEA) — sem autenticação, acesso direto pela URL:
#   response = requests.get(url)
#
# API com autenticação (ex: Laboratório de Finanças) — exige token no header:
#   response = requests.get(
#       url,
#       headers={"Authorization": f"Bearer {TOKEN}"},
#       params={"ticker": "PETR4", ...},
#       verify=False   # necessário quando o certificado SSL do servidor está expirado
#   )
#
# ATENÇÃO — headers vs params:
#   headers → vai no cabeçalho da requisição, invisível na URL.
#             Usado para autenticação (token, chave de API).
#   params  → vira ?chave=valor no final da URL.
#             Usado para filtros (ticker, datas, data_base).


# -----------------------------------------------------------------------------
# 3. A CHAVE "value" DO IPEA (PROTOCOLO OData4)
# -----------------------------------------------------------------------------
# O IPEA usa o protocolo OData4, que sempre envolve os dados numa chave "value".
# Por isso, ao trabalhar com IPEA, o passo 4 sempre é:
#   dados = response.json()["value"]   # ← obrigatório para o IPEA
#
# Outras APIs (ex: Lab de Finanças) retornam a lista direto, sem chave:
#   dados = response.json()            # ← sem ["value"]
#
# REGRA: inspecione o retorno antes de assumir.
#   print(response.json())        # ver estrutura completa
#   print(response.json().keys()) # ver chaves do nível raiz


# -----------------------------------------------------------------------------
# 4. str.contains vs ==
# -----------------------------------------------------------------------------
# Use == quando souber o valor exato:
#   df[df["FNTSIGLA"] == "Fipe"]
#
# Use str.contains quando o valor pode aparecer em qualquer parte da string
# ou quando não sabe a grafia exata (equivalente ao LIKE do SQL):
#   df[df["SERNOME"].str.contains("inflação", case=False)]
#
# O parâmetro case=False ignora diferença entre maiúsculas e minúsculas.
# ATENÇÃO: str.contains exige o ponto antes de str — sem ele dá SyntaxError:
#   ERRADO: df["coluna"]str.contains(...)
#   CERTO:  df["coluna"].str.contains(...)


# -----------------------------------------------------------------------------
# 5. ENCONTRAR O VALOR MÁXIMO E A LINHA CORRESPONDENTE
# -----------------------------------------------------------------------------
# Duas formas equivalentes — escolha conforme o contexto:
#
# Forma 1 — padrão da prova (retorna todas as linhas empatadas no máximo):
#   df[df["VALVALOR"] == df["VALVALOR"].max()]
#
# Forma 2 — mais direta (retorna só a primeira linha com o máximo):
#   df.loc[df["VALVALOR"].idxmax()]
#
# ATENÇÃO: df["col"].max() retorna um número, não uma máscara booleana.
# Não é possível usá-lo diretamente como filtro:
#   ERRADO: df[df["VALVALOR"].max()]   # tenta usar um float como índice
#   CERTO:  df[df["VALVALOR"] == df["VALVALOR"].max()]


# -----------------------------------------------------------------------------
# 6. iloc — QUANDO E POR QUÊ É NECESSÁRIO
# -----------------------------------------------------------------------------
# Um filtro de DataFrame sempre retorna uma Series, mesmo que só haja uma linha.
# Para extrair o valor escalar (necessário para float(), int(), etc.),
# use iloc[0] para pegar o primeiro elemento:
#
#   preco = float(df[df["data"] == "2024-01-02"]["fechamento"].iloc[0])
#
# Sem iloc[0], o float() receberia uma Series e lançaria um erro.
#
# ATENÇÃO: iloc usa colchetes, não parênteses — é um indexador, não um método:
#   ERRADO: .iloc(0)
#   CERTO:  .iloc[0]
#
# iloc vs loc:
#   iloc → acessa por posição numérica (0, 1, 2...)
#   loc  → acessa por rótulo (nome do índice ou condição booleana)


# -----------------------------------------------------------------------------
# 7. BOAS PRÁTICAS OBSERVADAS NO SIMULADO
# -----------------------------------------------------------------------------
# - Defina TOKEN e BASE_URL uma única vez no topo do arquivo.
#   Evita redigitar e elimina risco de erro de digitação no token.
#
# - Sempre verifique o status antes de continuar:
#   print(response.status_code)   # 200 = OK, 401 = token inválido, 404 = endpoint errado
#
# - Ao usar uma variável de parâmetros (params, params2...), confirme
#   que está passando a variável correta na requisição — erro comum é
#   copiar o bloco e esquecer de atualizar o nome da variável.
#
# - Ao criar um DataFrame a partir de uma variável, nunca coloque aspas:
#   ERRADO: pd.DataFrame('dados')   # passa a string "dados"
#   CERTO:  pd.DataFrame(dados)     # passa o conteúdo da variável
