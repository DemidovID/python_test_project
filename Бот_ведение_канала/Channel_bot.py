import config
import telebot
import time

bot = telebot.TeleBot(config.token)
# Адрес телеграм-канала, начинается с @
CHANNEL_NAME = '@HarryGraceEnglish'

# Загружаем список шуток
file_path = '/Users/igordemidov/Desktop/DemidovIgorBot/Бот_ведение_канала/fun.txt'

try:
    with open(file_path, 'r', encoding='UTF-8') as f:
        jokes = f.read().split('\n')
except FileNotFoundError:
    jokes = ["Файл с анекдотами не найден!"]

# Пока не закончатся шутки, посылаем их в канал
for joke in jokes:
    bot.send_message(CHANNEL_NAME, joke)
    # Делаем паузу в 30 секунд (можно указать любое время)
    time.sleep(5)

bot.send_message(CHANNEL_NAME, "Анекдоты внезапно закончились")