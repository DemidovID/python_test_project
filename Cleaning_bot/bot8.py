import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import asyncio

TOKEN = '7809105311:AAFfNc7nuO9lQuB8CFWuhXmtX59ZooblUM4'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    logger.debug("Команда /start вызвана")
    keyboard = [[InlineKeyboardButton("🧹 Тест", callback_data='test_button')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нажми кнопку:", reply_markup=reply_markup)

async def button_handler(update: Update, context):
    query = update.callback_query
    logger.debug(f"Callback получен: {query.data}")
    await query.answer()
    await query.edit_message_text("Кнопка нажата!")

async def reset_webhook(app):
    await app.bot.setWebhook("")
    logger.info("Webhook сброшен")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Бот запущен")

    await reset_webhook(app)
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())