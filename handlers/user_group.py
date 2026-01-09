import asyncio
import string
import time

from aiogram import Router, F, Bot
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command
from datetime import datetime, timedelta
from database.orm_query import add_user, update_warns, get_warns
from utils.logging_utils import send_log


user_group_router = Router()

def load_restricted_words():
    try:
        with open('restricted_words.txt', 'r', encoding='utf-8') as f:
            # Читаем, убираем лишние пробелы и пустые строки
            return {line.strip().lower() for line in f if line.strip()}
    except FileNotFoundError:
        print("Файл restricted_words.txt не найден! Создаю пустой список.")
        return set()

RESTRICTED_WORDS = load_restricted_words()

async def is_admin(message: Message, bot: Bot) -> bool:
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ["creator", "administrator"]



@user_group_router.message(Command("ban"))
async def ban_cmd(message: Message, bot: Bot):
    if message.reply_to_message:
        if await is_admin(message, bot):
            try:
                await message.chat.ban(message.reply_to_message.from_user.id)
                bot_msg = await message.answer(f"{message.reply_to_message.from_user.mention_html()} забанен!", parse_mode="HTML")
                await asyncio.sleep(5)
                await bot_msg.delete()
            except Exception:
                bot_msg = await message.answer("Не могу забанить этого пользователя!")
                await asyncio.sleep(5)
                await bot_msg.delete()



@user_group_router.message(Command("mute"))
async def mute_cmd(message: Message, bot: Bot):
    mute = ChatPermissions(can_send_messages=False)
    dt = datetime.now() + timedelta(seconds=30)
    if message.reply_to_message:
        if await is_admin(message, bot):
            try:
                await message.chat.restrict(
                    user_id= message.reply_to_message.from_user.id,
                    permissions=mute,
                    until_date=dt)
                bot_msg = await message.answer(f"Пользователь {message.reply_to_message.from_user.mention_html()} "
                                    f"замучен на 30 секунд.", parse_mode="HTML")
                await asyncio.sleep(5)
                await bot_msg.delete()
            except Exception as e:
                await message.answer(f"Пользователя {message.reply_to_message.from_user.mention_html()} "
                                     f"нельзя замутить", parse_mode="HTML")

@user_group_router.message(Command("unmute"))
async def unmute_cmd(message: Message, bot: Bot):
    unmute = ChatPermissions(can_send_messages=True)
    if message.reply_to_message:
        if await is_admin(message, bot):
            await message.chat.restrict(user_id= message.reply_to_message.from_user.id, permissions=unmute)
            bot_msg = await message.answer(f"Пользователь {message.reply_to_message.from_user.mention_html()} "
                                 f"размучен", parse_mode="HTML")
            await asyncio.sleep(5)
            await bot_msg.delete()


@user_group_router.message(Command("warn"))
async def warn_cmd(message: Message, bot: Bot):
    if message.reply_to_message:
        if await is_admin(message, bot):
            user_id = int(message.reply_to_message.from_user.id)
            cur_warn = await get_warns(user_id)
            warn = cur_warn + 1
            cur_time = int(time.time())
            if warn >= 3:
                try:
                    await message.chat.ban(user_id=user_id)
                    await message.answer(f"Пользователь {message.reply_to_message.from_user.mention_html()} "
                                 f"забанен за многократные нарушения правил чата", parse_mode="HTML")
                    await update_warns(0, user_id)
                except Exception as e:
                    await message.answer(f"Пользователя {message.reply_to_message.from_user.mention_html()} "
                                 f"нельзя забанить", parse_mode="HTML")
            else:
                await update_warns(warn,cur_time, user_id)
                await message.answer(f"Пользователь {message.reply_to_message.from_user.mention_html()} "
                                     f"получил {warn} предупреждение", parse_mode="HTML")
                await send_log(bot,f"Админ {message.from_user.mention_html()} выдал варн {message.reply_to_message.from_user.mention_html()}")

@user_group_router.message(Command("unwarn"))
async def unwarn_cmd(message: Message, bot: Bot):
    if message.reply_to_message:
        if await is_admin(message, bot):
            cur_warn = await get_warns(message.reply_to_message.from_user.id)
            if cur_warn == 0:
                return
            cur_time = int(time.time())
            warn = cur_warn - 1
            await update_warns(warn,cur_time, message.reply_to_message.from_user.id)
            await message.answer(f"C пользователя {message.reply_to_message.from_user.mention_html()} "
                                     f"снято предупреждение, на данный момент у него {warn} предупреждений!", parse_mode="HTML")
            await send_log(bot,f"Админ {message.from_user.mention_html()} снял варн с {message.reply_to_message.from_user.mention_html()}")




@user_group_router.message(F.text)
@user_group_router.edited_message(F.text)
async def clear_text(message: Message, bot: Bot):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    await add_user(message.from_user.id)

    if member.status in ["creator", "administrator"]:
        return
    text_clean = message.text.lower().translate(str.maketrans('', '', string.punctuation))
    words = text_clean.split()

    if any(word in RESTRICTED_WORDS for word in words):
        await message.delete()
        warning = await message.answer(
         f"{message.from_user.mention_html()}, мат запрещен!",
            parse_mode="HTML"
        )
        await asyncio.sleep(5)
        await warning.delete()



