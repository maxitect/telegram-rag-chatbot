from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()


async def mirror_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    await update.message.reply_text(message_text)

app = ApplicationBuilder().token(os.getenv('TELEGRAM_CHATBOT_API_KEY')).build()
app.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND, mirror_message))
app.run_polling()
