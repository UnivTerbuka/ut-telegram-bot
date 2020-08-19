from dacite import from_dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackContext, ConversationHandler, Filters, CallbackQueryHandler, CommandHandler, MessageHandler
from core.utils import action
from config import CALLBACK_SEPARATOR
from handlers.callbacks.modul import answer
from libs.rbv import Modul

# Data : HALAMAN|SUBFOLDER|DOC|END|PAGE

COMMAND = 'halaman'


GET_HALAMAN = range(1)


def back(data):
    data = data if type(data) == str else CALLBACK_SEPARATOR.join(data)
    keyboard = [
        [InlineKeyboardButton('Kembali', callback_data=data)]
    ]
    return InlineKeyboardMarkup(keyboard)


@action.typing
def halaman(update: Update, context: CallbackContext):
    callback_query: CallbackQuery = update.callback_query
    callback_query.answer('Nomor halaman yang dituju?')
    data: list = callback_query.data.split(CALLBACK_SEPARATOR)
    callback_query.edit_message_text(
        'Nomor halaman yang dituju?\n'
        f'Buku : <code>{data[1]}</code>\n'
        f'Modul : <code>{data[2]}</code>\n'
        f'<i>Halaman terakhir {data[3]}.</i>\n'
        '/cancel untuk membatalkan'
    )
    data[0] = 'MODUL'
    context.user_data['halaman'] = data
    return GET_HALAMAN


@action.typing
def get_halaman(update: Update, context: CallbackContext):
    data: str = context.user_data['halaman']
    reply_text = update.effective_message.reply_text
    if not data:
        reply_text('Oops data tidak ditemukan. :3')
        return -1
    nomor: str = update.effective_message.text
    if nomor.isdigit():
        page = int(nomor)
        if page < 1:
            reply_text(
                'Halaman tidak ditemukan',
                reply_markup=back(data)
            )
            return -1
        modul, _ = Modul.from_data(data)
        if not modul:
            reply_text(
                'Data tidak ditemukan',
                reply_markup=back(data)
            )
            return -1
        reply_text('Mencari halaman...')
        if page > modul.end:
            reply_text(
                'Halaman tidak ditemukan',
                reply_markup=back(data)
            )
            return -1
        answer(reply_text, modul, page)
        return -1
    reply_text(
        'Nomor halaman tidak valid',
        reply_markup=back(data)
    )
    return -1


@action.typing
def cancel(update: Update, context: CallbackContext):
    data = context.user_data['halaman']
    update.effective_message.reply_text(
        f'Ke {COMMAND} telah dibatalkan',
        reply_markup=back(data)
    )
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
    'conversation_timeout': 60,
}
