import os
from dotenv import load_dotenv

import logging
from telegram import Update 
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram_bot import message_texts
from telegram_bot.books import get_all_books


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
    all_books = await get_all_books()
    response = "\n".join((book.name for book in all_books))
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response
    )

# "\n".join((book.name for book in all_books))

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    all_books_handler = CommandHandler('allbooks', all_books)
    application.add_handler(all_books_handler)
    
    application.run_polling()
