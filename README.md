# 📰 News Summarizer Bot (Dockerized)

This is a Dockerized News Summarizer Bot that fetches and summarizes news articles using APIs like News API, OpenAI, and Telegram Bot API.

## 📌 Features

Fetches news from News API

Uses OpenAI API for summarization

Sends summarized news via Telegram Bot

Fully Dockerized for easy deployment

## 🚀 Getting Started

1️⃣ Clone the Repository & Switch to Dockerized Branch
```shell
git clone https://github.com/NandhuGB/news-summarizer-bot.git
cd news-summarizer-bot
git checkout dockerized
```

2️⃣ Download Docker Image from Docker Hub

The Docker image is available on Docker Hub:

🔹 Docker Hub Repository

Pull the image using:
```shell
docker pull nandhugb/news-summarizer-bot:latest
```

3️⃣ Create a .env File

Before running the bot, create a .env file in the project directory and add your API keys:
```python
NEWSAPI_KEY=your_newsapi_key
OPENAI_API_KEY=your_openai_api_key
NEWS_SUMMARY_AGENT_BOT=your_telegram_bot_token
```

4️⃣ Run the Container with Custom .env File

```shell
docker run --env-file .env nandhugb/news-summarizer-bot
```
🔹 This will start the bot inside a Docker container and load your API keys from .env.

5️⃣ Using Docker Compose (Optional)

If you prefer Docker Compose, create a docker-compose.yml file:
```python
version: '3.8'
services:
  news_bot:
    image: nandhugb/news-summarizer-bot:latest
    env_file:
      - .env
    restart: always
```

Run it with:
```shell
docker-compose up --build
```
🛑 Stopping the Container

To stop a running container:
```shell
docker ps   # Find the container ID
docker stop <container_id>
```
## 📜 License

This project is licensed under the MIT License.
