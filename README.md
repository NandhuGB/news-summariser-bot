📰 News Summarizer Bot (Dockerized)

This is a Dockerized News Summarizer Bot that fetches and summarizes news articles using APIs like News API, OpenAI, and Telegram Bot API.

📌 Features

Fetches news from News API

Uses OpenAI API for summarization

Sends summarized news via Telegram Bot

Fully Dockerized for easy deployment

🚀 Getting Started

1️⃣ Clone the Repository & Switch to Dockerized Branch

git clone https://github.com/your-username/news-summarizer-bot.git
cd news-summarizer-bot
git checkout dockerized

2️⃣ Download Docker Image from Docker Hub

The Docker image is available on Docker Hub:

🔹 Docker Hub Repository

Pull the image using:

docker pull your-dockerhub-username/news-summarizer-bot:latest

3️⃣ Create a .env File

Before running the bot, create a .env file in the project directory and add your API keys:

newsapi-py=your_newsapi_key
openai=your_openai_api_key
news_summary_agent_bot=your_telegram_bot_token

4️⃣ Run the Container with Custom .env File

docker run --env-file .env your-dockerhub-username/news-summarizer-bot

🔹 This will start the bot inside a Docker container and load your API keys from .env.

5️⃣ Using Docker Compose (Optional)

If you prefer Docker Compose, create a docker-compose.yml file:

version: '3.8'
services:
  news_bot:
    image: your-dockerhub-username/news-summarizer-bot:latest
    env_file:
      - .env
    restart: always

Run it with:

docker-compose up --build

🛑 Stopping the Container

To stop a running container:

docker ps   # Find the container ID
docker stop <container_id>

📜 License

This project is licensed under the MIT License.