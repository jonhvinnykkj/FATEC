import csv
import re
import requests
import pandas as pd
from lxml import html
import numpy as np

#Obtenção dos Dados
def obter_dados_jogo(numero_pagina):
    url = f'https://store.playstation.com/pt-br/category/dc464929-edee-48a5-bcd3-1e6f5250ae80/{numero_pagina}?FULL_GAME=storeDisplayClassification'
    resposta = requests.get(url)
    print(f"Página {numero_pagina} - Código de status: {resposta.status_code}")
    arvore = html.fromstring(resposta.content)
    jogos = arvore.xpath('//div[contains(@class, "psw-product-tile psw-interactive-root")]')
    print(f"Encontrados {len(jogos)} jogos na página {numero_pagina}")
    return jogos

def extrair_info_jogo(jogo):
    titulo = jogo.xpath('.//span[contains(@data-qa, "product-name")]/text()')
    preco = jogo.xpath('.//span[contains(@data-qa, "price#display-price")]/text()')
    urls_imagem = jogo.xpath('.//img[contains(@data-qa, "game-art#image#image")]/@src')
    if titulo and preco and urls_imagem:
        return titulo[0], preco[0], urls_imagem[0]
    else:
        print("Título, preço ou URL da imagem não encontrados para um jogo")
        return None, None, None

def escrever_para_csv(nome_arquivo, cabecalhos, dados):
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(cabecalhos)
        for linha in dados:
            escritor.writerow(linha)


#Tratamento dos Dados Obtidos
def limpar_dados_preco(df):
    df['Price'] = df['Price'].apply(lambda x: re.findall(r'R\$\d+.\d+', x)[-1] if re.findall(r'R\$\d+.\d+', x) else 'N/A')
    df['Price'] = df['Price'].str.replace('"', '')  
    df = df[['Title', 'Price']]
    df.to_csv('jogos_playstation.csv', index=False)
    return df

def filtrar_jogos(df):
    if df['Price'].str.contains('R\$').any():
        df['Price'] = df['Price'].replace('N/A', np.nan)
        df['Price'] = df['Price'].str.replace('R$', '').str.replace(',', '.').astype(float)
        df = df[df['Price'] < 50]
        df.to_csv('jogos_playstation.csv', index=False)
        print(df)
    else:
        print('Não há jogos com preço abaixo de 50 reais')

#Função Principal
def principal():
    catalogo = []
    imagens = []
    for i in range(1,59):  # 59 páginas
        jogos = obter_dados_jogo(i)
        for jogo in jogos:
            titulo, preco, url_imagem = extrair_info_jogo(jogo)
            if titulo and preco and url_imagem:
                catalogo.append([titulo, preco])
                imagens.append([url_imagem])
    escrever_para_csv('jogos_playstation.csv', ["Title", "Price"], catalogo)
    escrever_para_csv('imagens_playstation.csv', ["Image"], imagens)
    df = pd.read_csv('jogos_playstation.csv', encoding='ISO-8859-1')
    df = limpar_dados_preco(df)
    print(df)
    filtrar_jogos(df)

if __name__ == "__main__":
    principal()