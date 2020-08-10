from telegram import Update
from telegram.ext import CallbackContext

WELCOME_MESSAGE = '''
Selamat datang di bot @UniversitasTerbukaBot
'''


def start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(WELCOME_MESSAGE)
