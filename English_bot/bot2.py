import logging
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# Настройки
TOKEN = "7809105311:AAFfNc7nuO9lQuB8CFWuhXmtX59ZooblUM4"
MODEL_NAME = "sberbank-ai/rugpt3small_based_on_gpt2"  # Можно заменить на 'gpt2' (английский)

# Инициализация Telegram-бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Загрузка GPT-2
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
model = GPT2LMHeadModel.from_pretrained(MODEL_NAME).to(device)

# Клавиатура
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Слова"), KeyboardButton("Разговоры"), KeyboardButton("Теория"))

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот для изучения английского.\nВыбери раздел:", reply_markup=keyboard)

# Генерация ответа через GPT-2
def generate_response(prompt):
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    output = model.generate(input_ids, max_length=100, num_return_sequences=1)
    return tokenizer.decode(output[0], skip_special_tokens=True)

# Обработчик всех сообщений
@dp.message_handler()
async def chat_with_ai(message: types.Message):
    response = generate_response(message.text)
    await message.answer(response)

# Запуск бота
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)