import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler

# Укажите токен вашего бота, полученный от BotFather
TOKEN = '7809105311:AAFfNc7nuO9lQuB8CFWuhXmtX59ZooblUM4'  # Замените на ваш токен

# Настройка логирования для отслеживания работы бота
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Определяем состояния для процесса заказа
CHOOSING_SERVICE, ENTERING_ADDRESS, CHOOSING_TIME, CONFIRMATION = range(4)

# Функция для команды /start
async def start(update: Update, context):
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} начал разговор")
    welcome_text = (
        "🌟 Добро пожаловать в CleanBot! 🌟\n"
        "Мы — выдуманная клининговая компания, которая сделает ваш дом идеально чистым! ✨\n\n"
        "Чем могу помочь сегодня?"
    )
    keyboard = [
        ['🧹 Услуги', '🛒 Заказать уборку'],
        ['💬 Поддержка']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# Обработка текстовых сообщений из меню
async def handle_message(update: Update, context):
    text = update.message.text
    if text == '🧹 Услуги':
        await update.message.reply_text('Мы предлагаем:\n- Стандартная уборка — 2000 руб.\n- Генеральная уборка — 5000 руб.\n- Уборка после ремонта — 7000 руб.')
    elif text == '🛒 Заказать уборку':
        return await order_start(update, context)
    elif text == '💬 Поддержка':
        await update.message.reply_text('Свяжитесь с нами по телефону: +7 999 123-45-67')
    else:
        await update.message.reply_text('Пожалуйста, выберите действие из меню.')

# Начало процесса заказа уборки
async def order_start(update: Update, context):
    keyboard = [['Стандартная', 'Генеральная'], ['После ремонта']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Выберите тип уборки:", reply_markup=reply_markup)
    return CHOOSING_SERVICE

# Выбор типа уборки
async def choose_service(update: Update, context):
    context.user_data['service'] = update.message.text
    await update.message.reply_text("Введите адрес, где нужна уборка:")
    return ENTERING_ADDRESS

# Ввод адреса
async def enter_address(update: Update, context):
    context.user_data['address'] = update.message.text
    await update.message.reply_text("Укажите дату и время (например, 25.10.2023 14:00):")
    return CHOOSING_TIME

# Выбор времени
async def choose_time(update: Update, context):
    context.user_data['time'] = update.message.text
    order_summary = (
        f"Ваш заказ:\n"
        f"Тип уборки: {context.user_data['service']}\n"
        f"Адрес: {context.user_data['address']}\n"
        f"Дата и время: {context.user_data['time']}\n\n"
        "Всё верно? (Да/Нет)"
    )
    keyboard = [['Да', 'Нет']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(order_summary, reply_markup=reply_markup)
    return CONFIRMATION

# Подтверждение заказа
async def confirm_order(update: Update, context):
    if update.message.text == "Да":
        await update.message.reply_text("Спасибо! Ваш заказ принят. Мы свяжемся с вами для подтверждения.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Давайте начнём заново.")
        return ConversationHandler.END

# Отмена заказа
async def cancel(update: Update, context):
    await update.message.reply_text("Заказ отменён.")
    return ConversationHandler.END

# Запрос отзыва (можно вызвать вручную или настроить таймер)
async def ask_feedback(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("1", callback_data='1'),
         InlineKeyboardButton("2", callback_data='2'),
         InlineKeyboardButton("3", callback_data='3'),
         InlineKeyboardButton("4", callback_data='4'),
         InlineKeyboardButton("5", callback_data='5')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Как вам понравилась уборка? Оцените от 1 до 5:", reply_markup=reply_markup)

# Обработка отзыва
async def handle_feedback(update: Update, context):
    query = update.callback_query
    rating = query.data
    await query.answer()
    await query.edit_message_text(f"Спасибо за оценку: {rating}!")

# Основная функция для запуска бота
def main():
    # Создаем приложение с указанным токеном
    application = Application.builder().token(TOKEN).build()

    # Настройка ConversationHandler для заказа уборки
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('🛒 Заказать уборку'), order_start)],
        states={
            CHOOSING_SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_service)],
            ENTERING_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_address)],
            CHOOSING_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_time)],
            CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_order)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Добавляем обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_feedback))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()