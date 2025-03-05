from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📖 Слова"), KeyboardButton("🗣 Разговор")],
        [KeyboardButton("📚 Теория TIHL")]
    ],
    resize_keyboard=True
)
