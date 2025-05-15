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
from chroma_module import ChromaModule
import os

load_dotenv()

openai_module = OpenAIModule()
chroma_module = ChromaModule()


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    message_text = update.message.text
    response = openai_module.get_response(message_text)
    await update.message.reply_text(response)


async def query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query_text = ' '.join(context.args) if context.args else ""

    if not query_text:
        await update.message.reply_text(
            "Usage: /query <search terms> [number]"
        )
        return

    parts = query_text.split()
    n_results = 5
    if parts and parts[-1].isdigit():
        n_results = int(parts[-1])
        query_text = " ".join(parts[:-1])

    results = chroma_module.query_documents(query_text, n_results=n_results)

    response = f"Search Results ({len(results)}):\n\n"
    for i, result in enumerate(results, 1):
        source = result['metadata']['source']
        content = result['content'][:200] + \
            "..." if len(result['content']) > 200 else result['content']
        response += f"{i}. From {source}:\n{content}\n\n"

    await update.message.reply_text(response)


async def code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "https://github.com/maxitect/telegram-rag-chatbot"
    )

app = ApplicationBuilder().token(os.getenv('TELEGRAM_CHATBOT_API_KEY')).build()
app.add_handler(CommandHandler("code", code))
app.add_handler(CommandHandler("query", query))
app.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
