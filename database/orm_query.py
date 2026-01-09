import aiosqlite
from database.models import get_db



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


async def update_warns(warn, user_id):
    async with get_db() as db:
        await db.execute("""
        UPDATE users_warns SET warns = ? WHERE user_id = ?""", (warn, user_id))
        await db.commit()




