from typing import Any
from aiogram import BaseMiddleware

class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data) -> Any:
        member = await event.bot.get_chat_member(event.chat.id, event.from_user.id)
        is_admin = member.status in ['administrator', 'creator']

        data["is_admin_check"] = is_admin
        return await handler(event, data)


