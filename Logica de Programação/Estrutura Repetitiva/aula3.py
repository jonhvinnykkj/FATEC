def ex01_seriefibonacci():
    n = int(input("Digite o valor de n: "))
    a = 0
    b = 1
    print(a,b, end=" ")
    for i in range(2, n):
        c = a + b
        print(c, end=" ")
        a,b = b,c

#Codigo seguindo as boas praticas de programação:
def soma_inteiros(num1, num2):
    if num1 < num2:
        print(f'O primeiro termo é menor que o segundo termo, então o intervalo de sequencia é de {num2 - num1}')
        return sum(range(num1+1, num2))
    else:
        print(f'O primeiro termo é maior que o segundo termo, então o intervalo de sequencia é de {num1 - num2}')
        return sum(range(num2+1, num1))

def soma_inteiros_continuar():
    while True:
        num1 = int(input("Digite o primeiro termo do intervalo: "))
        num2 = int(input("Digite o segundo termo do intervalo: "))
        soma = soma_inteiros(num1, num2)
        print(f"A soma dos inteiros entre {num1} e {num2} é {soma}")
        if input("Deseja continuar? (s/n) ") == "n":
            break


def verifica_numero():
    for num in range(1000, 10000):
        primeiro_termo = num // 100  # Obtém os dois primeiros algarismos
        segundo_termo = num % 100  # Obtém os dois últimos algarismos
        soma = primeiro_termo // 10 + primeiro_termo % 10  # Soma os dois primeiros algarismos
        resultado = soma * soma  # Multiplica a soma por si mesma
        if resultado == segundo_termo:  # Verifica se o resultado é igual aos dois últimos algarismos
            print(num)

def fatorial():
    n = int(input("Digite o valor de n: "))
    fat = 1
    for i in range(1, n+1):
        fat *= i
    print(f"O fatorial de {n} é {fat}")







def verifica_primo():
    n = int(input("Digite o valor de n: "))
    if n < 2:
        print("Não é primo")
    else:
        for i in range(2, n):
            if n % i == 0:
                print("Não é primo")
                break
        else:
            print("É primo")


def verifica_primo2(pergunta):
    primos = []
    nao_primos = []
    for n in range(0, 999):
        if n < 2:
            nao_primos.append(n)
        else:
            for i in range(2, n):
                if n % i == 0:
                    nao_primos.append(n)
                    break
            else:
                primos.append(n)
    if pergunta in primos:
        print(f"{pergunta} é primo")
    else:
        print(f"{pergunta} não é primo")

def pergunta():
    pergunta = input("Digite o número da lista de  0 a 9999: ")
    verifica_primo2(pergunta)




def quadrado_perfeito():
    n = int(input("Digite o valor de n: "))
    raiz = n ** 0.5
    if raiz == int(raiz):
        print("É quadrado perfeito")
    else:
        print("Não é quadrado perfeito")
quadrado_perfeito()