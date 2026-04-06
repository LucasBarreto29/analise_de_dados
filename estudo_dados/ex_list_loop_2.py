# 1.

frutas = ["maçã", "banana", "laranja", "uva"]
print(frutas)

# 2.
print(frutas[0])
print(frutas[-1])
# 3.

frutas.append("manga")
print(frutas)

# 4.

frutas.remove("banana")
print(frutas)

# 5.

frutas[1] = "abacaxi"
print(frutas)

# 6.

numeros = list(range(1,11))
print(numeros)

# 7.

soma_numeros = sum(numeros)
print(soma_numeros)

# 8.

maior_num = max(numeros)
print(maior_num)

menor_num = min(numeros)
print (menor_num)

# 9. 

numeros_invertidos = numeros[::-1]
print(numeros_invertidos)

# 10.

cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba"]

# 11.

cidades.sort()
print(cidades)

# 12.
cidades.append("Porto Alegre")
print(cidades)

# 13. 

indice = cidades.index("Curitiba")
print(indice)

# 14.

cidades.remove("Rio de Janeiro")
print(cidades)

# 15.

lista1 = [1, 2, 3]
lista2 = [4, 5, 6]

# 16.

lista3 = lista1 + lista2
print(lista3)

# 17.

print(lista3)

# 18.

animais_domesticos = ["cachorro", "gato", "coelho"]
animais_selvagens = ["leão", "tigre", "urso"]

# 19. 
todos_animais = animais_domesticos + animais_selvagens

# 20.
print(todos_animais)

# Looping com for

# 21. e 22. 

nomes = ["Ana", "Pedro", "Maria", "João"]
for nome in nomes:
    print(nome)

# 23.

nomes_maiusculos = []
for nome in nomes:
    nomes_maiusculos.append(nome.upper())
print(nomes_maiusculos)

# 24.
numeros2 = list(range(1,21))
for pares in numeros2:
    if pares % 2 == 0:
        print(pares)

# 25.

quadrados = []

for num in numeros2:
    quadrados.append(num ** 2)
print(quadrados)

# 26.

linguagem = ["python", "java", "c", "javascript"]
for tamanho in linguagem:
    print(tamanho, len(tamanho))

# 27.
idade = [12, 18, 25, 40, 60]
for id in idade:
    if id >= 18:
        print(id, "Maior de Idade")
    else:
        print(id, "Menor de idade")


# 28.
notas = [5.5, 7.0, 8.3, 4.9, 6.2]
for resultado in notas:
    if resultado >= 7:
        print(resultado, "Aprovado")
    else:
        print(resultado, "Reprovado")

# 29. 
lista_compras = ["arroz", "feijão", "batata", "carne"]
for produtos in lista_compras:
    print("Preciso comprar", produtos)

# Looping usando While

# 30.
i = 1
while i <= 10:
    print(i)
    i += 1

# 31.
while True:
    num = int(input("Digite um número:"))
    if num == 0:
        print("Programa Encerrado")
        break
    print("Você digitou: ", num)

# 32. 
soma = 0
i = 1
while i <= 100:
    soma += i
    i += 1
print("A soma de 1-100 é: ", soma)

# Teste com lista
lista100 = list(range(1,101))
print(sum(lista100))

# 33.
secreto = 33
while True:
    palpite = int(input("Qual é o seu palpite?"))
    if palpite == secreto:
        print("Parabéns! Você acertou!")
        break
    else:
        print("Tente novamente")

# 34.
i = 2
while i <= 20:
    print(i)
    i += 2