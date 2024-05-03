from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import csv

def obter_dados_jogo():
    driver = webdriver.Chrome()
    driver.get('https://www.xbox.com/pt-br/promotions/sales/sales-and-specials?xr=shellnav')
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    jogos = soup.find_all('div', class_='m-panes-product-placement-item')
    return jogos

def extrair_info_jogo(jogos):
    catalogo = []
    for jogo in jogos:
        div_titulo = jogo.find('h3', class_='c-heading-4')
        div_preco = jogo.find('div', class_='c-price')

        if div_titulo and div_preco:
            titulo = div_titulo.text
            div_preco_original = div_preco.find('s')
            if div_preco_original:
                preco_original = div_preco_original.text
            else:
                preco_original = "Preço original não encontrado"
            preco_atual = div_preco.text
            catalogo.append([titulo, preco_original, preco_atual])
        else:
            print("Título ou preço não encontrado para um jogo")
    return catalogo

def escrever_para_csv(nome_arquivo, cabecalhos, dados):
    with open(nome_arquivo, 'w', newline='') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(cabecalhos)
        for linha in dados:
            escritor.writerow(linha)

def limpar_dados_preco(df):
    df['Current Price'] = df['Current Price'].apply(lambda x: re.findall(r'R\$\d+.\d+', x)[-1] if re.findall(r'R\$\d+.\d+', x) else 'N/A')
    df = df[['Title', 'Current Price']]
    df.to_csv('jogos_xbox.csv', index=False)
    return df

def obter_imagens(jogos):
    imagens = []
    for jogo in jogos:
        img = jogo.find('img')
        if img:
            imagens.append([img['src']])
        else:
            imagens.append(["Imagem não encontrada"])
    return imagens

def principal():
    jogos = obter_dados_jogo()
    catalogo = extrair_info_jogo(jogos)
    escrever_para_csv('jogos_xbox.csv', ["Title", "Original Price", "Current Price"], catalogo)
    df = pd.read_csv('jogos_xbox.csv', encoding='ISO-8859-1')
    df = limpar_dados_preco(df)
    print(df)
    imagens = obter_imagens(jogos)
    escrever_para_csv('imagens_xbox.csv', ["Image"], imagens)
    time.sleep(2)

if __name__ == "__main__":
    principal()