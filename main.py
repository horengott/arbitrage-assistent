import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers.user import router


bot = Bot(token='8092966537:AAEoEpxhMAqXuCWkmkZ-slnF5EHRZcRX4TY')
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())