import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.user import router
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')


bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())