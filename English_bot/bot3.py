import json
import random
import logging
import asyncio
import torch
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from config import TOKEN  # Убедись, что у тебя есть файл config.py с переменной TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Загружаем данные из файла
with open("/Users/igordemidov/Desktop/DemidovIgorBot/English_bot/data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Индексы для теории
user_theory_progress = {}

# Клавиатура
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📖 Слова"), KeyboardButton(text="🗣 Разговор")],
        [KeyboardButton(text="📚 Теория TIHL"), KeyboardButton(text="🤖 GPT-2")]
    ],
    resize_keyboard=True
)

# Загрузка модели GPT-2
MODEL_NAME = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)

# Функция для генерации текста с GPT-2
def generate_gpt2_response(prompt, max_length=50):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    
    with torch.no_grad():
        output = model.generate(
            input_ids, 
            max_length=max_length, 
            num_return_sequences=1, 
            pad_token_id=tokenizer.eos_token_id
        )

    return tokenizer.decode(output[0], skip_special_tokens=True)

# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! Я бот для изучения английского. Выбери, что хочешь изучать!",
        reply_markup=menu_keyboard
    )

# Слова
@dp.message(lambda msg: msg.text == "📖 Слова")
async def send_word(message: Message):
    word = random.choice(data["words"])
    response = f"**Слово:** {word['word']}\n**Перевод:** {word['translation']}\n**Пример:** {word['example']}"
    await message.answer(response, parse_mode="Markdown")

# Разговорные вопросы
@dp.message(lambda msg: msg.text == "🗣 Разговор")
async def send_question(message: Message):
    question = random.choice(data["questions"])
    await message.answer(f"💬 {question}")

# Теория TIHL
@dp.message(lambda msg: msg.text == "📚 Теория TIHL")
async def send_theory(message: Message):
    user_id = message.from_user.id
    if user_id not in user_theory_progress:
        user_theory_progress[user_id] = 0

    index = user_theory_progress[user_id]
    if index < len(data["theory"]):
        await message.answer(data["theory"][index])
        user_theory_progress[user_id] += 1
    else:
        await message.answer("Ты уже изучил всю теорию!")

# GPT-2 чат
@dp.message(lambda msg: msg.text == "🤖 GPT-2")
async def ask_gpt2(message: Message):
    await message.answer("Отправь мне сообщение, и я отвечу с помощью локального GPT-2!")

@dp.message()
async def handle_gpt2_message(message: Message):
    response = generate_gpt2_response(message.text)
    await message.answer(response)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
