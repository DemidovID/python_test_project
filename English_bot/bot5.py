import asyncio
import language_tool_python
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from config import TOKEN  # Убедись, что у тебя есть файл config.py с переменной TOKEN

# Инициализация бота и инструмента для проверки грамматики
bot = Bot(token=TOKEN)
dp = Dispatcher()
tool = language_tool_python.LanguageTool('en-US')  # Проверка английского языка

# Клавиатура с кнопкой "Тренировать письмо"
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✍️ Тренировать письмо")],
    ],
    resize_keyboard=True
)

# Флаг для определения, что пользователь сейчас тренирует письмо
user_states = {}

# Функция для улучшенной проверки текста
def check_text(text):
    matches = tool.check(text)
    if not matches:
        return "✅ No issues found! Your text is great."

    suggestions = []
    corrected_text = text

    for match in matches:
        error_part = text[match.offset:match.offset + match.errorLength]
        suggested_fix = ", ".join(match.replacements) if match.replacements else "No suggestion"

        # Исправляем текст (берем первую предложенную замену)
        if match.replacements:
            corrected_text = corrected_text.replace(error_part, match.replacements[0], 1)

        # Формируем подробный анализ ошибки
        suggestions.append(
            f"❌ **Ошибка:** {error_part}\n"
            f"📌 **Описание:** {match.message}\n"
            f"💡 **Совет:** {suggested_fix}\n"
        )

    # Итоговый ответ
    response = "**Найдены ошибки:**\n" + "\n".join(suggestions) + "\n"
    response += "**✍️ Улучшенный вариант:**\n" + corrected_text
    return response

# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "👋 Привет! Я помогу тебе тренировать английский.\n\n"
        "Нажми '✍️ Тренировать письмо', напиши текст, и я его проверю.",
        reply_markup=keyboard
    )

# Обработчик кнопки "Тренировать письмо"
@dp.message()
async def handle_button_press(message: Message):
    if message.text == "✍️ Тренировать письмо":
        user_states[message.from_user.id] = "writing"
        await message.answer("📝 Отлично! Напиши текст, и я его проверю.")
    elif user_states.get(message.from_user.id) == "writing":
        result = check_text(message.text)
        await message.answer(result, parse_mode="Markdown")
        user_states[message.from_user.id] = None  # Сбрасываем состояние
    else:
        await message.answer("❓ Я тебя не понял. Нажми кнопку '✍️ Тренировать письмо', чтобы начать.")
        
# Запуск бота
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
