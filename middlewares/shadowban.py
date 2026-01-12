from aiogram import BaseMiddleware

class ShadowBan(BaseMiddleware):
    async def __call__(self, handler, event, data):
        black_list = []
        if event.from_user.id in black_list:
            return
        else:
            return await handler(event, data)
