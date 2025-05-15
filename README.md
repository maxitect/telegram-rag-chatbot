# Telegram RAG Chatbot

A Telegram bot with retrieval-augmented generation (RAG) capabilities using ChromaDB and OpenAI.

## Setup

### 1. Clone the Repository

**HTTPS:**

```bash
git clone https://github.com/maxitect/telegram-rag-chatbot.git
cd telegram-rag-chatbot
```

**SSH:**

```bash
git clone git@github.com:maxitect/telegram-rag-chatbot.git
cd telegram-rag-chatbot
```

### 2. Create Telegram Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Choose a name for your bot
4. Choose a username ending in `bot`
5. Save the API token provided

### 3. Environment Setup

Create a `.env` file:

```
TELEGRAM_CHATBOT_API_KEY=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Install Dependencies

```bash
conda env create -f environment.yml
conda activate telegram-bot
```

### 5. Prepare Documents

1. Create a `docs/` folder
2. Add your Markdown files to index
3. Run the ingestion script:

```bash
python ingest_docs.py
```

### 6. Run the Bot

```bash
python main.py
```

## Commands

- `/query <search terms>` - Search the document database
- `/code` - Get the GitHub repository link
- Regular messages are answered using RAG with context from the documents
