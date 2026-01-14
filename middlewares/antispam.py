from aiogram import BaseMiddleware
import time


class AntiSpam(BaseMiddleware):
    def __init__(self):
        # Храним время последнего сообщения
        self.limit = {}

    async def __call__(self, handler, event, data):
        user_id = event.from_user.id
        current_time = time.time()

        # Получаем время предыдущего сообщения (если нет — 0)
        last_time = self.limit.get(user_id, 0)

        # Проверяем разницу
        if current_time - last_time < 0.7:
            # ОБЯЗАТЕЛЬНО обновляем время даже при спаме!
            # Это заставляет спамера ждать еще 0.7 сек с момента последней попытки
            self.limit[user_id] = current_time

            # Только удаляем, без .answer (чтобы бот не зависал)
            await event.delete()
            return

            # Если всё хорошо — обновляем время и пропускаем дальше
        self.limit[user_id] = current_time
        return await handler(event, data)


