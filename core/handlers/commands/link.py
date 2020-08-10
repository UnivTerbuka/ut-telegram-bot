from telegram import Update, Bot
from telegram.ext import CallbackContext

LINKS = []

MESSAGE = '''
Berikut link-link web universitas terbuka
Formulir | Universitas Terbuka
'''


def link(update: Update, context: CallbackContext):
    update.effective_message.reply_text(MESSAGE)
