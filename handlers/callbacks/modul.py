from telegram import Update, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.error import BadRequest
from typing import Callable, Union
from config import CALLBACK_SEPARATOR
from libs.rbv import Buku, Modul
from libs.utils import helpers


# Data : MODUL|SUBFOLDER|DOC|END|PAGE
# Data : MODUL|MNAU1234|M1|12|1


def answer(send: Callable, data: Union[Modul, str], page_: int = None):
    if isinstance(data, Modul):
        modul_ = data
    else:
        modul_, page = Modul.from_data(data)
    if page_:
        page = page_
    keyboard = []
    if page > 1:
        keyboard.append(
            InlineKeyboardButton(
                'Sebelumnya',
                callback_data=modul_.callback_data(page-1)
            )
        )
    if page < modul_.end:
        keyboard.append(
            InlineKeyboardButton(
                'Selanjutnya',
                callback_data=modul_.callback_data(page+1)
            )
        )
    footer = []
    footer.append(
        InlineKeyboardButton(
            'Kembali',
            callback_data=f"BUKU|{modul_.subfolder}"
        )
    )
    footer.append(
        InlineKeyboardButton('Tutup', callback_data='CLOSE')
    )
    halaman = InlineKeyboardButton(
        'Ke Halaman?', callback_data=modul_.callback_data(page, 'HALAMAN'))
    menu = helpers.build_menu(
        buttons=keyboard,
        n_cols=2,
        header_buttons=halaman,
        footer_buttons=footer,
    )
    send(
        modul_.message_page(page),
        reply_markup=InlineKeyboardMarkup(menu),
        disable_web_page_preview=False,
    )
    return -1


def modul(update: Update, context: CallbackContext):
    callback_query: CallbackQuery = update.callback_query
    callback_query.answer()
    data: str = callback_query.data
    answer(callback_query.edit_message_text, data)
    return -1
