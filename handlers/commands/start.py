from telegram import Update
from core.context import CoreContext
from core.session import message_wrapper

msg = """

Daftar Perintah
/start - Memulai bot
/baca - Baca buku
/elearning - Akses tuton (elearning.ut.ac.id)
/buku - Cari buku
/tiket - Mengecek tiket <a href="http://hallo-ut.ut.ac.id/">hallo-ut</a>
/shortlink - Memendekan url dengan <a href="https://sl.ut.ac.id/">sl-ut</a>
/link - Daftar link UT
/formulir - Daftar Formulir
/about - Tentang bot ini
'Dengan menggunakan bot ini, berarti anda faham & setuju dengan /eula'
"""


@message_wrapper
def start(update: Update, context: CoreContext):
    user = update.effective_user
    if context.user and not context.user.started:
        context.user.started = True
        context.save()
    context.message.reply_text(f"Selamat datang {user.full_name}" + msg)
    return -1
