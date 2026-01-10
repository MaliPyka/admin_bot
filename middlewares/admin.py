from typing import Any, Dict, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

class AdminMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ) -> Any:
        member = await event.bot.get_chat_member(event.chat.id, event.from_user.id)
        is_admin = member.status in ['administrator', 'creator']

        data["is_admin_check"] = is_admin
        return await handler(event, data)