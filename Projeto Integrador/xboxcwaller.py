from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import csv

driver = webdriver.Chrome()
driver.get('https://www.xbox.com/pt-br/promotions/sales/sales-and-specials?xr=shellnav')
time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
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

with open('jogos_xbox.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Original Price", "Current Price"])
    for game in catalog:
        writer.writerow(game)

df = pd.read_csv('jogos_xbox.csv', encoding='ISO-8859-1')
df['Current Price'] = df['Current Price'].apply(lambda x: re.findall(r'R\$\d+.\d+', x)[-1] if re.findall(r'R\$\d+.\d+', x) else 'N/A')
df = df[['Title', 'Current Price']]
df.to_csv('jogos_xbox.csv', index=False)

print(df)


#envia as imagens para um arquivo csv chamado img.csv
with open('imagens_xbox.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Image"])
    for game in games:
        img = game.find('img')
        if img:
            writer.writerow([img['src']])
        else:
            writer.writerow(["Image not found"])

time.sleep(2)