from logging import getLogger
from re import search as re_search
from telegram import Update, Message

from moodle.core.webservice import BaseWebservice

from core import CoreContext
from core.session import message_wrapper
from libs.elearning.utils import is_valid_token

logger = getLogger(__name__)

msg = """

Perintah yang dapat digunakan
/kursus - Untuk melihat kursus elearning
/reset_token - Cara reset token elearning
/reset - Keluar fitur ini

Mohon untuk tidak mem-forward pesan dari fitur ini ke chat lain.

NIM & Password tidak disimpan oleh bot. Hanya <b>Token</b> yang disimpan.
Token dijaga kerahasiaannya, dan tidak akan disalahgunakan!
"""


def set_token(context: CoreContext):
    text: str = context.message.text
    if not bool(re_search(r"^\S+\s+[a-z0-9]{32}$", text)):
        context.chat.send_message("Token tidak valid!")
        return -1
    token = text.split()[-1]
    message = context.chat.send_message("Mengecek token...")
    if is_valid_token(token):
        context.user.token = token
        context.save()
        message: Message = context.result(message, Message)
        message.edit_text("Token valid!\nSekarang Anda bisa menggunakan /elearning")
    else:
        message: Message = context.result(message, Message)
        message.edit_text("Token tidak valid!")
    return -1


@message_wrapper
def elearning(update: Update, context: CoreContext):
    if not context.user.token:
        return set_token(context)
    info = BaseWebservice(context.moodle).get_site_info()
    text = f"Selamat datang {info.fullname}" + msg
    context.message.reply_text(text)
    return -1
