from telegram import Update
from telegram.ext import (CallbackContext, Filters, CommandHandler,
                          MessageHandler)
from core.utils import action
from libs.bahan_ajar import BahanAjar

COMMAND = 'buku'

GET_BOOKS = range(1)


def answer(update: Update, query: str):
    books = BahanAjar.search(query)
    if books:
        texts = []
        for book in books:
            texts.append(book.text)
        update.effective_message.reply_text('\n'.join(texts))
    else:
        update.effective_message.reply_text(f'Buku `{query}` tidak ditemukan')


@action.typing
def buku(update: Update, context: CallbackContext):
    msg: str = update.effective_message.text
    if len(msg) > 5:
        answer(update, msg.lstrip('/buku '))
        return -1
    update.effective_message.reply_text('Cari buku apa?\n'
                                        '/cancel untuk membatalkan')
    return GET_BOOKS


@action.typing
def get_buku(update: Update, context: CallbackContext):
    query: str = update.effective_message.text
    answer(update, query)
    return -1


@action.typing
def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(f'/{COMMAND} telah dibatalkan')
    return -1


BUKU = {
    'name': COMMAND,
    'entry_points': [CommandHandler(COMMAND, buku, Filters.private)],
    'states': {
        GET_BOOKS:
        [MessageHandler(Filters.text & ~Filters.regex(r'^/'), get_buku)]
    },
    'fallbacks': [CommandHandler('cancel', cancel)],
    'conversation_timeout': 180,
}
