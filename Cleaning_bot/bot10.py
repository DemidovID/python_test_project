import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler

# Токен бота
TOKEN = '7943324084:AAHEXI3nIKDVcOvXiVROuCA50g5sPT7cVHk'

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

CHOOSING_SERVICE, ENTERING_ADDRESS, CHOOSING_TIME, CONFIRMATION = range(4)

MAIN_MENU_KEYBOARD = [['🧹 Услуги', '🛒 Заказать'], ['💬 Поддержка', '📖 История']]
MAIN_MENU_MARKUP = ReplyKeyboardMarkup(MAIN_MENU_KEYBOARD, resize_keyboard=True)

async def start(update: Update, context):
    await update.message.reply_text(
        "👋 Добро пожаловать в CleanBot!\nВыберите действие:",
        reply_markup=MAIN_MENU_MARKUP
    )

async def handle_menu(update: Update, context):
    text = update.message.text
    if text == '🧹 Услуги':
        await show_services(update, context)
    elif text == '🛒 Заказать':
        return await order_start(update, context)
    elif text == '💬 Поддержка':
        await update.message.reply_text("📞 Поддержка: +7 999 123-45-67")
    elif text == '📖 История':
        await update.message.reply_text("📖 История заказов пока пуста.")

async def show_services(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🧹 Стандартная", callback_data='info_standard')],
        [InlineKeyboardButton("🔍 Генеральная", callback_data='info_general')],
        [InlineKeyboardButton("🏠 После ремонта", callback_data='info_after_repair')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if isinstance(update, Update) and update.message:  # Если это сообщение от пользователя
        await update.message.reply_text("Выберите услугу:", reply_markup=reply_markup)
    else:  # Если это callback-запрос
        await update.callback_query.edit_message_text("Выберите услугу:", reply_markup=reply_markup)

async def service_info(update: Update, context):
    query = update.callback_query
    await query.answer()

    services = {
        'info_standard': "🧹 Стандартная уборка: 2000 руб.\n- Пыль\n- Полы\n- Сантехника",
        'info_general': "🔍 Генеральная уборка: 5000 руб.\n- Окна\n- Мебель\n- Глубокая чистка",
        'info_after_repair': "🏠 Уборка после ремонта: 7000 руб.\n- Пыль\n- Строительные остатки\n- Окна"
    }
    text = services.get(query.data, "Услуга не найдена")

    keyboard = [
        [InlineKeyboardButton("🔙 Назад", callback_data='back_services')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text, reply_markup=reply_markup)

async def go_back(update: Update, context):
    query = update.callback_query
    await query.answer()
    # Редактируем текущее сообщение, возвращая список услуг
    keyboard = [
        [InlineKeyboardButton("🧹 Стандартная", callback_data='info_standard')],
        [InlineKeyboardButton("🔍 Генеральная", callback_data='info_general')],
        [InlineKeyboardButton("🏠 После ремонта", callback_data='info_after_repair')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Выберите услугу:", reply_markup=reply_markup)

async def order_start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🧹 Стандартная", callback_data='service_standard')],
        [InlineKeyboardButton("🔍 Генеральная", callback_data='service_general')],
        [InlineKeyboardButton("🏠 После ремонта", callback_data='service_after_repair')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите услугу:", reply_markup=reply_markup)
    return CHOOSING_SERVICE

async def choose_service(update: Update, context):
    query = update.callback_query
    await query.answer()
    service_map = {
        'service_standard': 'Стандартная уборка',
        'service_general': 'Генеральная уборка',
        'service_after_repair': 'Уборка после ремонта'
    }
    context.user_data['service'] = service_map.get(query.data)
    await query.edit_message_text(f"Вы выбрали: {context.user_data['service']}\nВведите адрес:")
    return ENTERING_ADDRESS

async def enter_address(update: Update, context):
    context.user_data['address'] = update.message.text
    await update.message.reply_text("Введите дату и время (например, 01.03.2025 14:00):")
    return CHOOSING_TIME

async def choose_time(update: Update, context):
    context.user_data['time'] = update.message.text
    summary = (
        f"Ваш заказ:\n"
        f"🧹 Услуга: {context.user_data['service']}\n"
        f"📍 Адрес: {context.user_data['address']}\n"
        f"🕒 Время: {context.user_data['time']}\n\n"
        "Подтвердить заказ?"
    )

    keyboard = [
        [InlineKeyboardButton("✅ Подтвердить", callback_data='confirm_yes')],
        [InlineKeyboardButton("❌ Отменить", callback_data='confirm_no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(summary, reply_markup=reply_markup)
    return CONFIRMATION

async def confirm_order(update: Update, context):
    query = update.callback_query
    await query.answer()
    if query.data == 'confirm_yes':
        await query.edit_message_text("✅ Заказ подтверждён! Ожидайте звонка.")
    else:
        await query.edit_message_text("❌ Заказ отменён.")
    return ConversationHandler.END

async def cancel(update: Update, context):
    await update.message.reply_text("🚫 Заказ отменён.", reply_markup=MAIN_MENU_MARKUP)
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('🛒 Заказать'), order_start)],
        states={
            CHOOSING_SERVICE: [CallbackQueryHandler(choose_service, pattern='^service_')],
            ENTERING_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_address)],
            CHOOSING_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_time)],
            CONFIRMATION: [CallbackQueryHandler(confirm_order, pattern='^confirm_')]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(service_info, pattern='^info_'))
    app.add_handler(CallbackQueryHandler(go_back, pattern='^back_services'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    app.run_polling()

if __name__ == '__main__':
    main()