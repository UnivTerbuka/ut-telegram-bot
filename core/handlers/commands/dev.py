from telegram import Update, Bot
from telegram.ext import CallbackContext

MESSAGE = '''
Pengembang @UniversitasTerbukaBot

@hexatester - Habib Rohman
'''


def dev(update: Update, context: CallbackContext):
    update.effective_message.reply_text(MESSAGE)
