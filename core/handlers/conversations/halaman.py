from dacite import from_dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackContext, ConversationHandler, Filters, CommandHandler, MessageHandler
from core.config import CALLBACK_SEPARATOR
from core.handlers.callbacks.modul import answer
from libs.rbv import Modul

# Data : HALAMAN|SUBFOLDER|DOC|END|PAGE

COMMAND = 'halaman'


HALAMAN = range(1)


def halaman(update: Update, context: CallbackContext):
    callback_query: CallbackQuery = update.callback_query
    callback_query.answer('Nomor halaman yang dituju?')
    update.effective_message.reply_text(
        'Nomor halaman yang dituju?'
    )
    context.user_data['halaman'] = callback_query.data
    return HALAMAN


def get_halaman(update: Update, context: CallbackContext):
    nomor: str = update.effective_message.text
    if nomor.isdigit():
        page = int(nomor)
        if page < 1:
            update.effective_message.reply_text('Halaman tidak ditemukan')
            return
        data = context.user_data['halaman'].split(CALLBACK_SEPARATOR)
        data = {
            'subfolder': data[1],
            'doc': data[2],
            'end': data[3],
        }
        modul: Modul = from_dict(Modul, data)
        if not modul:
            update.effective_message.reply_text('Data tidak ditemukan')
            return -1
        if page > modul.end:
            update.effective_message.reply_text('Halaman tidak ditemukan')
            return
        answer(update.effective_message.reply_text, modul)
    return -1


def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(f'/{COMMAND} telah dibatalkan')


BACA = {
    'name': COMMAND,
    'entry_points': [
        CommandHandler(COMMAND, halaman),
    ],
    'states': {
        HALAMAN: [
            MessageHandler(Filters.text & Filters.regex(
                r'^\d+$'), get_halaman)
        ]
    },
    'fallbacks': [CommandHandler('cancel', cancel)],
    'conversation_timeout': 180,
}
