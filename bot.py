from telegram.ext import *
from telegram import *
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument
import os
from google.colab import drive
drive.mount('/content/gdrive')
DIALOGFLOW_PROJECT_ID = 'shop-bot-hpur(!!Вставить свой ID!!)'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'current-user-id'
credential_path = "/content/google-credentialsa.json
(!!Вставить свой файл.json!!)"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
def start(update, context):
update.message.reply_text("Hi! I am a bot with Google Dialogflow")
def echo(update, context):
text_to_be_analyzed = update.message.text
session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID,
SESSION_ID)
text_input = dialogflow.TextInput(text=text_to_be_analyzed,
language_code=DIALOGFLOW_LANGUAGE_CODE)
query_input = dialogflow.QueryInput(text=text_input)
try:
try:
response = session_client.detect_intent(session=session,
query_input=query_input)
except InvalidArgument:
update.message.reply_text('Something went wrong')
return
update.message.reply_text
(response.query_result.fulfillment_text)
except Exception as err:
update.message.reply_text(err)
def main():
updater = Updater("81335677111:AAGEXGLR45az3vr-mFcnERTZRAJLGdgtTpU"
(!!Вставить свой Bot-ID!!))
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text, echo))
# Start the Bot
updater.start_polling()
updater.idle()
if __name__ == '__main__':
main()