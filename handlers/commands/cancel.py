from telegram import Update, Bot
from telegram.ext import CallbackContext
from core.utils import action

MESSAGE = '''
Tidak ada yang bisa dibatalkan...
'''


@action.typing
def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(MESSAGE)
