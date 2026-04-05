# Criando um dicionário - Exercício 1
aluno = {
    'nome': 'Lucas',
    'idade': 20,
    'curso': 'Economia'
}
print(aluno)

# Para utilizar o formato correto preciso utilizar as f-strings do python para
# que seja possível utilizar as variáveis dentro do próprio texto

print(f"Nome: {aluno['nome']}")
print(f"Idade: {aluno['idade']}")
print(f"Curso: {aluno['curso']}")

# Exercício 2 - Manipulação de Dicionário

produto = {
    "nome": "Teclado Mecânico",
    "preco": 350.00,
    "estoque": 10
}

# Adicionando a marca no dicionário
# Atualizando o valor do prduto
# Reduzindo o valor do estoque
# Metódo: alterando a estrutura diretamente

produto = {
    "nome": "Teclado Mecânico",
    "preco": 320.00,
    "estoque": 8,
    "marca": "Redgragon"
}

print(produto)

# Criando um novo dicionário e mutando

produto_2 = {
    'nome': 'Mouse Wireless',
    'preco': 250.00,
    'estoque': 25
}

# Adicionando marca
# Atualizando preço
# Reduzindo estoque

produto_2['marca'] = 'Redragon'
produto_2['preco'] = 220.00
produto_2['estoque'] -= 2
print(produto_2) 

# Removendo 'Marca'

del produto_2['marca']

print(produto_2)

# Exibindo

print(f"Nome: {produto_2['nome']}")
print(f"Preço: {produto_2['preco']}")
print(f"Estoque: {produto_2['estoque']}")

# Exercicio 3 - Iterando sobre um dicionário

notas = {
    "Alice": 8.5,
    "Bruno": 7.0,
    "Carla": 9.2,
    "Daniel": 6.8
}

# Iterando sobre o dicionário
# Para passar por cada item deste dicionário e exibi-lo, preciso utilizar um loop for
for nome, nota in notas.items():
    print(f"Nome: {nome} - Nota: {nota}")

# Calculando a média das notas e exibindo o resultado
notas_soma = sum(notas.values())
qtd_aluno = len(notas)

media = notas_soma/qtd_aluno
print(f"A média das notas da classe é: {media:.2f}")

# Exercício 4 - Soma de valores

numeros = {
    "a": 10, "b": 20, "c": 30
    }

soma_numeros = sum(numeros.values())
print(soma_numeros)

# Exercício 5 - Contagem de Itens Repetidos

lista = ["maçã", "banana", "laranja", "maçã", "banana", "maçã"]

# A primeira coisa a se fazer é criar um dicionário vazio para começar a contagem

contagem ={}

for fruta in lista:
    if fruta in contagem:
        contagem[fruta] += 1
    else:
        contagem[fruta] = 1
print(contagem)    

# Exercício 6 - Filtrando Dicionário

produtos_3 = {"caneta": 10, "mochila": 80, "caderno": 45, "notebook": 3000}

# filtrando os produtos que custam mais que R$ 50
# Preciso criar um novo dicionário para armazenar os dados

produtos_filtrados = {}

# Criando um loop para fazer a avaliação
for item, preco in produtos_3.items():
    if preco > 50:
        produtos_filtrados[item] = preco
print(produtos_filtrados)

# Exercício 7 - Tradutor Simples

tradutor = {
    'book': 'livro',
    'keyboard': 'teclado',
    'list': 'lista',
    'country': 'pais'
}

palavra = input("Digite uma palavra em inglês: ").lower()

traducao = tradutor.get(palavra, "Palavra nao encontrada")

print(f"Tradução: {traducao}")