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

# api_key for news_summary_agent
telebot_token = os.getenv("news_summary_agent_bot")

# Aiogram dispatcher connection
dp = Dispatcher()

# Mediator instance
mediator = NewsBotMediator()

# Handlers #

# /start handler
@dp.message(CommandStart())
async def command_start_handler(message:Message):
    """
    This handles the first message after the "/start"
    """

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! This is news summariser powered by opeai.")

# /help handler
@dp.message(Command("help"))
async def help_handler(message:Message):
    """
    This handles the command /help
    """
    text = """
    Here is some usefull commands to get more out this bot:
    /start  - To getting started with news summariser
    /help   - To get help
    /option - To get list of all available options
    /info   - To get current options / Default options
    """
    await message.answer(text)


# /option handler
@dp.message(Command("option"))
async def info_handler(message:Message):
    """
    This handles the command "/info"
    """
    text = "this is a infomer"
    await message.answer(text)


# /headline handler
@dp.message(Command("headline"))
async def headline_summary(message:Message):
  """
  This will return general healine
  """

  summary = mediator.headlines()
  await message.answer(summary)



# News Query Handler
@dp.message()
async def echo_handler(message:Message):
    """
    This handles any receiving message, except for the first message. This replies the same message back to the user
    """

    summary = mediator.query(str(message.text))
    await message.answer(summary)


@dp.message()
async def main():
    bot = Bot(token = telebot_token, default =DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__=="__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())