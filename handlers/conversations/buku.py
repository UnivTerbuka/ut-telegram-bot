from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, Filters, CommandHandler, MessageHandler
from libs.bahan_ajar import BahanAjar, Book

COMMAND = 'buku'

GET_BOOKS = range(1)


def answer(update: Update, query: str):
    books = BahanAjar.search(query)
    if books:
        texts = []
        for book in books:
            texts.append(book.text)
        update.effective_message.reply_text(
            '\n'.join(texts)
        )
    else:
        update.effective_message.reply_text(
            f'Buku `{query}` tidak ditemukan'
        )


def buku(update: Update, context: CallbackContext):
    msg: str = update.effective_message.text
    if len(msg) > 5:
        answer(update, msg.lstrip('/buku '))
        return -1
    update.effective_message.reply_text(
        'Cari buku apa?\n'
        '/cancel untuk membatalkan'
    )
    return GET_BOOKS


def get_buku(update: Update, context: CallbackContext):
    query: str = update.effective_message.text
    answer(update, query)
    return -1


def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(f'/{COMMAND} telah dibatalkan')


BUKU = {
    'name': COMMAND,
    'entry_points': [CommandHandler(COMMAND, buku)],
    'states': {
        GET_BOOKS: [
            MessageHandler(Filters.text & ~Filters.regex(r'^/'), get_buku)
        ]
    },
    'fallbacks': [CommandHandler('cancel', cancel)],
    'conversation_timeout': 180,
}
