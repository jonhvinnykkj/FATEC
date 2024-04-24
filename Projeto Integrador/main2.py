import asyncio
from aiogram import Bot
import csv

async def main():
    bot = Bot(token='7068288484:AAFCqDwuUOSrcJhBIXMwMQshDUMJ_U4ejGA')

    # Ler o arquivo de imagens e criar uma lista de URLs de imagens
    with open('img.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        next(reader)  # Pular o cabeçalho
        img_urls = [row[0] for row in reader]

    # Ler o arquivo de jogos e enviar o conteúdo
    with open('catalog_cleaned.csv', 'r') as file:
        next(file)  # Pular o cabeçalho
        for line, img_url in zip(file, img_urls):
            title, price = line.strip().split(',')
            caption = f"🔥PROMOÇÃO! {title}🔥\n\n💰POR APENAS {price}!💰\n \n🏃‍♂️CORRE, VAI PERDER ESSA OPORTUNIDADE?🏃‍♂️"
            await bot.send_photo(chat_id='7002586722', photo=img_url, caption=caption)

# Rodar a função assíncrona
asyncio.run(main())