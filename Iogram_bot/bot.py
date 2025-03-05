from aiogram import Bot, Dispatcher, types
from aiogram import F
import logging
import asyncio
import config

# Инициализация бота
bot = Bot(token=config.token)

# Инициализация диспетчера
dp = Dispatcher()

# Логирование ошибок
logging.basicConfig(level=logging.INFO)

# Обработка команды /start
@dp.message(F.text == '/start')
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ Эхо-бот от Skillbox!\nОтправь мне любое сообщение, а я тебе обязательно отвечу.")

# Эхо-обработка всех сообщений
@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)

# Функция запуска бота
async def main():
    # Привязываем диспетчер к боту
    await dp.start_polling(bot)

# Запуск асинхронной функции
if __name__ == "__main__":
    asyncio.run(main())
