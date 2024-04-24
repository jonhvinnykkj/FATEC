# Comentário: Exercícios de fixação
import random
def ex1():
    nome = input("Digite seu nome: ")
    for i in range(0, 10):
        print(nome)

def ex2():
    num = 0
    while num <= 100:
        print(num)
        num = num + 1
        
    #diminuindo com for
    for i in range(100, -1, -1):
        print(i)

def ex3():
    numero1 = random.randint(0, 10)
    numero2 = random.randint(0, 10)
    while True:
        resposta = int(input(f"Quanto é {numero1} * {numero2}? "))
        if resposta != numero1 * numero2:
            print("Resposta incorreta! Tente novamente.")
        else: 
            print("Resposta correta!")
            break
def ex4():
    pergunta = int(input("Quantas medias deseja calcular? "))
    for i in range(0, pergunta):
        nota1 = float(input("Digite a primeira nota: "))
        nota2 = float(input("Digite a segunda nota: "))
        media = (nota1 + nota2) / 2
        print(f"A média do aluno é: {media}")
def ex5():
    while True:
        for i in range(0, 10):
            pergunta = int(input("Digite um numero: "))

        soma = 0
        for i in range(0, 10):
            if pergunta % 2 == 0:
                soma = soma + pergunta
        print(f"A soma dos pares é: {soma}")

        for i in range(0, 10):
            if pergunta % 2 != 0:
                soma = soma + pergunta
        print(f"A soma dos impares é: {soma}")
def ex6():
    maior = 0
    for i in range(0, 20):
        num = random.randint(0, 100)
        print(num)
        if num > maior:
            maior = num
    print(f"O maior número gerado foi: {maior}")

def ex7():
    for i in range(1000, 196, -3):
        print(i)
        