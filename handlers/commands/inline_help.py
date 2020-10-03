from telegram import Update
from telegram.ext import CallbackContext

MESSAGE = """
Fitur inline dapat Anda gunakan untuk mencari faq, buku, tiket dan pengumuman.
Untuk mencari buku silahkan gunakan kode buku yang akan dicari.
Untuk melihat pengumuman cukup dengan masuk ke inline mode tanpa argumen.

Cara masuk inline mode cukup ketik
<code>@UniversitasTerbukaBot argumen</code>
Jadi @UniversitasTerbukaBot + spasi
"""


def inline_help(update: Update, context: CallbackContext):
    update.effective_message.reply_text(MESSAGE)
