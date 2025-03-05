import json
import random
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Загружаем данные из файла
with open("/Users/igordemidov/Desktop/DemidovIgorBot/English_bot/data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Индексы для теории
user_theory_progress = {}

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📖 Слова"), KeyboardButton(text="🗣 Разговор")],
        [KeyboardButton(text="📚 Теория TIHL")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! Я бот для изучения английского. Выбери, что хочешь изучать!",
        reply_markup=menu_keyboard
    )

@dp.message(lambda msg: msg.text == "📖 Слова")
async def send_word(message: Message):
    word = random.choice(data["words"])
    response = f"**Слово:** {word['word']}\n**Перевод:** {word['translation']}\n**Пример:** {word['example']}"
    await message.answer(response, parse_mode="Markdown")

@dp.message(lambda msg: msg.text == "🗣 Разговор")
async def send_question(message: Message):
    question = random.choice(data["questions"])
    await message.answer(f"💬 {question}")

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

@dp.message()
async def handle_other_messages(message: Message):
    await message.answer("Я пока понимаю только команды из меню 🙂")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
