import config
import telebot
import os
from fuzzywuzzy import fuzz
import config


bot = telebot.TeleBot(config.token)

# Загружаем список фраз и ответов в массив
mas = []

faq_file_path = r'/Users/igordemidov/Desktop/DemidovIgorBot/Чат_бот/faq.txt'  # Путь к файлу faq.txt

if os.path.exists(faq_file_path):
    with open(faq_file_path, 'r', encoding='UTF-8') as f:
        faq_pairs = []
        # Читаем файл и собираем пары вопрос-ответ
        for line in f:
            line = line.strip().lower()
            if len(line) > 2:
                if line.startswith("u: "):  # Вопрос
                    question = line.replace('u: ', '')
                    answer = next(f, '').strip().lower().replace('u: ', '')
                    faq_pairs.append((question, answer))

# С помощью fuzzywuzzy определяем наиболее похожую фразу и выдаем в качестве ответа следующий элемент списка
def answer(text):
    try:
        text = text.lower().strip()
        if os.path.exists(faq_file_path):
            a = 0
            best_match = None
            # Поиск самого похожего вопроса
            for question, response in faq_pairs:
                aa = fuzz.token_sort_ratio(question, text)
                print(f"Сравниваю: {question} с {text}, схожесть: {aa}")  # Диагностика
                if aa > a:
                    a = aa
                    best_match = response
            if best_match:
                print(f"Найден ответ: {best_match}")  # Диагностика
                return best_match
            else:
                return 'Не смог найти подходящий ответ.'
        else:
            return 'Не найден файл FAQ'
    except Exception as e:
        return f'Ошибка: {e}'

# Команда «Старт»
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Давай поболтаем. Например, напиши мне Привет!')

# Получение сообщений от клиента
@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Запись ответа
    s = answer(message.text)
    # Отправка ответа
    bot.send_message(message.chat.id, s)

# Запускаем бота
bot.polling(none_stop=True, interval=0)