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

<b>Fitur ini masih dalam proses pengembangan.</b>
Mohon untuk tidak mem-forward pesan dari fitur ini ke chat lain,
karena ada kemungkinan pesan mengandung token Anda (khususnya dokumen)!

Jika token Anda tersebar, segera Set Ulang di
Elearning > Dasbor > Preferensi > Akun Pengguna > Kunci Keamanan > Set Ulang
(Kolom Operasi & Baris Moodle mobile web service)

Untuk keluar dari fitur ini : <pre>/elearning reset</pre>
"""


@message_wrapper
@assert_token
def elearning(update: Update, context: CoreContext):
    if "reset" in context.message.text:
        context.user.token = None
        context.save()
        context.message.reply_text("Token berhasil direset.")
        logger.debug("Berhasil mereset token pengguna {}".format(context.user.name))
        return -1
    info = BaseWebservice(context.moodle).get_site_info()
    text = f"Selamat datang {info.fullname}" + msg
    context.message.reply_text(text)
    return -1
