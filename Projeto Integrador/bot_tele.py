import asyncio
from aiogram import Bot
import csv
import os  # Importe o módulo os

async def enviar_mensagem_promocao(bot, chat_id, mensagem):
    await bot.send_message(chat_id=chat_id, text=mensagem)

def ler_arquivo_csv(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        leitor = csv.reader(arquivo)
        next(leitor)
        dados = [linha[0] for linha in leitor]
    return dados

async def enviar_promocoes(bot, chat_id, arquivo_jogos, arquivo_imagens):
    img_urls = ler_arquivo_csv(arquivo_imagens)
    with open(arquivo_jogos, 'r', encoding='utf-8') as arquivo:
        next(arquivo)  # Pular o cabeçalho
        for linha, img_url in zip(arquivo, img_urls):
            titulo, preco = linha.strip().split(',', 1)
            legenda = f"🔥PROMOÇÃO! {titulo}🔥\n\n💰POR APENAS {preco}!💰"
            await bot.send_photo(chat_id=chat_id, photo=img_url, caption=legenda)

async def main():
    bot_token = os.getenv('BOT_TOKEN')  # Obtenha o token do bot da variável de ambiente
    if bot_token is None:
        raise Exception('Token não definido. Por favor, defina a variável de ambiente BOT_TOKEN.')
    bot = Bot(token=bot_token)
    chat_id = '7002586722'
    mensagem = '---------------🔥PROMOÇÕES DE JOGOS!🔥\n\n🎮XBOX🎮/PLAYSTATION DA SEMANA -------------------'
    await enviar_mensagem_promocao(bot, chat_id, mensagem)
    await enviar_promocoes(bot, chat_id, 'jogos_xbox.csv', 'imagens_xbox.csv')
    await enviar_promocoes(bot, chat_id, 'jogos_playstation.csv', 'imagens_playstation.csv')

asyncio.run(main())