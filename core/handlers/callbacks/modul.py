from telegram import Update, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.error import BadRequest
from libs.ticket import Ticket
from core.config import CALLBACK_SEPARATOR
from libs.rbv import Buku, Modul

# Data : MODUL|SUBFOLDER|DOC|END|PAGE
# Data : MODUL|MNAU1234|M1|12|1


def modul(update: Update, context: CallbackContext):
    callback_query: CallbackQuery = update.callback_query
    callback_query.answer()
    data: str = callback_query.data
    modul_, page = Modul.from_data(data)
    keyboard = []
    if page > 1:
        keyboard.append([
            InlineKeyboardButton(
                'Sebelumnya',
                callback_data=modul_.callback_data(page-1)
            )]
        )
    if page < modul_.end:
        keyboard.append([
            InlineKeyboardButton(
                'Selanjutnya',
                callback_data=modul_.callback_data(page+1)
            )]
        )
    keyboard.append([
        InlineKeyboardButton(
            'Tutup',
            callback_data='CLOSE'
        )]
    )
    callback_query.edit_message_text(
        modul_.message_page(page),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return -1
