from dataclasses import dataclass
from datetime import datetime
from typing import List

import aiosqlite

import config


@dataclass
class Book:
    id: int
    name: str
    category_id: int
    category_name: str or None
    read_start: str or None
    read_finish: str or None

    def __post_init__(self):
        """Set up read_start and read_finish to needed string format"""
        for field in ("read_start", "read_finish"):
            value = getattr(self, field)
            if value is None:
                continue
            value = datetime.strptime(value, "%Y-%m-%d").strftime(config.DATE_FORMAT)
            setattr(self, field, value)


@dataclass
class Category:
    id: int
    name: str
    books: List[Book]


def _group_books_by_categoies(books: List[Book]) -> List[Category]:
    categories = []
    category_id = None
    for book in books:
        if category_id != book.category_id:
            categories.append(Category(
                id=book.category_id,
                name=book.category_name,
                books=[book]
            ))
            category_id = book.category_id
            continue
        categories[-1].books.append(book)
    return categories


async def get_all_books() -> List[Category]:
    sql = _get_books_base_sql() + """
        WHERE b.read_start IS NULL
        ORDER BY c."ordering", b."ordering" """
    books = await _get_books_from_db(sql)
    return _group_books_by_categoies(books)


async def get_unread_books() -> List[Category]:
    sql = _get_books_base_sql() + """
        ORDER BY c."ordering", b."ordering" """
    books = await _get_books_from_db(sql)
    return _group_books_by_categoies(books)


async def get_already_readen_books() -> List[Book]:
    sql = _get_books_base_sql() + """
        WHERE read_start < current_date
            AND read_finish <= current_date
        ORDER BY b.read_start"""
    return await _get_books_from_db(sql)


async def get_books_we_reading_now() -> List[Book]:
    sql = _get_books_base_sql() + """
                WHERE read_start <= current_date
                    AND read_finish >= current_date"""
    return await _get_books_from_db(sql)


async def get_books_by_numbers(numbers) -> List[Book]:
    numbers_joined = ", ".join(map(str, map(int, numbers)))

    hardcoded_sql_values = []
    for index, number in enumerate(numbers, 1):
        hardcoded_sql_values.append(f"({number}, {index})")

    output_hardcoded_sql_values = ", ".join(hardcoded_sql_values)

    base_sql = _get_books_base_sql(
        'ROW_NUMBER() OVER (order by c."ordering", b."ordering") as idx'
    )
    sql = f"""
        SELECT t2.* FROM (
          VALUES {output_hardcoded_sql_values}
        ) t0
        INNER JOIN
        (
        SELECT t.* FROM (
            {base_sql}
            WHERE read_start IS NULL
        ) t
        WHERE t.idx IN ({numbers_joined})
        ) t2
        ON t0.column1 = t2.idx
        ORDER BY t0.column2
    """
    books = await _get_books_from_db(sql)
    return books



def _get_books_base_sql(select_param: str or None = None) -> str:
    return f"""
        SELECT
            b.id as book_id,   
            b.name as book_name,
            c.id as category_id,
            c.name as category_name,
            {select_param + "," if select_param else ""}                   
            b.read_start,
            b.read_finish
        FROM book as b
        LEFT JOIN book_category c ON c.id=b.category_id
        """


async def _get_books_from_db(sql) -> List[Book]:
    books = []
    async with aiosqlite.connect(config.SQLITE_DB) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(sql) as cursor:
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
