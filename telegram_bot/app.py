import os
from dotenv import load_dotenv
import re

from datetime import datetime

import logging
import telegram
from telegram import Update 
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)
from telegram_bot import message_texts
from telegram_bot.books import (
    get_all_books,
    get_already_readen_books,
    get_books_by_numbers,
    get_books_we_reading_now
)
import config
from telegram_bot.voting import get_actual_voting_id


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    exit("Specify TELEGRAM_BOT_TOKEN env variable")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_texts.GREETINGS
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_texts.HELP
    )


async def all_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories_with_books = await get_all_books()
    for category in categories_with_books:   
        response = f" <b> {category.name} </b> \n\n"
        for index, book in enumerate(category.books, 1):
            response += f"{index}. {book.name}\n"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
            parse_mode=telegram.constants.ParseMode.HTML
        )


async def already(update: Update, context: ContextTypes.DEFAULT_TYPE):
    already_readen_books = await get_already_readen_books()
    response = "Прочитанные книги:\n\n"
    for index, book in enumerate(already_readen_books, 1):     
        response += (
            f'{index}. {book.name} '
            f'читали ({book.read_start} - {book.read_finish})\n'
        )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response
    )


    
async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now_read_books = await get_books_we_reading_now()
    response = "Сейчас мы читаем:\n\n"
    for index, book in enumerate(now_read_books, 1):      
        response += (
            f'{index}. {book.name} '
            f'читаем ({book.read_start} - {book.read_finish})\n'
        )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response
    )


async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if get_actual_voting_id() is None:
        await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_texts.NO_ACTUAL_VOTING,
        parse_mode=telegram.constants.ParseMode.HTML
    )


    categories_with_books = await get_all_books()
    index = 1
    for category in categories_with_books:   
        response = f" <b> {category.name} </b> \n\n"
        for book in category.books:
            response += f"{index}. {book.name}\n"
            index += 1
        await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
        parse_mode=telegram.constants.ParseMode.HTML
        )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_texts.VOTE,
        parse_mode=telegram.constants.ParseMode.HTML
    )


async def vote_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    numbers = re.findall("\d+", user_message)
    numbers = tuple(set(map(int, numbers)))
    if len(numbers) != config.VOTE_ELEMENTS_COUNT:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_texts.VOTE_PROCESS_INCORRECT_INPUT,
            parse_mode=telegram.constants.ParseMode.HTML
        )
        return
    books = await get_books_by_numbers(numbers)
    if len(books) != config.VOTE_ELEMENTS_COUNT:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_texts.VOTE_PROCESS_INCORRECT_BOOKS,
            parse_mode=telegram.constants.ParseMode.HTML
        )
        return

    response = "Ура, ты выбрали три книги! \n"
    for index, book in enumerate(books, 1):
        response += f"{index}. {book.name}\n"
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
            parse_mode=telegram.constants.ParseMode.HTML
        )


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    all_books_handler = CommandHandler('allbooks', all_books)
    application.add_handler(all_books_handler)

    already_handler = CommandHandler('already', already)
    application.add_handler(already_handler)

    now_handler = CommandHandler('now', now)
    application.add_handler(now_handler)
    
    vote_handler = CommandHandler('vote', vote)
    application.add_handler(vote_handler)

    vote_process_handler = MessageHandler(filters.TEXT & (~filters.COMMAND),
                                         vote_process)
    application.add_handler(vote_process_handler)

    application.run_polling()
