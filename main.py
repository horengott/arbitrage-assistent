import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message


bot = Bot(token='8092966537:AAEoEpxhMAqXuCWkmkZ-slnF5EHRZcRX4TY')
dp = Dispatcher()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())