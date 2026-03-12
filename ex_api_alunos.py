"""
===========================================================
ATIVIDADE – CONSULTA DE DADOS VIA API
OBJETIVO:
- Consultar APIs públicas usando requests
- Entender estrutura JSON
- Transformar resposta em DataFrame
- Trabalhar com parâmetros e TOKENS
- Explorar dados externos
REGRAS:
- NÃO apagar os enunciados.
- Organizar o código.
- Comentar cada etapa importante.
- Mostrar os resultados com print() ou DataFrame.
===========================================================
"""
import requests
import pandas as pd
# ===========================================================
# PARTE 1 – INTRODUÇÃO
# ===========================================================
"""
O que é uma API?
API (Application Programming Interface) permite que um sistema
se comunique com outro.
Quando usamos requests.get(), estamos enviando uma requisição
HTTP para um servidor que retorna dados, geralmente em JSON.
Fluxo básico:
1. Definir URL
2. Enviar requisição
3. Verificar status_code
4. Converter para JSON
5. Transformar em DataFrame (quando necessário)
"""
# ===========================================================
# PARTE 2 – VIACEP (Consulta de CEP)
# ===========================================================
"""
Site: https://viacep.com.br/
Exemplo de consulta:
https://viacep.com.br/ws/01001000/json/

Exercícios:
1. Consulte um CEP da sua escolha.
2. Verifique o status da requisição.
3. Converta a resposta para JSON.
4. Transforme em DataFrame.
5. Mostre as principais informações.
"""
# RESOLVA AQUI:



# ===========================================================
# PARTE 3 – BRASILAPI
# ===========================================================
"""
Documentação:
https://brasilapi.com.br/docs
Exercícios:
1. Consulte a lista de bancos.
2. Transforme o resultado em DataFrame.
3. Conte quantos bancos existem.
4. Filtre bancos cujo nome contenha "Brasil".
Explique:
O que você percebe sobre a estrutura do JSON retornado?
"""
# RESOLVA AQUI:



# ===========================================================
# PARTE 4 – SERVIÇO DE DADOS IBGE
# ===========================================================
"""
Documentação:
https://servicodados.ibge.gov.br/api/docs/
Exercícios:
1. Consulte os estados brasileiros.
2. Transforme em DataFrame.
3. Mostre apenas:
   - nome
   - sigla
   - região
4. Pesquise como consultar dados de população.
Desafio:
Consultar a população total de um estado específico.
"""
# RESOLVA AQUI:



# ===========================================================
# PARTE 5 – IPEA DATA
# ===========================================================
"""
Documentação:
https://www.ipeadata.gov.br/api/
Exercícios:
1. Consulte os metadados de uma série.
2. Identifique:
   - nome da série
   - descrição
   - unidade
3. Consulte os valores históricos da série.
4. Transforme em DataFrame.
"""
# RESOLVA AQUI:



# ===========================================================
# PARTE 6 – BANCO CENTRAL DO BRASIL (BCB)
# ===========================================================
"""
Dados Abertos BCB:
https://dadosabertos.bcb.gov.br/
Exemplo: Consulta PTAX
Parâmetros:
{
 "formato": "json",
 "dataInicial": "01/01/2024",
 "dataFinal": "31/12/2024"
}
Exercícios:
1. Consulte a cotação do dólar em 2024.
2. Transforme em DataFrame.
3. Calcule:
   - média
   - valor máximo
   - valor mínimo
4. Plote gráfico de linha.
"""
# RESOLVA AQUI:



# ===========================================================
# PARTE 7 – FOOTBALL-DATA.ORG
# ===========================================================
"""
Documentação:
https://www.football-data.org/documentation/quickstart
Observação:
Essa API exige API-KEY.
Exercícios:
1. Consulte as áreas (countries).
2. Filtre o Brasil (CountryCode = "BRA").
3. Consulte competições do Brasil.
4. Consulte os times da temporada 2025.
Explique:
O que são parâmetros de consulta?
"""
# RESOLVA AQUI:



# ===========================================================
# PARTE 8 – RAPIDAPI (EXEMPLOS)
# ===========================================================
"""
Exemplos:
Tripadvisor – SearchLocation
querystring = {"query":"brasilia"}
NBA – Estatísticas de jogadores
querystring = {"game":"8133"}
Exercícios:
1. Escolha uma API do RapidAPI.
2. Faça uma consulta.
3. Transforme a resposta em DataFrame.
4. Descreva a estrutura do JSON retornado.
Desafio:
Identifique níveis aninhados no JSON.
"""
# RESOLVA AQUI:



# ===========================================================
# PARTE 9 – EXPLORAÇÃO LIVRE
# ===========================================================
"""
Pesquise APIs públicas em:
https://github.com/public-apis/public-apis
https://apilayer.com/marketplace
https://app.balldontlie.io/
Exercícios:
1. Escolha uma API pública.
2. Consulte dados.
3. Transforme em DataFrame.
4. Faça uma pequena análise exploratória.
"""
# RESOLVA AQUI:



# ===========================================================
# Revisão FINAL
# ===========================================================
"""
Responda:

1. O que é uma API?
2. O que é um endpoint?
3. O que são parâmetros?
4. O que é JSON?
5. O que é Headers?
6. O que é Token?
"""