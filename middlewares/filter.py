import string

from aiogram import BaseMiddleware



def load_restricted_words():
    try:
        with open('restricted_words.txt', 'r', encoding='utf-8') as f:
            print("Restricted words loaded")
            return {line.strip().lower() for line in f if line.strip()}
    except FileNotFoundError:
        print("Файл restricted_words.txt не найден! Создаю пустой список.")
        return set()

RESTRICTED_WORDS = load_restricted_words()

class Filter(BaseMiddleware):
    async def __call__(self, handler, event, data):
        clean_text = event.text.lower().translate(str.maketrans('', '', string.punctuation))
        words = set(clean_text.split())

        if words & RESTRICTED_WORDS:
            await event.delete()
            await event.answer(f"{event.from_user.mention_html()}, мат запрещен!", parse_mode="html")
            return

        return await handler(event, data)