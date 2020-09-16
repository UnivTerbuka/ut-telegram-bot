from telegram import Update, Message
from telegram.ext import (CallbackContext, Filters, CommandHandler,
                          MessageHandler)
from core.context import CoreContext
from core.decorator import only_users
from core.session import message_wrapper
from libs.elearning.utils import is_valid_token
from config import DEVS, DOMAIN

COMMAND = 'elearning'
SET_TOKEN = range(1)


@only_users(DEVS, 'Fitur masih dalam pengembangan.')
@message_wrapper
def elearning(update: Update, context: CoreContext):
    message: Message = update.effective_message
    if not context.user.token:
        message.reply_text(
            'Silahkan login untuk mendapatkan token elearning\n' + DOMAIN +
            'elearning.html')
        return -1
    if 'reset' in message.text:
        message.reply_text('Token berhasil direset.')
        context.user.token = None
        context.session.commit()
        return -1
    message.reply_text('Masukan token elearning anda.')
    return SET_TOKEN


@message_wrapper
def set_token(update: Update, context: CoreContext):
    message: Message = update.effective_message
    if context.user and context.session:
        context.user.token = message.text
        context.session.commit()
    message.reply_text('Berhasil mengatur token elearning')
    return -1


def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(f'/{COMMAND} telah dibatalkan')
    return -1


@message_wrapper
def start(update: Update, context: CoreContext):
    message: Message = update.effective_message
    try:
        token = message.text.split('-')[-1]
    except Exception:
        return -1
    if not is_valid_token(token):
        message.reply_text('Token tidak valid!')
    elif context.user.token == token:
        message.reply_text('Token sudah diatur (masih sama).')
    else:
        context.user.token = token
        context.session.commit()
        message.reply_text('Berhasil mengatur token elearning')
    return -1


ELEARNING = {
    'name':
    COMMAND,
    'entry_points': [
        CommandHandler(COMMAND, elearning),
        CommandHandler('start',
                       start,
                       filters=Filters.private
                       & Filters.regex(r'^\/start TOKEN-[a-z0-9]+$'))
    ],
    'states': {
        SET_TOKEN:
        [MessageHandler(Filters.text & ~Filters.regex(r'^/'), set_token)]
    },
    'fallbacks': [CommandHandler('cancel', cancel)]
}
