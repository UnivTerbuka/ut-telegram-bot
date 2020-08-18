from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext
from telegram.error import BadRequest
from libs.ticket import Ticket
from config import CALLBACK_SEPARATOR


def ticket(update: Update, context: CallbackContext):
    try:
        callback_query: CallbackQuery = update.callback_query
        data: str = callback_query.data
        nomor = data.split(CALLBACK_SEPARATOR)[1]
        tiket: Ticket = Ticket.from_nomor(nomor)
        callback_query.edit_message_text(
            str(tiket), reply_markup=tiket.reply_markup)
        callback_query.answer('Data berhasil direfresh.')
    except BadRequest:
        callback_query.answer('Tidak ada perubahan data.')
