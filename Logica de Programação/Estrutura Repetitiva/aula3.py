CLASSIFICACOES = {
    18.5: 'Abaixo do peso',
    24.9: 'Peso normal',
    29.9: 'Sobrepeso',
    34.9: 'Obesidade grau 1',
    39.9: 'Obesidade grau 2',
    40: 'Obesidade grau 3'
}

def calcular_classificar_imc(peso, altura):
    imc = peso / (altura ** 2)
    for limite, classificacao in CLASSIFICACOES.items():
        if imc <= limite:
            return classificacao

try:
    peso = float(input('Digite o peso: '))
    altura = float(input('Digite a altura: '))
    print(f'O IMC é {calcular_classificar_imc(peso, altura)}')
except ValueError:
    print("Entrada inválida. Por favor, insira um número.")