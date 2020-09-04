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
    txt = data.endswith('txt')
    keyboard = []
    if page > 1:
        keyboard.append(
            InlineKeyboardButton('Halaman Sebelumnya',
                                 callback_data=modul_.callback_data(page - 1,
                                                                    txt=txt)))
    if page < modul_.end:
        keyboard.append(
            InlineKeyboardButton('Halaman Selanjutnya',
                                 callback_data=modul_.callback_data(page + 1,
                                                                    txt=txt)))
    footer = []
    footer.append(
        InlineKeyboardButton(f'Ke modul? ({modul_.doc})',
                             callback_data=f"BUKU|{modul_.subfolder}"))
    footer.append(InlineKeyboardButton('Tutup', callback_data='CLOSE'))
    header = []
    header.append(
        InlineKeyboardButton(f'Ke halaman? ({page})',
                             callback_data=modul_.callback_data(page,
                                                                'PAGE',
                                                                txt=txt)))
    # Switch text or image
    if txt:
        header.append(
            InlineKeyboardButton('Versi Gambar',
                                 callback_data=modul_.callback_data(
                                     page, txt=False)))
    else:
        header.append(
            InlineKeyboardButton('Versi Teks [Beta]',
                                 callback_data=modul_.callback_data(page)))
    menu = build_menu(
        buttons=keyboard,
        n_cols=2,
        header_buttons=header,
        footer_buttons=footer,
    )
    text = modul_.get_page_text(page) if txt else modul_.message_page(page)
    bot.edit_message_text(
        text,
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=InlineKeyboardMarkup(menu),
        disable_web_page_preview=txt,
    )
    if context.chat_data and 'modul' in context.chat_data:
        del context.chat_data['modul']
