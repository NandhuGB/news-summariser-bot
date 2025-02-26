from dotenv import load_dotenv
import os
import logging
import sys
import asyncio
# Telebot
from aiogram import Bot, Dispatcher, html
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

# Local modules
from NewsBotMediator import NewsBotMediator
load_dotenv()

# API key for news summarization bot
TELEGRAM_BOT_TOKEN = os.getenv("NEWS_SUMMARY_AGENT_BOT")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Api key for telegram bot is missing")

print(f"Telegram bot api:{TELEGRAM_BOT_TOKEN[:5]}******")

# Initialize Aiogram dispatcher
dispatcher = Dispatcher()

# Mediator instance
news_mediator = NewsBotMediator()

# Handlers #

@dispatcher.message(CommandStart())
async def start_command_handler(message: Message):
    """
    Handles the "/start" command.
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! This is a news summarizer powered by OpenAI.")

@dispatcher.message(Command("help"))
async def help_command_handler(message: Message):
    """
    Handles the "/help" command.
    """
    help_text = """
    Here are some useful commands to get the most out of this bot:
    /start  - Start the news summarizer bot
    /help   - Get help with available commands
    /headline - Get a summary of top news headlines
    """
    await message.answer(help_text)

@dispatcher.message(Command("headline"))
async def headline_summary_handler(message: Message):
    """
    Returns a summary of general news headlines.
    """
    summary = news_mediator.fetch_headlines()
    await message.answer(summary)

@dispatcher.message()
async def news_query_handler(message: Message):
    """
    Handles user queries by summarizing related news.
    """
    summary = news_mediator.fetch_query_based_news(str(message.text))
    await message.answer(summary)

async def main():
    """
    Main function to start the bot.
    """
    bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

