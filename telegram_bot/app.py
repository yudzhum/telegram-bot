import os
from dotenv import load_dotenv

from datetime import datetime

import logging
import telegram
from telegram import Update 
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram_bot import message_texts
from telegram_bot.books import (
    get_all_books,
    get_already_readen_books,
    get_books_we_reading_now
)
import config


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
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_texts.HELP
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

    application.run_polling()
