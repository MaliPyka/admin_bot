from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

builder = InlineKeyboardBuilder()

class AdminAction(CallbackData, prefix="adm"):
    action: str
    user_id: int
    reason_code: int



builder.button(
    text="Забанить",
    callback_data=AdminAction(action="ban", user_id=555, reason_code=1)
)