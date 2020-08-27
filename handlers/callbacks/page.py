from telegram import (Update, CallbackQuery, InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import CallbackContext
from telegram.ext.dispatcher import run_async
from config import CALLBACK_SEPARATOR
from libs.utils.helpers import build_menu

# Data : PAGE|SUBFOLDER|DOC|END|PAGE
# Data : PAGE|MNAU1234|M1|12|1|1

# [Sebelumnya] [Selanjutnya]
# [1] [2] [3]
# [4] [5] [6]
# [7] [8] [9]
# [Kembali] [Tutup]


@run_async
def page(update: Update, context: CallbackContext):
    callback_query: CallbackQuery = update.callback_query
    if not callback_query or not callback_query.data:
        return -1
    callback_query.answer()
    # Validate data
    data = str(callback_query.data).split(CALLBACK_SEPARATOR)
    if len(data) == 6:
        _, subfolder, doc, end, current, number = data
        end, current, number = int(end), int(current), int(number)
    else:
        _, subfolder, doc, end, current = data
        end, current = int(end), int(current)
        number = current // 10

    # Number buttons
    a = 10 * number if 10 * number > 1 else 1
    b = 10 * (number + 1)
    keyboard = []
    limit = False
    for page_number in range(a, b):
        if page_number > end:
            limit = True
            break
        datas = f'MODUL,{subfolder},{doc},{end},{page_number}'.replace(
            ',', CALLBACK_SEPARATOR)
        keyboard.append(
            InlineKeyboardButton(str(page_number), callback_data=datas))

    # Header buttons
    header = []
    if number > 0:
        datas = f"PAGE,{subfolder},{doc},{end},{current},{number - 1}".replace(
            ',', CALLBACK_SEPARATOR)
        header.append(InlineKeyboardButton('Sebelumnya', callback_data=datas))
    if not limit:
        datas = f"PAGE,{subfolder},{doc},{end},{current},{number + 1}".replace(
            ',', CALLBACK_SEPARATOR)
        header.append(InlineKeyboardButton('Selanjutnya', callback_data=datas))

    # Footer buttons
    foooter = [
        InlineKeyboardButton(
            'Kembali',
            callback_data=f'MODUL,{subfolder},{doc},{end},{current}'.replace(
                ',', CALLBACK_SEPARATOR)),
        InlineKeyboardButton('Tutup', callback_data='CLOSE')
    ]

    menu = build_menu(
        buttons=keyboard,
        n_cols=3,
        header_buttons=header,
        footer_buttons=foooter,
    )
    callback_query.edit_message_reply_markup(InlineKeyboardMarkup(menu))
    return -1
