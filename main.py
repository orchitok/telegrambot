import asyncio
import logging
import sys
import os


from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Load tokens
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load tokens
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Set up dispatcher
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Ahoy, {message.from_user.full_name}! Ask me anythin', matey!")


@dp.message()
async def chatgpt_handler(message: Message) -> None:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a coding assistant that talks like a pirate."},
                {"role": "user", "content": message.text},
            ]
        )
        reply = response.choices[0].message.content
        await message.answer(reply)
    except Exception as e:
        await message.answer("Arrr, somethin' went wrong, matey!")
        logging.error(f"OpenAI API error: {e}")


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())