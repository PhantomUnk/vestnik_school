import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from handlers.homework.homework import homework_router
from handlers.schedule.schedule import schedule_router

from utils import get_keyboard

load_dotenv()

TOKEN = getenv("TOKEN", "")

dp = Dispatcher()

dp.include_router(homework_router)
dp.include_router(schedule_router)

ADMINS = [1890754637, 6256796672, 1866532717]

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    kb = get_keyboard(message.from_user.id, ADMINS) # type: ignore
    await message.answer(
        f"Привет, {message.from_user.full_name}!", # type: ignore
        reply_markup=kb
    ) 


async def main() -> None:
    bot = Bot(
        token=TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s [%(levelname)s] %(message)s",  # <-- добавили время
        datefmt="%Y-%m-%d %H:%M:%S"  # <-- формат времени
    )
    asyncio.run(main())
