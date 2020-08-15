from dacite import from_dict
from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext
from core.config import CALLBACK_SEPARATOR
from libs.rbv import Buku, Modul

# data : BUKU|KODE|DOC|END


def buku(update: Update, context: CallbackContext):
    callback_query: CallbackQuery = update.callback_query
    callback_query.answer()
    datas: list = callback_query.data.split(CALLBACK_SEPARATOR)
    data = {
        'id': datas[1]
    }
    buku_: Buku = from_dict(Buku, data)
    if not buku_:
        callback_query.edit_message_text('Data tidak ditemukan.')
        return -1
    callback_query.edit_message_text(
        buku_.text,
        reply_markup=buku_.reply_markup
    )
    return -1
