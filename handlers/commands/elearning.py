from logging import getLogger
from telegram import Update

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
    if not context.args:
        return -1
    token = context.args[0]
    if is_valid_token(token):
        context.user.token = token
        context.save()
        context.chat.send_message("Sekarang Anda bisa menggunakan /elearning")
    else:
        context.chat.send_message("Token tidak valid!")


@message_wrapper
def elearning(update: Update, context: CoreContext):
    if not context.user.token:
        return set_token(context)
    info = BaseWebservice(context.moodle).get_site_info()
    text = f"Selamat datang {info.fullname}" + msg
    context.message.reply_text(text)
    return -1
