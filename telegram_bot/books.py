from dataclasses import dataclass
from datetime import datetime
from typing import List

import aiosqlite

import config


@dataclass
class Book:
    id: int
    category_id: int
    category_name: str
    read_start: datetime
    read_finish: datetime


@dataclass
class Category:
    id: int
    books: List[Book]


async def get_all_books() -> List[Category]:
    books = []
    async with aiosqlite.connect(config.SQLITE_DB) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(""" SELECT
            b.id as book_id,
            b.name as book_name,
            c.id as category_id,
            c.name as category_name,
            b.read_start,
            b.read_finish
        FROM book as b
        LEFT JOIN book_category c ON c.id=b.category_id
    """) as cursor:
            async for row in cursor:
                books.append(Book(
                    id=row["book_id"],
                    name=row["book_name"],
                    category_id=row["category_id"],
                    category_name=row["category_name"],
                    read_start=row["read_start"],
                    read_finish=row["read_finish"],
                ))
    return books
