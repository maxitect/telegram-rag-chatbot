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

## Docker Setup

1. **Add your documents** to the `docs/` folder as above (Markdown files)

2. **Build and run:**

   ```bash
   docker-compose up --build -d
   ```

   The container will automatically:

   - Install dependencies
   - Ingest documents from `docs/` folder
   - Start the Telegram bot

3. **Check logs:**

   ```bash
   docker-compose logs -f
   ```

4. **Stop the bot:**
   ```bash
   docker-compose down
   ```

> [!NOTE]
> Document ingestion runs automatically on container startup. The bot will start once ingestion completes.

### Data Persistence

The Docker setup includes persistent volumes for:

- `./docs` - Your markdown documents
- `./chroma_db` - Vector database storage

Your data persists between container restarts.

## Commands

- `/query <search terms>` - Search the document database
- `/code` - Get the GitHub repository link
- Regular messages are answered using RAG with context from the documents
