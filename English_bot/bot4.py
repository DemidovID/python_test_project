import json
import random
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from config import TOKEN  # Убедись, что у тебя есть файл config.py с переменной TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Загружаем данные из файла
with open("/Users/igordemidov/Desktop/DemidovIgorBot/English_bot/data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Клавиатура
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧑‍🏫 Тренировка слов"), KeyboardButton(text="📚 Общие слова")],
        [KeyboardButton(text="🔄 Тесты на перевод"), KeyboardButton(text="🗣 Фразы для общения")]
    ],
    resize_keyboard=True
)

# Индекс текущего слова для тренировки
user_progress = {}

# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! Я бот для изучения английского. Выбери, что хочешь изучать!",
        reply_markup=menu_keyboard
    )

# Тренировка слов
@dp.message(lambda msg: msg.text == "🧑‍🏫 Тренировка слов")
async def start_word_training(message: Message):
    user_id = message.from_user.id
    if user_id not in user_progress:
        user_progress[user_id] = {"index": 0, "correct": 0, "incorrect": 0}

    word = data["words"][user_progress[user_id]["index"]]
    question = f"Переведи это слово на английский: {word['word']}"
    user_progress[user_id]["word"] = word
    await message.answer(question)

@dp.message()
async def check_word_answer(message: Message):
    user_id = message.from_user.id
    if user_id not in user_progress or "word" not in user_progress[user_id]:
        return

    correct_word = user_progress[user_id]["word"]["translation"]
    user_answer = message.text.strip().lower()

    if user_answer == correct_word.lower():
        user_progress[user_id]["correct"] += 1
        await message.answer("Правильно!")
    else:
        user_progress[user_id]["incorrect"] += 1
        await message.answer(f"Неправильно. Правильный ответ: {correct_word}")

    # Переходим к следующему слову
    user_progress[user_id]["index"] += 1
    if user_progress[user_id]["index"] < len(data["words"]):
        word = data["words"][user_progress[user_id]["index"]]
        question = f"Переведи это слово на английский: {word['word']}"
        user_progress[user_id]["word"] = word
        await message.answer(question)
    else:
        await message.answer(f"Ты прошел все слова! Правильных ответов: {user_progress[user_id]['correct']}, Неправильных: {user_progress[user_id]['incorrect']}")
        user_progress[user_id]["index"] = 0  # Сбросить прогресс для следующего обучения

# Общие слова
@dp.message(lambda msg: msg.text == "📚 Общие слова")
async def show_common_words(message: Message):
    word = random.choice(data["words"])
    response = f"**Слово:** {word['word']}\n**Перевод:** {word['translation']}\n**Пример:** {word['example']}"
    await message.answer(response, parse_mode="Markdown")

# Тесты на перевод
@dp.message(lambda msg: msg.text == "🔄 Тесты на перевод")
async def start_translation_test(message: Message):
    word = random.choice(data["words"])
    choices = random.sample(data["words"], 3)
    correct_translation = word["translation"]
    options = [word["translation"]] + [choice["translation"] for choice in choices]
    random.shuffle(options)

    options_text = "\n".join([f"{idx+1}. {opt}" for idx, opt in enumerate(options)])
    question = f"Какой перевод у этого слова: {word['word']}?\n{options_text}"

    user_progress[message.from_user.id] = {"test_word": word, "correct_answer": correct_translation}
    await message.answer(question)

@dp.message()
async def check_translation_answer(message: Message):
    user_id = message.from_user.id
    if user_id not in user_progress or "test_word" not in user_progress[user_id]:
        return

    correct_answer = user_progress[user_id]["correct_answer"]
    try:
        answer = int(message.text.strip())
    except ValueError:
        await message.answer("Пожалуйста, выбери вариант от 1 до 4.")
        return

    if answer < 1 or answer > 4:
        await message.answer("Пожалуйста, выбери вариант от 1 до 4.")
        return

    options = [user_progress[user_id]["test_word"]["translation"]] + \
             [choice["translation"] for choice in random.sample(data["words"], 3)]
    options_text = [opt.lower() for opt in options]
    
    if options_text[answer - 1] == correct_answer.lower():
        await message.answer("Правильно!")
    else:
        await message.answer(f"Неправильно. Правильный перевод: {correct_answer}")

# Фразы для общения
@dp.message(lambda msg: msg.text == "🗣 Фразы для общения")
async def show_communication_phrases(message: Message):
    phrase = random.choice(data["phrases"])
    response = f"**Фраза:** {phrase['phrase']}\n**Перевод:** {phrase['translation']}"
    await message.answer(response, parse_mode="Markdown")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
