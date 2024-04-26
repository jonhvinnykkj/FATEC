from lxml import html
import requests
import csv
import pandas as pd
import re

catalog = []
img = []
for i in range(1,98):  # 97 páginas
    url = f'https://store.playstation.com/pt-br/category/dc464929-edee-48a5-bcd3-1e6f5250ae80/{i}'
    response = requests.get(url)
    print(f"Page {i} - Status code: {response.status_code}")
    tree = html.fromstring(response.content)
    games = tree.xpath('//div[contains(@class, "psw-product-tile psw-interactive-root")]')

    print(f"Found {len(games)} games in page {i}")
    for game in games:
        title = game.xpath('.//span[contains(@data-qa, "product-name")]/text()')
        price = game.xpath('.//span[contains(@data-qa, "price#display-price")]/text()')
        image_urls = game.xpath('.//img[contains(@data-qa, "game-art#image#image")]/@src')
        if title and price and image_urls:
            catalog.append([title[0], price[0]])
            img.append(image_urls[0])
        else:
            print("Title, price or image URL not found for a game")

with open('jogos_playstation.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price"])
    for game in catalog:
        writer.writerow(game)
with open('imagens_playstation.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Image"])
    for image in img:
        writer.writerow([image])

df = pd.read_csv('jogos_playstation.csv', encoding='ISO-8859-1')
df['Price'] = df['Price'].apply(lambda x: re.findall(r'R\$\d+.\d+', x)[-1] if re.findall(r'R\$\d+.\d+', x) else 'N/A')
df['Price'] = df['Price'].str.replace('"', '')  
df = df[['Title', 'Price']]
df.to_csv('jogos_playstation.csv', index=False)

print(df)



import numpy as np
#filra os jogos com preço abaixo de 50
if df['Price'].str.contains('R\$').any():
    df['Price'] = df['Price'].replace('N/A', np.nan)
    df['Price'] = df['Price'].str.replace('R$', '').str.replace(',', '.').astype(float)
    df = df[df['Price'] < 50]
    df.to_csv('jogos_playstation.csv', index=False)
    print(df)
else:

    print('Não há jogos com preço abaixo de 50 reais')