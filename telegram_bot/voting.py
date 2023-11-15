from typing import Iterable
import aiosqlite
import config

from telegram_bot.users import _insert_user


async def get_actual_voting_id() -> int or None:
    sql = """
        SELECT id, voting_start, voting_finish
        FROM voting
        WHERE voting_start <= current_date
            AND voting_finish >= current_date
        ORDER BY voting_start
        LIMIT 1
    """
    async with aiosqlite.connect(config.SQLITE_DB) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(sql) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None
            return row["id"]


async def save_vote(telegram_user_id: int, books: Iterable[Book]):
    _insert_user(telegram_user_id)
