from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
    CommandHandler,
)
from dotenv import load_dotenv
import os

load_dotenv()


async def mirror(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    await update.message.reply_text(message_text)


async def code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("https://github.com/maxitect/telegram-rag-chatbot")

app = ApplicationBuilder().token(os.getenv('TELEGRAM_CHATBOT_API_KEY')).build()
app.add_handler(CommandHandler("code", code))
app.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND, mirror))
app.run_polling()
