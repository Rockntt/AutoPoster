from bs4 import BeautifulSoup
import random
import json
import requests
import datetime
import json
import logging
import asyncio
from aiogram import Bot, types
from aiogram import Dispatcher, executor
import time
from fake_useragent import UserAgent

ua = UserAgent()

headers = {
    'accept': 'application/json, text/plain, */*',
    'user-Agent': ua.google,
}

article_dict = {}


url = f'https://habr.com/ru/top/daily/'

req = requests.get(url, headers=headers).text

soup = BeautifulSoup(req, 'lxml')
all_hrefs_articles = soup.find_all('a', class_='tm-title__link') # получаем статьи

for article in all_hrefs_articles: # проходимся по статьям
    article_name = article.find('span').text # собираем названия статей
    article_link = f'https://habr.com{article.get("href")}' # ссылки на статьи
    article_dict[article_name] = article_link
    print(article_name, article_link, article_dict)

with open(f"articles.json", "w", encoding='utf-8') as f:
    try:
        json.dump(article_dict, f, indent=4, ensure_ascii=False)
        print('Got it!')
    except:
        print('Error!')


# Настройки постинга
TOKEN = '123456789:blahblahblah' # Токен твоего телеграм-бота
CHANNEL_ID = '-123456789'  # ID твоего телеграм-канала
MESSAGES_FILE = 'articles.json'  # Файл со статьями

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Чтение сообщений из файла
with open(MESSAGES_FILE, 'r', encoding='UTF-8') as file:
    messages = json.load(file)

# Отправка сообщений в канал
async def send_messages():
    i = 1
    for key, value in messages.items():
        await bot.send_message(chat_id=CHANNEL_ID, text=f"[{key}]({value})\n\n[⤷ Читать статью]({value})\n\n#Habr", parse_mode="Markdown")
        print(i)
        i += 1
        time.sleep(3600) # Чтобы делать пост в ТГ каждый час

async def main():
    await send_messages()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())