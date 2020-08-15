from telegram import Update, Bot
from telegram.ext import CallbackContext

MESSAGE = '''
Tidak ada yang bisa dibatalkan...
'''


def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(MESSAGE)
