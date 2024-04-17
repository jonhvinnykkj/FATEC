from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Inicialize o driver do navegador (você precisa do driver correto para o seu navegador instalado, neste exemplo, usamos o Chrome)
driver = webdriver.Chrome()

# Carregue a página
driver.get('https://www.xbox.com/pt-br/promotions/sales/sales-and-specials?xr=shellnav')

# Aguarde o JavaScript ser executado
time.sleep(15)

# Obtenha o conteúdo da página
html = driver.page_source

# Use BeautifulSoup para analisar o conteúdo
soup = BeautifulSoup(html, 'html.parser')

# Agora você pode encontrar os elementos como antes
games = soup.find_all('div', class_='m-panes-product-placement-item')

catalog = []
for game in games:
    title_div = game.find('h3', class_='c-heading-4')
    price_div = game.find('div', class_='c-price')

    if title_div and price_div:
        title = title_div.text
        original_price_div = price_div.find('s')
        if original_price_div:
            original_price = original_price_div.text
        else:
            original_price = "Original price not found"
        current_price = price_div.text
        catalog.append([title, original_price, current_price])
    else:
        print("Title or price not found for a game")

#Filtra somente o nome do jogo e o preço atual e salva em um arquivo CSV
import csv

with open('catalog.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Original Price", "Current Price"])
    for game in catalog:
        writer.writerow(game)

import pandas as pd
import re
import chardet

rawdata = open('xbox_sales.csv', 'rb').read()
result = chardet.detect(rawdata)
print(result['encoding'])

df = pd.read_csv('xbox_sales.csv', encoding=result['encoding'])

# Create a new DataFrame with only the game title and current price
df['Current Price'] = df['Current Price'].apply(lambda x: x.split('Agora por')[-1] if 'Agora por' in x else 'N/A')
na_prices = df[df['Current Price'] == 'N/A']
print(na_prices)
new_df = df[['Title', 'Current Price']]

# Print the game title and current price
for index, row in new_df.iterrows():
    print(f"Jogo: {row['Title']} Preço: {row['Current Price']}")

#reescreve o arquivo CSV com os dados filtrados
new_df.to_csv('xbox_sales.csv', index=False)
