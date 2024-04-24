from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import csv
import requests

# driver = webdriver.Chrome()
# driver.get('https://www.xbox.com/pt-br/promotions/sales/sales-and-specials?xr=shellnav')
# time.sleep(5)

# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')
# games = soup.find_all('div', class_='m-panes-product-placement-item')

# catalog = []
# for game in games:
#     title_div = game.find('h3', class_='c-heading-4')
#     price_div = game.find('div', class_='c-price')

#     if title_div and price_div:
#         title = title_div.text
#         original_price_div = price_div.find('s')
#         if original_price_div:
#             original_price = original_price_div.text
#         else:
#             original_price = "Original price not found"
#         current_price = price_div.text
#         catalog.append([title, original_price, current_price])
#     else:
#         print("Title or price not found for a game")

# with open('catalog.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Title", "Original Price", "Current Price"])
#     for game in catalog:
#         writer.writerow(game)

# df = pd.read_csv('catalog.csv', encoding='ISO-8859-1')
# df['Current Price'] = df['Current Price'].apply(lambda x: re.findall(r'R\$\d+.\d+', x)[-1] if re.findall(r'R\$\d+.\d+', x) else 'N/A')
# df = df[['Title', 'Current Price']]
# df.to_csv('catalog_cleaned.csv', index=False)

# print(df)


# #envia as imagens para um arquivo csv chamado img.csv
# with open('img.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Image"])
#     for game in games:
#         img = game.find('img')
#         if img:
#             writer.writerow([img['src']])
#         else:
#             writer.writerow(["Image not found"])

# time.sleep(2)

#Playstation
from lxml import html
catalog = []

for i in range(1, 4):  # 97 páginas
    url = f'https://store.playstation.com/pt-br/category/dc464929-edee-48a5-bcd3-1e6f5250ae80/{i}'
    response = requests.get(url)
    print(f"Page {i} - Status code: {response.status_code}")
    tree = html.fromstring(response.content)

    games = tree.xpath('/html/body/div[3]/main/section/div/div/div/div[2]/div[2]')

    print(f"Found {len(games)} games in page {i}")
    for game in games:
        title = game.xpath('.//span[contains(@data-qa, "product-name")]/text()')
        price = game.xpath('.//h3[contains(@data-qa, "display-price")]/text()')

        if title and price:
            catalog.append([title[0], price[0]])
        else:
            print("Title or price not found for a game")

with open('catalogplay.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price"])
    for game in catalog:
        writer.writerow(game)

with open('catalogplay.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price"])
    for game in catalog:
        writer.writerow(game)

