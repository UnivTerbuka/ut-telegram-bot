from dacite import from_dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, Filters, CommandHandler, MessageHandler
from libs.rbv import Buku

COMMAND = 'baca'

GET_BOOK = range(1)


def answer(update: Update, code: str):
    data = {
        'id': code
    }
    buku: Buku = from_dict(Buku, data)
    if not buku:
        update.effective_message.reply_text('Buku tidak ditemukan')
        return -1
    update.effective_message.reply_text(
        buku.text,
        reply_markup=buku.reply_markup
    )
    return -1


def baca(update: Update, context: CallbackContext):
    msg: str = update.effective_message.text
    if len(msg) > 5:
        answer(update, msg.lstrip('/baca '))
        return -1
    update.effective_message.reply_text(
        'Kode buku yang aka dibaca?'
    )
    return GET_BOOK


def get_buku(update: Update, context: CallbackContext):
    code: str = update.effective_message.text
    answer(update, code)
    return -1


def start(update: Update, context: CallbackContext):
    text: str = update.effective_message.text
    # /start BACA-code
    code: str = text.split('-')[-1]
    answer(update, code)
    return -1


def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(f'/{COMMAND} telah dibatalkan')


BACA = {
    'name': COMMAND,
    'entry_points': [
        CommandHandler(COMMAND,
                       baca),
        CommandHandler('start',
                       start,
                       filters=Filters.regex(r'BACA-[A-Z]{4}\d+\$')),
    ],
    'states': {
        GET_BOOK: [
            MessageHandler(Filters.text & Filters.regex(
                r'^[A-Z]{4}\d+$'), get_buku)
        ]
    },
    'fallbacks': [CommandHandler('cancel', cancel)],
    'conversation_timeout': 180,
}
