from aiogram import Router, F
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import Message
import os


admin_router = Router()


class IsAdmin(Filter):
    def __init__(self) -> None:
        self.admin_id = int(os.getenv("ADMIN_ID"))

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == self.admin_id

admin_router.message.filter(IsAdmin(), F.chat.type == "private")


@admin_router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("Доступ разрешен. Привет, Босс!")


