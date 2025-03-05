# Создаем бота
import config
import telebot
import random
from telebot import types

bot = telebot.TeleBot(config.token)

# Загружаем список интересных фактов
with open('/Users/igordemidov/Desktop/DemidovIgorBot/Виртуальные_кнопки/facts.txt', 'r', encoding='UTF-8') as f:
    facts = f.read().split('\n')

# Загружаем список поговорок
with open('/Users/igordemidov/Desktop/DemidovIgorBot/Виртуальные_кнопки/thinks.txt', 'r', encoding='UTF-8') as f:
    thinks = f.read().split('\n')


# Команда start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    # Добавляем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Новость")
    item2 = types.KeyboardButton("Афоризм")
    markup.add(item1, item2)
    bot.send_message(m.chat.id,
                     'Нажми:\nНовость - для получения сегодняшних новостей\nАфоризм - для получения лучших афоризмов всех времён',
                     reply_markup=markup)


# Получение сообщений от клиента
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Новость':
        answer = random.choice(facts)
    elif message.text.strip() == 'Афоризм':
        answer = random.choice(thinks)
    else:
        answer = "Я не понимаю эту команду."

    # Отсылаем сообщение в чат пользователя
    bot.send_message(message.chat.id, answer)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
