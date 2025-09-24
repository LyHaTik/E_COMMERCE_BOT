import asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import logging

from auth import bot
from handlers import routers
from shared.db import create_tables_if_not_exist


logging.basicConfig(level=logging.INFO)

async def main():
    await create_tables_if_not_exist()
    
    dp = Dispatcher(storage=MemoryStorage())
    for router in routers:
        dp.include_router(router)
    
    logging.info("Starting bot")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
