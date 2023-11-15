GREETINGS = """
HI! This is bot for book club.


Bot commands:

/start - greeting message.
/help - info.
/allbooks - all books from the list.
/already - book that was read.
/now - current book.
/vote - voting for the next book.

"""


HELP = """
help info
"""

VOTE = """
Выше тебе отправили все книги, за которые можно проголосовать

Тебе нудно выбрать три книги.

Пришли в ответном соообщении номера книг, которые ты хочешь прочесть. \
Номера книг можно разделить пробелами, запятыми и переносами строк.

Обрати внимание, что порядок важен — на первом месте книга, которую ты \
хочешь прочесть сейчас.
"""

VOTE_PROCESS_INCORRECT_INPUT = """НЕ смог прочесть твое сообщение.

Напиши три номера киги в одном сообщении, например, так.

54, 10, 109
"""


VOTE_PROCESS_INCORRECT_BOOKS = """
Переданы некорректные номера книг, пожалуйста, проверь их!
"""


NO_ACTUAL_VOTING = """Нет активного голосования"""
