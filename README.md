# 📢 Telegram News Summarization Bot  

## Overview  
This bot fetches and summarizes news articles based on user queries. It integrates NewsAPI, OpenAI’s GPT models, and Retrieval-Augmented Generation (RAG) to provide concise and relevant news summaries directly in Telegram.  

## Features  
- 📰 **Headline Summarization** – Fetch and summarize the latest headlines.  
- 🔍 **Query-Based News** – Retrieve and summarize news articles based on user input.  
- 🧠 **Retrieval-Augmented Generation (RAG)** – Improves summarization with vector-based search.  
- 🤖 **AI-Powered Summarization** – Uses OpenAI’s GPT for concise news summaries.  
- 🏗 **Factory Design Pattern** – Modular and scalable architecture.  

## Tech Stack  
- **Python** (aiogram, OpenAI API, langchain, newspaper3k, chromadb)  
- **Telegram Bot API**  
- **NewsAPI** for fetching articles  
- **ChromaDB** for vectorized storage and retrieval  
- **LangChain** for efficient text processing
- **Docker** for containerized deployment  

## Setup

### 1️⃣ Prerequisites  
- Python 3.8+  
- A Telegram bot token from [BotFather](https://t.me/BotFather)  
- NewsAPI API key from [NewsAPI.org](https://newsapi.org)  
- OpenAI API key from [OpenAI](https://platform.openai.com/signup/)
- Docker (for containerized deployment)  

### 2️⃣ Installation  
Clone the repository and install dependencies:  
```bash
git clone https://github.com/NandhuGB/news-summariser-bot.git
cd telegram-news-bot
pip install -r requirements.txt
```

### 3️⃣ Configuration  
Create a `.env` file with:  
```env
NEWSAPI_KEY=your_newsapi_key
OPENAI_API_KEY=your_openai_api_key
NEWS_SUMMARY_AGENT_BOT=your_telegram_bot_token
```

### 4️⃣ Run the Bot  
```bash
python main.py
```

## Dockerized Branch
A dedicated `dockerized` branch contains the latest updates for seamless containerization. To switch to it:  
```bash
git checkout dockerized
```

## Usage  
- **`/start`** – Start the bot  
- **`/help`** – List available commands  
- **`/headline`** – Get a summary of the latest news headlines  
- **Query message** – Send any text query to get a news summary  

## Project Structure  
```
📂 telegram-news-bot  
 ├── 📜 main.py            # Bot entry point  
 ├── 📜 NewsBotMediator.py # Manages bot interaction  
 ├── 📜 NewsFetcher.py     # Fetches news using NewsAPI  
 ├── 📜 RagNews.py         # Implements RAG for summarization  
 ├── 📜 TextSummarizer.py  # Summarization pipeline with OpenAI  
 ├── 📜 requirements.txt   # Dependencies  
 ├── 📜 .env.example       # Environment variables template  
 └── 📜 README.md          # Project documentation  
```

## Contributing  
Feel free to fork the repo and submit pull requests! 🚀  

## License  
This project is licensed under the MIT License.  
