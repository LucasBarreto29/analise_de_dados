# # Exercício 1: Criando um Dicionário
# Crie um dicionário chamado 'aluno' com as seguintes chaves:
#  'nome': contendo um nome fictício,
#  'idade': contendo a idade do aluno,
#  'curso': contendo o curso que ele está matriculado.
# Após criar o dicionário, exiba seus valores no seguinte formato:
# Nome: <nome>
# Idade: <idade>
# Curso: <curso>

aluno = {
    "nome": "Lucas Braga",
    "idade": 20,
    "curso": "Economia"
}

print(f"Nome: {aluno['nome']}")
print(f"Idade: {aluno['idade']}")
print(f"Curso: {aluno['curso']}")

# Exercício 2: Manipulação de Dicionário
# Dado o dicionário abaixo:
produto = {
     "nome": "Teclado Mecânico",
     "preco": 350.00,
     "estoque": 10
}
# 1. Adicione uma nova chave chamada 'marca' com um valor de sua escolha.
# 2. Atualize o preço do produto para R$ 320,00.
# 3. Reduza o estoque em 2 unidades.
# 4. Remova a chave 'marca' do dicionário.
# 5. Exiba o dicionário atualizado.

produto["marca"] = "Logitech"
produto["preco"] = 320.00
produto["estoque"] -= 2
del produto["marca"]
print(produto)

# Exercício 3: Iterando sobre um Dicionário
# Dado o dicionário:
notas = {
    "Alice": 8.5,
    "Bruno": 7.0,
    "Carla": 9.2,
    "Daniel": 6.8
}
# 1. Itere sobre o dicionário e exiba os nomes dos alunos e suas respectivas notas.
# 2. Calcule a média das notas e exiba o resultado.
total_notas = sum(notas.values())
media = total_notas / len(notas)
for aluno, nota in notas.items():
    print(f"{aluno}: {nota}")
print(f"Média das notas: {media:.2f}")


# Exercício 4: Soma de Valores
# Dado um dicionário com valores numéricos, percorra o dicionário e some todos os valores.
# Exemplo:
# numeros = {"a": 10, "b": 20, "c": 30}
# Saída esperada: 60

numeros = {"a": 10, "b": 20, "c": 30}
soma = sum(numeros.values())
print(f"Soma dos valores: {soma}")

# Exercício 5: Contagem de Itens Repetidos
# Dado uma lista de elementos, conte a frequência de cada elemento utilizando um dicionário.
# Exemplo:
# lista = ["maçã", "banana", "laranja", "maçã", "banana", "maçã"]
# Saída esperada: {'maçã': 3, 'banana': 2, 'laranja': 1}

lista = ["maçã", "banana", "laranja", "maçã", "banana", "maçã"]
frequencia = {}
for item in lista:
    if item in frequencia:
        frequencia[item] += 1
    else:
        frequencia[item] = 1
print(f"Frequência dos itens: {frequencia}")

# Exercício 6: Filtrando Dicionário
# Dado um dicionário contendo produtos e seus preços, filtre os produtos que custam mais de R$ 50,00.
# Exemplo:
# produtos = {"caneta": 10, "mochila": 80, "caderno": 45, "notebook": 3000}
# Saída esperada: {"mochila": 80, "notebook": 3000}

produtos = {"caneta": 10, "mochila": 80, "caderno": 45, "notebook": 3000}
produtos_filtrados = {produto: preco for produto, preco in produtos.items() if preco > 50}
print(f"Produtos que custam mais de R$ 50,00: {produtos_filtrados}")

# Exercício 7: Tradutor Simples
# Crie um dicionário chamado 'tradutor' que contém algumas palavras em inglês como chaves e suas traduções para português como valores.
# Peça ao usuário para digitar uma palavra em inglês e exiba sua tradução, caso exista no dicionário.
# Se a palavra não estiver cadastrada, exiba "Palavra não encontrada".

tradutor = {
    "hello": "olá",
    "world": "mundo",
    "cat": "gato",
    "dog": "cachorro",
    "book": "livro"
}
palavra_ingles = input("Digite uma palavra em inglês: ").lower()
traducao = tradutor.get(palavra_ingles, "Palavra não encontrada")
print(f"Tradução: {traducao}")

# Exercício 8: Lista de Compras
# Crie um dicionário onde as chaves são nomes de produtos e os valores são quantidades.
# Permita ao usuário adicionar produtos, atualizar quantidades e remover itens.
# No final, exiba a lista completa de compras.

lista_compras = {}
while True:
    acao = input("Digite 'adicionar', 'atualizar', 'remover' ou 'sair': ").lower()
    if acao == 'sair':
        break
    elif acao == 'adicionar':
        produto = input("Digite o nome do produto: ")
        quantidade = int(input("Digite a quantidade: "))
        lista_compras[produto] = quantidade
    elif acao == 'atualizar':
        produto = input("Digite o nome do produto a atualizar: ")
        if produto in lista_compras:
            quantidade = int(input("Digite a nova quantidade: "))
            lista_compras[produto] = quantidade
        else:
            print("Produto não encontrado.")
    elif acao == 'remover':
        produto = input("Digite o nome do produto a remover: ")
        if produto in lista_compras:
            del lista_compras[produto]
        else:
            print("Produto não encontrado.")
    else:
        print("Ação inválida. Tente novamente.")

# Exercício 9: Dicionário Aninhado
# Crie um dicionário chamado 'turma' onde as chaves são nomes de alunos e os valores são dicionários contendo:
# - "idade" (inteiro),
# - "notas" (lista de três notas).
# Exemplo de estrutura:
# turma = {
#     "Ana": {"idade": 17, "notas": [8, 9, 7]},
#     "Pedro": {"idade": 18, "notas": [6, 7, 8]},
#     "Mariana": {"idade": 17, "notas": [9, 10, 8]}
# }
# 1. Adicione um novo aluno ao dicionário.
# 2. Calcule a média de notas de cada aluno e exiba no formato:
#    Ana: Média 8.0
#    Pedro: Média 7.0
#    Mariana: Média 9.0
# 3. Encontre o aluno com a maior média e exiba o nome dele.

turma = {
    "Ana": {"idade": 17, "notas": [8, 9, 7]},
    "Pedro": {"idade": 18, "notas": [6, 7, 8]},
    "Mariana": {"idade": 17, "notas": [9, 10, 8]}
}
# Adicionando um novo aluno
turma["Lucas"] = {"idade": 20, "notas": [7, 8, 9]}

# Calculando a média de notas de cada aluno
medias = {}
for aluno, dados in turma.items():
    media = sum(dados["notas"]) / len(dados["notas"])
    medias[aluno] = media
    print(f"{aluno}: Média {media:.1f}")

# Encontrando o aluno com a maior média
melhor_aluno = max(medias, key=medias.get)
print(f"Aluno com a maior média: {melhor_aluno} ({medias[melhor_aluno]:.1f})")

# Exercício 10: Cadastro de Funcionários
# Crie um programa que permita cadastrar funcionários em uma empresa.
# O programa deve permitir adicionar funcionários com os seguintes dados:
# - Nome
# - Cargo
# - Salário
# Os funcionários devem ser armazenados em um dicionário onde a chave é o nome e o valor é outro dicionário com os dados do funcionário.
# O programa deve permitir consultar funcionários pelo nome e exibir suas informações.

funcionarios = {}
while True:
    acao = input("Digite 'adicionar', 'consultar' ou 'sair': ").lower()
    if acao == 'sair':
        break
    elif acao == 'adicionar':
        nome = input("Digite o nome do funcionário: ")
        cargo = input("Digite o cargo do funcionário: ")
        salario = float(input("Digite o salário do funcionário: "))
        funcionarios[nome] = {"cargo": cargo, "salário": salario}
    elif acao == 'consultar':
        nome = input("Digite o nome do funcionário a consultar: ")
        if nome in funcionarios:
            info = funcionarios[nome]
            print(f"Nome: {nome}, Cargo: {info['cargo']}, Salário: R$ {info['salário']:.2f}")
        else:
            print("Funcionário não encontrado.")
    else:
        print("Ação inválida. Tente novamente.")

