from aiogram import BaseMiddleware
import time


class AntiSpam(BaseMiddleware):

    def __init__(self):
        self.limit = {}

    async def __call__(self, handler, event, data):

        user_id = event.from_user.id

        if user_id not in self.limit:
            self.limit[user_id] = time.time()

        if time.time() - int(self.limit[user_id]) > 0.6:
            return await handler(event, data)
        else:
            await event.delete()
            await event.answer("Не флуди!")
            return


