import os
from dotenv import load_dotenv
import random

from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import Filters
from telegram import ReplyKeyboardMarkup

load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')


WORDS = {
    'Привет': 'Hello',
    'Пока': 'Goodbye',
    'Запустить': 'Run',
    'Ракета': 'Rocket',
    'Школа': 'School',
    'Змея': 'Python',
    'Машина': 'Car',
    'Язык': 'Language'
}


def generate_question():
    options = random.sample(WORDS.keys(), 4)
    question = random.choice(options)
    correct_answer = WORDS[question]
    return options, question, correct_answer


def handle_start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text='Hello!')
    context.bot.send_message(chat_id=chat_id, text='You are given word and 4 variant of answer. Choose your variant')
    updater(update, context)


def handle_answer(update, context):
    chat_id = update.effective_chat.id
    player_answer = update.effective_message.text
    correct_answer = context.user_data['answer']
    if correct_answer == player_answer:
        context.bot.send_message(chat_id=chat_id, text='Correct!')
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=f'Incorrect, right answer: "{correct_answer}"'
        )
    updater(update, context)


def updater(update, context):
    chat_id = update.effective_chat.id
    options, question, correct_answer = generate_question()
  
    translate_options = []
    for word in options:
        translate_options.append(WORDS[word])

    keyboard = ReplyKeyboardMarkup.from_column(
        translate_options,
        one_time_keyboard=True,
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat_id,
        text=f'translate this word "{question}"',
        reply_markup=keyboard,
    )
    context.user_data['answer'] = correct_answer
  
  


bot = Updater(token=SECRET_KEY)
# /start -> Greeting
bot.dispatcher.add_handler(CommandHandler('start', handle_start))
# game start
bot.dispatcher.add_handler(MessageHandler(Filters.text, handle_answer))

bot.start_polling()
