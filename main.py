import asyncio
import logging
from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv
import os
from handlers.ask_join_handler import router as ask_router
from handlers.approve_join_handler import router as approve_router
load_dotenv()
token = os.getenv("TOKEN")
bot = Bot(token=token)

dp = Dispatcher()
async def main():
    logging.basicConfig(level=logging.INFO)
    #dp.include_router(ask_router)
    dp.include_router(approve_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())