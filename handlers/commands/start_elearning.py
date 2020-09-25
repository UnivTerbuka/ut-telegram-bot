from telegram import Update, Message

from moodle.core.webservice import BaseWebservice

from core.context import CoreContext
from core.session import message_wrapper
from libs.elearning.utils import is_valid_token


@message_wrapper
def start_elearning(update: Update, context: CoreContext):
    message: Message = update.effective_message
    try:
        token = message.text.split('-')[-1]
    except Exception:
        return -1
    if not is_valid_token(token):
        message.reply_text('Token tidak valid!')
        return -1
    context.user.token = token
    context.save()
    context.moodle.token = token
    site_info = BaseWebservice(context.moodle).get_site_info()
    message.reply_text(
        f'Selamat datang {site_info.fullname}.'
        '\nSekarang Anda bisa menggunakan /elearning'
        '\n<b>Fitur ini masih dalam proses pengembangan.</b>'
        '\nMohon untuk tidak mem-forward pesan dari fitur ini ke chat lain, '
        'karena ada kemungkinan pesan mengandung token Anda!\n'
        'Jika token Anda tersebar, segera Set Ulang di Elearning > Dasbor > '
        'Preferensi > Akun Pengguna > Kunci Keamanan > Set Ulang '
        '(Kolom Operasi & Baris Moodle mobile web service)', )
    return -1
