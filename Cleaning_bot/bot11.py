import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler

# Токен бота (замените на свой)
TOKEN = '7943324084:AAHEXI3nIKDVcOvXiVROuCA50g5sPT7cVHk'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Состояния диалога
CHOOSING_SERVICE, ENTERING_ADDRESS, CHOOSING_TIME, CONFIRMATION = range(4)

# Главное меню
MAIN_MENU_KEYBOARD = [['🧹 Услуги', '🛒 Заказать'], ['💬 Поддержка', '📖 История']]
MAIN_MENU_MARKUP = ReplyKeyboardMarkup(MAIN_MENU_KEYBOARD, resize_keyboard=True)

# Список кнопок главного меню
main_menu_options = ['🧹 Услуги', '🛒 Заказать', '💬 Поддержка', '📖 История']  

# Стартовая команда
async def start(update: Update, context):
    await update.message.reply_text(
        "👋 **Добро пожаловать в CleanBot!**\n"
        "Я помогу вам заказать уборку или узнать больше о наших услугах.\n\n"
        "✨ Выберите действие:",
        reply_markup=MAIN_MENU_MARKUP
    )

# Обработка главного меню
async def handle_menu(update: Update, context):
    text = update.message.text
    if text == '🧹 Услуги':
        await show_services(update, context)
    elif text == '🛒 Заказать':
        return await order_start(update, context)
    elif text == '💬 Поддержка':
        await update.message.reply_text(
            "📞 **Поддержка CleanBot**\n"
            "Свяжитесь с нами: **+7 999 123-45-67**\n"
            "Мы всегда рады помочь! 😊"
        )
    elif text == '📖 История':
        await update.message.reply_text(
            "📖 **История заказов**\n"
            "Пока здесь пусто, но скоро появятся ваши заказы! 😉"
        )
    return ConversationHandler.END

# Показ списка услуг
async def show_services(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🧹 Стандартная", callback_data='info_standard')],
        [InlineKeyboardButton("🔍 Генеральная", callback_data='info_general')],
        [InlineKeyboardButton("🏠 После ремонта", callback_data='info_after_repair')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "🧼 **Наши услуги**\n"
        "Выберите, что вам нужно:"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

# Информация об услуге
async def service_info(update: Update, context):
    query = update.callback_query
    await query.answer()
    services = {
        'info_standard': (
            "🧹 **Стандартная уборка**\n"
            "💰 Цена: 2000 руб.\n"
            "Что входит:\n"
            "- Уборка пыли\n"
            "- Мытьё полов\n"
            "- Чистка сантехники"
        ),
        'info_general': (
            "🔍 **Генеральная уборка**\n"
            "💰 Цена: 5000 руб.\n"
            "Что входит:\n"
            "- Мытьё окон\n"
            "- Чистка мебели\n"
            "- Глубокая уборка"
        ),
        'info_after_repair': (
            "🏠 **Уборка после ремонта**\n"
            "💰 Цена: 7000 руб.\n"
            "Что входит:\n"
            "- Уборка строительной пыли\n"
            "- Удаление остатков\n"
            "- Мытьё окон"
        )
    }
    text = services.get(query.data, "❌ Услуга не найдена")
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_services')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

# Возврат к списку услуг
async def go_back(update: Update, context):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🧹 Стандартная", callback_data='info_standard')],
        [InlineKeyboardButton("🔍 Генеральная", callback_data='info_general')],
        [InlineKeyboardButton("🏠 После ремонта", callback_data='info_after_repair')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "🧼 **Наши услуги**\n"
        "Выберите, что вам нужно:",
        reply_markup=reply_markup
    )

# Начало процесса заказа
async def order_start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🧹 Стандартная", callback_data='service_standard')],
        [InlineKeyboardButton("🔍 Генеральная", callback_data='service_general')],
        [InlineKeyboardButton("🏠 После ремонта", callback_data='service_after_repair')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🛒 **Оформление заказа**\n"
        "Выберите услугу для заказа:",
        reply_markup=reply_markup
    )
    return CHOOSING_SERVICE

# Выбор услуги в заказе
async def choose_service(update: Update, context):
    query = update.callback_query
    await query.answer()
    service_map = {
        'service_standard': 'Стандартная уборка',
        'service_general': 'Генеральная уборка',
        'service_after_repair': 'Уборка после ремонта'
    }
    context.user_data['service'] = service_map.get(query.data)
    await query.edit_message_text(
        f"🧹 **Вы выбрали:** {context.user_data['service']}\n"
        "📍 Введите адрес уборки:"
    )
    return ENTERING_ADDRESS

# Ввод адреса
async def enter_address(update: Update, context):
    text = update.message.text
    if text in main_menu_options:
        context.user_data.clear()  # Очищаем данные заказа
        await handle_menu(update, context)  # Сразу выполняем действие кнопки
        return ConversationHandler.END
    context.user_data['address'] = text
    await update.message.reply_text(
        "📅 Введите дату и время уборки\n"
        "Например: **01.03.2025 14:00**"
    )
    return CHOOSING_TIME

# Выбор времени
async def choose_time(update: Update, context):
    text = update.message.text
    if text in main_menu_options:
        context.user_data.clear()  # Очищаем данные заказа
        await handle_menu(update, context)  # Сразу выполняем действие кнопки
        return ConversationHandler.END
    context.user_data['time'] = text
    summary = (
        "🛒 **Ваш заказ**\n"
        f"🧹 Услуга: **{context.user_data['service']}**\n"
        f"📍 Адрес: **{context.user_data['address']}**\n"
        f"🕒 Время: **{context.user_data['time']}**\n\n"
        "Всё верно?"
    )
    keyboard = [
        [InlineKeyboardButton("✅ Подтвердить", callback_data='confirm_yes')],
        [InlineKeyboardButton("❌ Отменить", callback_data='confirm_no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(summary, reply_markup=reply_markup)
    return CONFIRMATION

# Подтверждение заказа
async def confirm_order(update: Update, context):
    query = update.callback_query
    await query.answer()
    if query.data == 'confirm_yes':
        await query.edit_message_text(
            "✅ **Заказ подтверждён!**\n"
            "Спасибо за выбор CleanBot! Ожидайте звонка для подтверждения. 😊"
        )
    else:
        await query.edit_message_text(
            "❌ **Заказ отменён**\n"
            "Если передумаете, просто нажмите '🛒 Заказать'!"
        )
    context.user_data.clear()
    return ConversationHandler.END

# Отмена заказа командой /cancel
async def cancel(update: Update, context):
    await update.message.reply_text(
        "🚫 **Заказ отменён**\n"
        "Вы вернулись в главное меню.",
        reply_markup=MAIN_MENU_MARKUP
    )
    context.user_data.clear()
    return ConversationHandler.END

# Основная функция
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

    # Обработчики команд и меню
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex('^🧹 Услуги$'), show_services))
    app.add_handler(MessageHandler(filters.Regex('^💬 Поддержка$'), lambda update, context: update.message.reply_text(
        "📞 **Поддержка CleanBot**\n"
        "Свяжитесь с нами: **+7 999 123-45-67**\n"
        "Мы всегда рады помочь! 😊"
    )))
    app.add_handler(MessageHandler(filters.Regex('^📖 История$'), lambda update, context: update.message.reply_text(
        "📖 **История заказов**\n"
        "Пока здесь пусто, но скоро появятся ваши заказы! 😉"
    )))
    app.add_handler(CallbackQueryHandler(service_info, pattern='^info_'))
    app.add_handler(CallbackQueryHandler(go_back, pattern='^back_services'))
    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == '__main__':
    main()