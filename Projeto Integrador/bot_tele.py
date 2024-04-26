import asyncio
from aiogram import Bot
import csv

async def main():
    bot = Bot(token='7068288484:AAFCqDwuUOSrcJhBIXMwMQshDUMJ_U4ejGA')

    # Ler o arquivo de imagens e criar uma lista de URLs de imagens
    await bot.send_message(chat_id='7002586722', text='---------------🔥PROMOÇÕES DE JOGOS!🔥\n\n🎮XBOX🎮/PLAYSTATION DA SEMANA -------------------')
    with open('imagens_xbox.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        next(reader)  # Pular o cabeçalho
        img_urls = [row[0] for row in reader]

    # Ler o arquivo de jogos e enviar o conteúdo
    with open('jogos_xbox.csv', 'r', encoding='utf-8') as file:
        next(file)  # Pular o cabeçalho
        for line, img_url in zip(file, img_urls):
            title, price = line.strip().split(',', 1)
            caption = f"🔥PROMOÇÃO! {title}🔥\n\n💰POR APENAS {price}!💰"
            await bot.send_photo(chat_id='7002586722', photo=img_url, caption=caption)
    # Ler o arquivo de imagens e criar uma lista de URLs de imagens
    with open('imagens_playstation.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        img_urls = [row[0] for row in reader]

    # Ler o arquivo de jogos e enviar o conteúdo
    with open('jogos_playstation.csv', 'r', encoding='utf-8') as file: 
        next(file)  # Pular o cabeçalho
        for line, img_url in zip(file, img_urls):
            title, price = line.strip().split(',', 1)
            caption = f"🔥PROMOÇÃO! {title}🔥\n\n💰POR APENAS R$ {price}!💰"
            await bot.send_photo(chat_id='7002586722', photo=img_url, caption=caption)

asyncio.run(main())
