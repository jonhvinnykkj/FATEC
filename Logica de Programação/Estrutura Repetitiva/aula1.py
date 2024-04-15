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

