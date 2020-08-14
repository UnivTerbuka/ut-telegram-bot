from dacite import from_dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackContext, ConversationHandler, Filters, CallbackQueryHandler, CommandHandler, MessageHandler
from core.config import CALLBACK_SEPARATOR
from core.handlers.callbacks.modul import answer
from libs.rbv import Modul

# Data : HALAMAN|SUBFOLDER|DOC|END|PAGE

COMMAND = 'halaman'


GET_HALAMAN = range(1)


def halaman(update: Update, context: CallbackContext):
    callback_query: CallbackQuery = update.callback_query
    callback_query.answer('Nomor halaman yang dituju?')
    update.effective_message.reply_text(
        'Nomor halaman yang dituju?'
    )
    context.user_data['halaman'] = callback_query.data
    return GET_HALAMAN


def get_halaman(update: Update, context: CallbackContext):
    nomor: str = update.effective_message.text
    if nomor.isdigit():
        page = int(nomor)
        if page < 1:
            update.effective_message.reply_text('Halaman tidak ditemukan')
            return
        data = context.user_data['halaman']
        modul, _ = Modul.from_data(data)
        if not modul:
            update.effective_message.reply_text('Data tidak ditemukan')
            return -1
        if page > modul.end:
            update.effective_message.reply_text('Halaman tidak ditemukan')
            return
        answer(update.effective_message.reply_text, modul, page)
        return -1
    update.effective_message.reply_text('Nomor halaman tidak valid')
    return -1


def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(f'Ke {COMMAND} telah dibatalkan')
    data = context.user_data['halaman']
    modul, page = Modul.from_data(data)
    if not modul:
        update.effective_message.reply_text('Data tidak ditemukan')
        return -1
    if page > modul.end:
        update.effective_message.reply_text('Halaman tidak ditemukan')
        return -1
    answer(update.effective_message.reply_text, modul, page)
    return -1


HALAMAN = {
    'name': COMMAND,
    'entry_points': [
        CallbackQueryHandler(
            halaman, pattern=r'^HALAMAN\|[A-Z]{4}\d+\|\S+\|\d+$'),
    ],
    'states': {
        GET_HALAMAN: [
            MessageHandler(Filters.text & Filters.regex(
                r'^\d+$'), get_halaman)
        ]
    },
    'fallbacks': [CommandHandler('cancel', cancel)],
    'conversation_timeout': 180,
}
