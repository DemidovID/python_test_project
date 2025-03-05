import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Токен твоего бота
TOKEN = '7809105311:AAFfNc7nuO9lQuB8CFWuhXmtX59ZooblUM4'

# Включаем логирование для отслеживания работы бота
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция для команды /start
async def start(update: Update, context):
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} начал разговор")
    # Создаем клавиатуру с кнопками
    keyboard = [
        ['Услуги', 'Заказать уборку'],
        ['Поддержка']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text('Добро пожаловать в CleanBot! Чем могу помочь?', reply_markup=reply_markup)

# Функция для обработки текстовых сообщений
async def handle_message(update: Update, context):
    text = update.message.text
    if text == 'Услуги':
        await update.message.reply_text('Мы предлагаем:\n- Стандартная уборка — 2000 руб.\n- Генеральная уборка — 5000 руб.\n- Уборка после ремонта — 7000 руб.')
    elif text == 'Заказать уборку':
        await update.message.reply_text('Выберите тип уборки:\n1. Стандартная\n2. Генеральная\n3. После ремонта')
    elif text == 'Поддержка':
        await update.message.reply_text('Свяжитесь с нами по телефону: +7 999 123-45-67')
    else:
        await update.message.reply_text('Пожалуйста, выберите действие из меню.')

# Основная функция для запуска бота
def main():
    # Создаем приложение с твоим токеном
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Добавляем обработчик текстовых сообщений (кроме команд)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()