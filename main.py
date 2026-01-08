import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

from handlers.admin_private import admin_router
from handlers.user_group import user_group_router



bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

dp.include_router(admin_router)
dp.include_router(user_group_router)

async def main():
    print("Бот запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")