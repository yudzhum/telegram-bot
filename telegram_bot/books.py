from dataclasses import dataclass
from datetime import datetime
from typing import List

import aiosqlite

import config


@dataclass
class Book:
    id: int
    category_id: int
    read_start: datetime
    read_finish: datetime


@dataclass
class Category:
    id: int
    books: List[Book]


async def get_all_books() -> List[Category]:
    async with aiosqlite.connect(config.SQLITE_DB) as db:
        async with db.execute("") as cursor:
            async for row in cursor:
                pass
