from logging import getLogger
from telegram import Update

from moodle.core.webservice import BaseWebservice

from core import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper

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


@message_wrapper
@assert_token
def elearning(update: Update, context: CoreContext):
    info = BaseWebservice(context.moodle).get_site_info()
    text = f"Selamat datang {info.fullname}" + msg
    context.message.reply_text(text)
    return -1
