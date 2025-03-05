import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler

# Укажите токен вашего бота
TOKEN = '7809105311:AAFfNc7nuO9lQuB8CFWuhXmtX59ZooblUM4'

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Состояния для заказа
CHOOSING_SERVICE, ENTERING_ADDRESS, CHOOSING_TIME, CONFIRMATION = range(4)

# Постоянная клавиатура
MAIN_MENU_KEYBOARD = [['🧹 Услуги', '🛒 Заказать'], ['💬 Поддержка', '📖 История']]
MAIN_MENU_MARKUP = ReplyKeyboardMarkup(MAIN_MENU_KEYBOARD, resize_keyboard=True)

# Команда /start
async def start(update: Update, context):
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} начал чат")
    welcome_text = (
        "🌟 Добро пожаловать в CleanBot! 🌟\n"
        "Я помогу вам заказать уборку, узнать об услугах и не только. "
        "Выберите действие из меню ниже:"
    )
    await update.message.reply_text(welcome_text, reply_markup=MAIN_MENU_MARKUP)

# Обработка меню
async def handle_menu(update: Update, context):
    text = update.message.text
    if text == '🧹 Услуги':
        await show_services(update, context)
    elif text == '🛒 Заказать':
        return await order_start(update, context)
    elif text == '💬 Поддержка':
        await update.message.reply_text("📞 Свяжитесь с нами: +7 999 123-45-67")
    elif text == '📖 История':
        await show_history(update, context)
    else:
        await update.message.reply_text("Выберите действие из меню ниже.")

# Показ услуг
async def show_services(update: Update, context):
    services_text = (
        "Наши услуги:\n"
        "1. Стандартная уборка — 2000 руб.\n"
        "2. Генеральная уборка — 5000 руб.\n"
        "3. Уборка после ремонта — 7000 руб."
    )
    keyboard = [
        [InlineKeyboardButton("Подробнее о Стандартной", callback_data='info_standard')],
        [InlineKeyboardButton("Подробнее о Генеральной", callback_data='info_general')],
        [InlineKeyboardButton("Подробнее о После ремонта", callback_data='info_after_repair')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(services_text, reply_markup=reply_markup)

# Информация об услуге
async def service_info(update: Update, context):
    query = update.callback_query
    await query.answer()
    service_map = {
        'info_standard': "Стандартная уборка: уборка пыли, полов, сантехники.",
        'info_general': "Генеральная уборка: глубокая чистка всего дома.",
        'info_after_repair': "Уборка после ремонта: удаление строительной пыли."
    }
    await query.edit_message_text(service_map[query.data])

# Начало заказа
async def order_start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Стандартная", callback_data='service_standard')],
        [InlineKeyboardButton("Генеральная", callback_data='service_general')],
        [InlineKeyboardButton("После ремонта", callback_data='service_after_repair')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите тип уборки:", reply_markup=reply_markup)
    return CHOOSING_SERVICE

# Выбор типа уборки
async def choose_service(update: Update, context):
    query = update.callback_query
    await query.answer()
    service_map = {
        'service_standard': 'Стандартная',
        'service_general': 'Генеральная',
        'service_after_repair': 'После ремонта'
    }
    context.user_data['service'] = service_map[query.data]
    await query.edit_message_text("Введите адрес для уборки:")
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
        f"Тип: {context.user_data['service']}\n"
        f"Адрес: {context.user_data['address']}\n"
        f"Время: {context.user_data['time']}\n"
        "Подтверждаете?"
    )
    keyboard = [
        [InlineKeyboardButton("Да", callback_data='confirm_yes'),
         InlineKeyboardButton("Нет", callback_data='confirm_no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(order_summary, reply_markup=reply_markup)
    return CONFIRMATION

# Подтверждение заказа
async def confirm_order(update: Update, context):
    query = update.callback_query
    await query.answer()
    if query.data == 'confirm_yes':
        await query.edit_message_text("Заказ принят! Скоро с вами свяжемся.")
    else:
        await query.edit_message_text("Заказ отменён.")
    return ConversationHandler.END

# История заказов
async def show_history(update: Update, context):
    await update.message.reply_text("История заказов:\n1. Генеральная, 15.10.2023")

# Отмена
async def cancel(update: Update, context):
    await update.message.reply_text("Заказ отменён.")
    return ConversationHandler.END

# Основная функция
def main():
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('🛒 Заказать'), order_start)],
        states={
            CHOOSING_SERVICE: [CallbackQueryHandler(choose_service)],
            ENTERING_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_address)],
            CHOOSING_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_time)],
            CONFIRMATION: [CallbackQueryHandler(confirm_order)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    application.add_handler(CallbackQueryHandler(service_info, pattern='info_'))
    application.run_polling()

if __name__ == '__main__':
    main()