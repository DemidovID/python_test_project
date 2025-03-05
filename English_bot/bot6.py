import random
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import F
import asyncio

# Включаем логирование
logging.basicConfig(level=logging.INFO)

API_TOKEN = "7809105311:AAFfNc7nuO9lQuB8CFWuhXmtX59ZooblUM4"

# Создаем экземпляры бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Список слов для тренировки
words_list = [
    ("apple", "яблоко", "I eat an apple every day."),
    ("dog", "собака", "My dog loves to play with a ball."),
    ("house", "дом", "We live in a big house.")
]

# Стартовый обработчик
@dp.message(F.command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="Слова", callback_data='words'),
        InlineKeyboardButton(text="Тренировка выражения", callback_data='expression'),
        InlineKeyboardButton(text="Тренировка восприятия", callback_data='perception'),
        InlineKeyboardButton(text="Теория о языке", callback_data='theory')
    ]
    keyboard.add(*buttons)
    await message.answer("Привет! Я бот для изучения языков. Выберите действие:", reply_markup=keyboard)

# Обработчик для кнопки "Слова"
@dp.callback_query(F.data == 'words')
async def words(callback_query: types.CallbackQuery):
    word, translation, example = random.choice(words_list)
    text = f"Новое слово: {word}\nПеревод: {translation}\nПример: {example}"
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="Еще одно слово", callback_data='words'),
        InlineKeyboardButton(text="Закончить", callback_data='end')
    ]
    keyboard.add(*buttons)
    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text, reply_markup=keyboard)

# Обработчик для кнопки "Тренировка выражения"
@dp.callback_query(F.data == 'expression')
async def expression(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text="Предложить тему", callback_data='suggest_topic'),
        InlineKeyboardButton(text="Закончить", callback_data='end')
    ]
    keyboard.add(*buttons)
    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Напишите текст на тему для тренировки выражения.", reply_markup=keyboard)

# Обработчик для кнопки "Тренировка восприятия"
@dp.callback_query(F.data == 'perception')
async def perception(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text="Восприятие на слух", callback_data='listen'),
        InlineKeyboardButton(text="Восприятие текста", callback_data='text'),
        InlineKeyboardButton(text="Закончить", callback_data='end')
    ]
    keyboard.add(*buttons)
    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Выберите, что хотите тренировать: восприятие на слух или восприятие текста.", reply_markup=keyboard)

# Обработчик для восприятия на слух
@dp.callback_query(F.data == 'listen')
async def listen(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Проигрываю запись... Напишите, что слышите.")
    # Тут нужно добавить логику для проигрывания аудио

# Обработчик для восприятия текста
@dp.callback_query(F.data == 'text')
async def text(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Переведите следующий текст: 'My name is John.'")

# Обработчик для теории
@dp.callback_query(F.data == 'theory')
async def theory(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text="Учебник", callback_data='textbook'),
        InlineKeyboardButton(text="Закончить", callback_data='end')
    ]
    keyboard.add(*buttons)
    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Здесь будет учебник по теории языка.", reply_markup=keyboard)

# Обработчик для завершения
@dp.callback_query(F.data == 'end')
async def end(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Спасибо за использование бота!")

# Запуск бота
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
