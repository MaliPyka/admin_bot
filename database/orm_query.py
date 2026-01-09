import aiosqlite
from database.models import get_db
import time



async def add_user(user_id):
    async with get_db() as db:
        await db.execute("""
        INSERT OR IGNORE INTO users_warns (user_id) VALUES (?)""", (user_id,))
        await db.commit()


async def get_warns(user_id):
    async with get_db() as db:
        cursor = await db.execute("""SELECT (warns) FROM users_warns WHERE user_id = ?""", (user_id,))
        row = await cursor.fetchone()
        return row[0] if row else 0


async def update_warns(warn,cur_time, user_id):
    async with get_db() as db:
        await db.execute("""
        UPDATE users_warns SET warns = ?, last_warn_time = ? WHERE user_id = ?""", (warn,cur_time,user_id))
        await db.commit()

async def check_and_reset_warns():
    threshold = int(time.time()) - 30#86400 # Время 24 часа назад
    async with get_db() as db:
        # Ищем тех, у кого есть варны и последний был давно
        await db.execute("""
            UPDATE users_warns 
            SET warns = warns - 1, last_warn_time = ? 
            WHERE warns > 0 AND last_warn_time < ?
        """, (int(time.time()), threshold))
        await db.commit()




