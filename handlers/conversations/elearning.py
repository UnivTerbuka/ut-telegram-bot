from telegram import Update, Message, User
from telegram.ext import (CallbackContext, Filters, CommandHandler,
                          MessageHandler)
from core.context import CoreContext
from core.session import message_wrapper
from config import DEVS

COMMAND = 'elearning'
SET_TOKEN = range(1)


def elearning(update: Update, context: CallbackContext):
    user: User = update.effective_user
    message: Message = update.effective_message
    if user.id not in DEVS:
        message.reply_text(
            'Untuk saat ini hanya @hexatester yang dapat mengakses fitur ini, '
            'karena masih dalam tahap pengembangan.')
        return -1
    message.reply_text('Masukan token elearning anda.')
    return SET_TOKEN


@message_wrapper
def set_token(update: Update, context: CoreContext):
    message: Message = update.effective_message
    if context.user and context.session:
        context.user.token = message.text
        context.session.commit()
    message.reply_text('Berhasil mengatur toen elearning')
    return -1


def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(f'/{COMMAND} telah dibatalkan')
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
