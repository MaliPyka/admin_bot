import os
from aiogram import Bot

async def send_log(bot: Bot, text: str):
    # Берем ID из .env
    channel_id = os.getenv("LOG_CHANNEL_ID")
    if channel_id:
        try:
            await bot.send_message(chat_id=channel_id, text=text, parse_mode="HTML")
        except Exception as e:
            print(f"Ошибка при отправке лога: {e}")