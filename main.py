import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from database.models import init_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.orm_query import check_and_reset_warns
from middlewares.admin import AdminMiddleware

load_dotenv()

from handlers.admin_private import admin_router
from handlers.user_group import user_group_router

scheduler = AsyncIOScheduler()

async def on_startup(bot: Bot):
    await init_db()

    scheduler.add_job(check_and_reset_warns, "interval", hours = 1)
    scheduler.start()



bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

dp.include_router(admin_router)
dp.include_router(user_group_router)

user_group_router.message.middleware(AdminMiddleware())

async def main():
    print("Бот запущен!")

    dp.startup.register(on_startup)


    await bot.delete_webhook(drop_pending_updates=True)
    await init_db()                          # создаем бд
    await dp.start_polling(bot)






if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")