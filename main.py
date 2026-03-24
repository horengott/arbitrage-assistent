import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.user import router
from dotenv import load_dotenv
from exchange.fetcher import reload_markets
from db.database import init_db

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')


bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def main():
    await init_db()
    
    dp.include_router(router)
    await reload_markets()
    await dp.start_polling(bot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())