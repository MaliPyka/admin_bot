import aiosqlite
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "database.db"

DATA_DIR.mkdir(exist_ok=True)

def get_db():
    return aiosqlite.connect(DB_PATH)



async def init_db():
    async with get_db() as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users_warns (
        user_id INTEGER PRIMARY KEY,
        warns INTEGER DEFAULT 0,
        last_warn_time INTEGER DEFAULT 0
        )
        """)
        await db.commit()





