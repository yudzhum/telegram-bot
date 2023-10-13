from dataclasses import dataclass
from datetime import datetime
from typing import List

import aiosqlite

import config


def _chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


@dataclass
class Book:
    id: int
    name: str
    category_id: int
    category_name: str or None
    read_start: datetime or None
    read_finish: datetime or None


@dataclass
class Category:
    id: int
    name: str
    books: List[Book]


async def get_all_books(chunk_size: int) -> List[Category]:
    books = []
    async with aiosqlite.connect(config.SQLITE_DB) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""SELECT      
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
    return _chunks(books, chunk_size)
