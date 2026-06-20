# Nota Técnica — Lista de Exercícios Pandas
### Ranking Mundial de Universidades | `notas.csv`

---

## 1. Objetivo da Lista

Essa lista tem como objetivo introduzir as principais ferramentas da biblioteca **Pandas** para quem está começando a trabalhar com análise de dados em Python. A proposta é passar por todas as etapas fundamentais de uma análise real:

1. **Conhecer o dado** — entender o que tem no dataset antes de qualquer análise
2. **Resumir numericamente** — calcular estatísticas básicas
3. **Filtrar e selecionar** — extrair partes específicas dos dados
4. **Tratar valores ausentes** — lidar com dados incompletos
5. **Agregar por categoria** — comparar grupos (países, anos)
6. **Visualizar** — transformar números em gráfico

Cada exercício representa uma fase real de um projeto de análise de dados. Quem consegue fazer essa lista com segurança já tem base para trabalhar com qualquer dataset tabular.

---

## 2. As Bibliotecas Utilizadas

### `pandas` — a planilha inteligente do Python

```python
import pandas as pd
```

Pensa no Pandas como o Excel do Python, mas muito mais poderoso. Ele cria e manipula **DataFrames** — tabelas com linhas e colunas, exatamente como uma planilha. Com ele você carrega arquivos CSV, filtra linhas, calcula médias, agrupa por categoria e muito mais.

O `as pd` é só um apelido para não precisar digitar `pandas` toda hora — uma convenção universal.

---

### `matplotlib.pyplot` — o papel milimetrado do Python

```python
import matplotlib.pyplot as plt
```

É a biblioteca de visualização mais clássica do Python. Ela transforma seus dados em gráficos. O `pyplot` é o módulo específico que tem as funções de plotagem (linha, barra, dispersão, etc.). Usamos `as plt` pelo mesmo motivo: é um apelido para facilitar.

---

## 3. Funções Utilizadas

### `pd.read_csv()`

```python
df = pd.read_csv('notas.csv')
```

**O que faz:** Lê um arquivo `.csv` e transforma em um DataFrame.

**Quando usar:** Sempre que você tiver um arquivo de dados separado por vírgulas (ou ponto-e-vírgula) e quiser carregá-lo no Python.

**Analogia:** É como abrir um arquivo no Excel — a diferença é que aqui você dá um nome para a tabela (`df`) e passa a trabalhar com ela pelo código.

---

### `.shape`

```python
linhas, colunas = df.shape
```

**O que faz:** Retorna uma dupla de números `(linhas, colunas)` com o tamanho do DataFrame.

**Quando usar:** Logo no início de qualquer análise, para saber com o que você está lidando.

> **Atenção semântica:** O enunciado pergunta *"quantas linhas e colunas existem"*. Se perguntasse só *"qual o tamanho do dataset"*, usar `df.shape` direto sem desempacotar já responderia. A forma de desempacotar (`linhas, colunas = df.shape`) só faz sentido quando você quer usar esses valores separadamente — como dentro de um `print` explicativo.

---

### `.dtypes`

```python
df.dtypes
```

**O que faz:** Mostra o tipo de dado de cada coluna (`int64`, `float64`, `object`).

**Quando usar:** Para entender se os dados estão no formato certo antes de operar sobre eles. Calcular a média de uma coluna que está como `object` (texto), por exemplo, vai dar erro.

**Analogia:** É como olhar o rótulo de cada gaveta antes de abrir — você sabe o que esperar dentro.

| Tipo | Significa |
|------|-----------|
| `int64` | Número inteiro |
| `float64` | Número decimal |
| `object` | Texto (string) |

---

### `.isnull().sum()`

```python
df.isnull().sum()
df['coluna'].isnull().sum()
```

**O que faz:** Conta quantos valores nulos (ausentes) existem. Quando aplicado ao DataFrame inteiro retorna uma contagem por coluna. Quando aplicado a uma coluna específica, retorna um único número.

**Quando usar:** Para identificar se há dados faltando antes de fazer qualquer cálculo — valores nulos podem distorcer médias e quebrar funções.

> **Atenção semântica:** O enunciado do exercício 1.3 pede *"existe coluna com valores ausentes?"* — a resposta ideal é `df.isnull().sum()` mostrando todas as colunas. Já o exercício 5.1 pede *"quantos valores nulos em broad_impact?"* — aí você isola a coluna: `df['broad_impact'].isnull().sum()`. Mesma função, escopo diferente.

---

### `.unique()` e `.nunique()`

```python
df['year'].unique()   # quais são os valores únicos
df['year'].nunique()  # quantos valores únicos existem
```

**O que faz:** `.unique()` retorna a lista de valores distintos. `.nunique()` retorna apenas a contagem.

**Quando usar:** Para entender a variedade de uma coluna categórica — anos disponíveis, países presentes, etc.

**Analogia:** Imagine uma lista de chamada com nomes repetidos. `.unique()` é como listar cada nome uma vez. `.nunique()` é como contar quantos alunos diferentes tem na turma.

> **Atenção semântica:** *"Qual o período de anos?"* pede `.unique()` (você quer ver os anos). *"Quantos anos?"* pede `.nunique()` (você quer o número). Mudar uma palavra no enunciado muda a função.

---

### `.mean()`, `.max()`, `.min()`, `.std()`

```python
df['score'].mean()  # média
df['score'].max()   # maior valor
df['score'].min()   # menor valor
df['score'].std()   # desvio padrão
```

**O que faz:** Estatísticas descritivas básicas de uma coluna numérica.

**Quando usar:** Para resumir numericamente um conjunto de dados — o coração do exercício 2.

| Função | Retorna | Pergunta que responde |
|--------|---------|----------------------|
| `.mean()` | Média aritmética | "Qual o valor típico?" |
| `.max()` | Maior valor | "Qual o teto?" |
| `.min()` | Menor valor | "Qual o piso?" |
| `.std()` | Desvio padrão | "Quão espalhados estão os dados?" |

> **Desvio padrão na prática:** Um desvio padrão alto significa que os dados variam muito em torno da média (universidades com scores muito diferentes entre si). Um desvio padrão baixo indica que os valores são parecidos.

---

### `.sort_values()`

```python
df.sort_values(by='world_rank', ascending=True)
```

**O que faz:** Ordena o DataFrame por uma coluna. `ascending=True` vai do menor para o maior; `ascending=False` vai do maior para o menor.

**Quando usar:** Quando você quer ver os dados em ordem — rankings, maiores valores, menores valores.

> **Atenção semântica — armadilha comum:** *"Melhores universidades"* significa **menor** `world_rank` (rank 1 é o melhor). Então `ascending=True` é o correto. Se você usar `ascending=False` você vai listar as **piores**. Leia o enunciado com atenção: *"menor rank = melhor posição"* é uma inversão de lógica que confunde muito iniciante.

---

### Filtro com colchetes `df[condição]`

```python
df[df['score'] > 90]
df[df['country'] == 'Brazil']
df[(df['country'] == 'USA') & (df['score'] > 80)]
```

**O que faz:** Seleciona apenas as linhas que satisfazem uma condição. Com `&` você combina dois filtros (ambos precisam ser verdadeiros).

**Quando usar:** Sempre que você quiser ver um subconjunto dos dados com base em algum critério.

**Analogia:** Pensa no filtro como um peneira. Você passa o DataFrame pela peneira e só ficam as linhas que atendem à condição. Com dois filtros (`&`), é como duas peneiras em sequência — só passa quem passa nas duas.

> **Atenção semântica:** *"Universidades entre rank 50 e 100"* filtra pela coluna `world_rank`. *"Universidades com score entre 50 e 100"* filtra pela coluna `score`. Troca uma palavra, troca a coluna — e o resultado é completamente diferente.

---

### Seleção de colunas `df[['col1', 'col2']]`

```python
df[['institution', 'country', 'score']]
```

**O que faz:** Retorna o DataFrame com apenas as colunas listadas.

**Quando usar:** Quando você quer simplificar a visualização ou trabalhar apenas com campos relevantes.

**Analogia:** É como esconder colunas no Excel — os dados continuam existindo, você só está escolhendo o que mostrar.

> O duplo colchete `[[ ]]` é intencional: o externo é o operador de seleção do DataFrame, o interno é a lista Python. Um erro comum é usar `df['institution', 'country']` com colchete simples — isso vai dar erro.

---

### `.head()` e `.nsmallest()`

```python
df.head(10)                        # primeiras 10 linhas
df.nsmallest(10, 'world_rank')     # 10 menores valores de world_rank
```

**O que faz:** `.head(n)` retorna as primeiras `n` linhas do DataFrame como está. `.nsmallest(n, coluna)` retorna as `n` linhas com os menores valores naquela coluna.

**Quando usar:** Use `.head()` quando o dado já está ordenado e você quer pegar os primeiros. Use `.nsmallest()` quando você quer os menores valores independentemente da ordem atual.

> Se você já ordenou com `.sort_values(ascending=True)`, usar `.head(10)` é equivalente a `.nsmallest(10, coluna)`. São dois caminhos para o mesmo resultado.

---

### `.dropna()` e `.fillna()`

```python
df_sem_nulos = df.dropna(subset=['broad_impact'])   # remove linhas com nulo
df['broad_impact'] = df['broad_impact'].fillna(media)  # preenche nulos
```

**O que faz:** `.dropna()` remove linhas que têm valores nulos. `.fillna()` substitui os nulos por um valor que você define (média, zero, etc.).

**Quando usar:**
- Use `.dropna()` quando as linhas com nulo são poucas e você prefere trabalhar com dados completos.
- Use `.fillna()` quando não quer perder linhas — preenche o buraco com um valor razoável.

**Analogia:** Imagine uma pesquisa onde alguns participantes não responderam a uma pergunta. `.dropna()` é como descartar os questionários incompletos. `.fillna()` é como escrever "média da turma" no espaço em branco antes de tabular os resultados.

> **Propriedade matemática importante:** Preencher nulos com a média **não altera a média** do conjunto. Por quê? Porque você está inserindo exatamente o valor médio — o centro de massa não se move. Por isso as médias antes e depois do `fillna(media)` são iguais.

---

### `.groupby()`

```python
df.groupby('country')['score'].mean()
df.groupby('year')['score'].mean()
```

**O que faz:** Agrupa o DataFrame por uma coluna e aplica uma função em cima de cada grupo. É a versão Python do "SOMASE" ou "MÉDIASE" do Excel.

**Quando usar:** Sempre que a pergunta tiver a estrutura *"por país"*, *"por ano"*, *"por categoria"* — qualquer cálculo segmentado.

**Analogia:** Imagina que você tem uma lista de notas de alunos de várias turmas misturadas. O `groupby('turma')` é como separar fisicamente as folhas de cada turma em pilhas diferentes. Depois você calcula a média de cada pilha separadamente.

> **Leitura do código:** `df.groupby('country')['score'].mean()` lê-se assim: *"Agrupe o DataFrame por país, pegue a coluna score de cada grupo, e calcule a média."* Sempre que ver `groupby`, leia como "para cada [categoria], calcule [operação]".

---

### `.idxmax()`

```python
score_por_pais.idxmax()
```

**O que faz:** Retorna o **índice** (rótulo) do maior valor de uma Series. Quando usada após um `groupby`, o índice é a categoria (país, ano, etc.).

**Quando usar:** Quando você quer saber **quem** tem o maior valor, não apenas **qual** é o maior valor.

> A diferença entre `.max()` e `.idxmax()`: `.max()` retorna o número (ex: `95.3`). `.idxmax()` retorna o nome (ex: `'Israel'`). A pergunta *"qual o maior score?"* pede `.max()`. A pergunta *"qual país tem o maior score?"* pede `.idxmax()`.

---

### `.plot()` com Matplotlib

```python
filtro_score_pais.plot(kind='line', marker='o', title='Evolução do Score Médio por Ano')
plt.xlabel('Ano')
plt.ylabel('Score Médio')
plt.tight_layout()
plt.show()
```

**O que faz:** Gera um gráfico diretamente de uma Series ou DataFrame do Pandas, usando o Matplotlib por baixo dos panos.

**Parâmetros principais:**

| Parâmetro | O que faz |
|-----------|-----------|
| `kind='line'` | Define o tipo de gráfico (linha, bar, hist...) |
| `marker='o'` | Coloca um ponto em cada dado |
| `title=` | Título do gráfico |
| `plt.xlabel()` | Rótulo do eixo X |
| `plt.ylabel()` | Rótulo do eixo Y |
| `plt.tight_layout()` | Ajusta o espaçamento para não cortar nada |
| `plt.show()` | Exibe o gráfico na tela |

---

## 4. Semântica: como o enunciado define a solução

Uma das habilidades mais importantes em análise de dados é **ler o enunciado com precisão**. Palavras diferentes implicam funções diferentes. Veja os exemplos desta lista:

| Enunciado | Função correta | Por quê |
|-----------|---------------|---------|
| "Quantos países **diferentes** existem?" | `.nunique()` | Quer o número de únicos |
| "Quais são os países presentes?" | `.unique()` | Quer a lista de únicos |
| "Mostre as 10 **melhores** (menor rank)" | `ascending=True` | Rank 1 = melhor |
| "Mostre as 10 **piores** (maior rank)" | `ascending=False` | Rank 1000 = pior |
| "Universidades entre **rank** 50 e 100" | Filtra `world_rank` | A coluna é rank |
| "Universidades entre **score** 50 e 100" | Filtra `score` | A coluna é score |
| "Qual país tem **maior média**?" | `.groupby().mean().idxmax()` | Quer o nome do país |
| "Qual é a **maior média**?" | `.groupby().mean().max()` | Quer o número |
| "**Remova** linhas nulas" | `.dropna()` | Elimina as linhas |
| "**Preencha** valores nulos" | `.fillna()` | Substitui o nulo |

---

## 5. Resumo Geral das Funções

| Função | Categoria | Para que serve |
|--------|-----------|---------------|
| `pd.read_csv()` | Carga | Ler arquivo CSV |
| `.shape` | EDA | Dimensões do DataFrame |
| `.dtypes` | EDA | Tipos de cada coluna |
| `.isnull().sum()` | EDA | Contar valores nulos |
| `.unique()` | EDA | Listar valores distintos |
| `.nunique()` | EDA | Contar valores distintos |
| `.mean()` | Estatística | Média |
| `.max()` / `.min()` | Estatística | Maior / Menor valor |
| `.std()` | Estatística | Desvio padrão |
| `df[condição]` | Filtro | Selecionar linhas |
| `df[['col1', 'col2']]` | Seleção | Selecionar colunas |
| `.sort_values()` | Ordenação | Ordenar por coluna |
| `.head()` | Visualização | Primeiras n linhas |
| `.nsmallest()` | Ordenação | n menores valores |
| `.dropna()` | Limpeza | Remover linhas nulas |
| `.fillna()` | Limpeza | Preencher nulos |
| `.groupby()` | Agregação | Agrupar e calcular |
| `.idxmax()` | Agregação | Índice do maior valor |
| `.plot()` | Visualização | Gerar gráfico |
