def programa1():
    a = 5
    b = 1

    while b <= a:
        print(a)
        a = a + 1
        break

def programa2(): #tabuada
    num = int(input('Digite um número: '))
    a = 0
    while a <= 10:
        print(f'{num} x {a} = {num * a}')
        a = a + 1

def programa3():
    pergunta = input('Deseja uma tabuaba? [S/N] ')
    while pergunta == 'S' or pergunta == 's':
        num = int(input('Digite um número: '))
        a = 0
        while a <= 10:
            print(f'{num} x {a} = {num * a}')
            a = a + 1
        pergunta = input('Deseja continuar? [S/N] ')

def programa4():
    for i in range(1, 11):
        if i == 4:
            break
        print(f"{i}")

    for i in range(1, 11):
        if i == 4:
            continue
        print(f"{i}")

def programa5():
    soma = 0
    num = 1
    while num != 0:
        num = int(input('Digite um número: '))
        soma = soma + num
        if num == 0:
            break
    print(f'A soma dos números digitados é {soma}')

def programa6():
    num = int(input('Digite um número: '))
    for i in range(0, 11):
        print(f'{num} x {i} = {num * i}')

def programa7():
    num = -1
    while True:
        num += 1
        print(num)
        if num == 100:
            break
        