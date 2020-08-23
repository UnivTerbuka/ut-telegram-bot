from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import CallbackContext, Job
from libs.rbv import Modul
from libs.utils.helpers import build_menu


def modul(context: CallbackContext):
    job: Job = context.job
    bot: Bot = context.bot
    # context = (chat_id, message_id, data)
    chat_id, message_id, data = job.context
    modul_, page = Modul.from_data(data)
    keyboard = []
    if page > 1:
        keyboard.append(
            InlineKeyboardButton('Sebelumnya',
                                 callback_data=modul_.callback_data(page - 1)))
    if page < modul_.end:
        keyboard.append(
            InlineKeyboardButton('Selanjutnya',
                                 callback_data=modul_.callback_data(page + 1)))
    footer = []
    footer.append(
        InlineKeyboardButton('Kembali',
                             callback_data=f"BUKU|{modul_.subfolder}"))
    footer.append(InlineKeyboardButton('Tutup', callback_data='CLOSE'))
    header = []
    header.append(
        InlineKeyboardButton('Share', url=modul_.deep_linked_page(page)))
    header.append(
        InlineKeyboardButton('Ke Halaman?',
                             callback_data=modul_.callback_data(page, 'PAGE')))
    menu = build_menu(
        buttons=keyboard,
        n_cols=2,
        header_buttons=header,
        footer_buttons=footer,
    )
    bot.edit_message_text(
        modul_.message_page(page),
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=InlineKeyboardMarkup(menu),
        disable_web_page_preview=False,
    )
    if context.chat_data and 'modul' in context.chat_data:
        del context.chat_data['modul']
