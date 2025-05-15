from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
    CommandHandler,
)
from dotenv import load_dotenv
from openai_module import OpenAIModule
import os

load_dotenv()

openai_module = OpenAIModule()


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    message_text = update.message.text
    response = openai_module.get_response(message_text)
    await update.message.reply_text(response)


async def code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "https://github.com/maxitect/telegram-rag-chatbot"
    )

app = ApplicationBuilder().token(os.getenv('TELEGRAM_CHATBOT_API_KEY')).build()
app.add_handler(CommandHandler("code", code))
app.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
