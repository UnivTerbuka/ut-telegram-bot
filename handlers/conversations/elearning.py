from telegram import Update, User, Message
from telegram.ext import (CallbackContext, Filters, CommandHandler,
                          MessageHandler)
from config import DEVS

COMMAND = 'elearning'
SET_TOKEN = range(1)


def elearning(update: Update, context: CallbackContext):
    user: User = update.effective_user
    message: Message = update.effective_message
    if user.id not in DEVS:
        message.reply_text('Coming soon. :D')
        return -1
    return SET_TOKEN


def set_token(update: Update, context: CallbackContext):
    return -1


def cancel(update: Update, context: CallbackContext):
    return -1


ELEARNING = {
    'name': COMMAND,
    'entry_points': [CommandHandler(COMMAND, elearning)],
    'states': {
        SET_TOKEN:
        [MessageHandler(Filters.text & ~Filters.regex(r'^/'), set_token)]
    },
    'fallbacks': [CommandHandler('cancel', cancel)]
}
