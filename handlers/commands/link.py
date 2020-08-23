from telegram import Update
from telegram.ext import CallbackContext
from core.utils import action

MESSAGE = '''
<a href="https://www.ut.ac.id/">Universitas Terbuka</a>

<a href="https://www.ut.ac.id/jaminan-kualitas/akreditasi-ban-pt">Akreditasi BAN-PT</a>
<a href="https://www.ut.ac.id/biaya-pendidikan">Biaya Pendidikan</a>
<a href="https://www.ut.ac.id/katalog">Katalog</a>
<a href="https://sia.ut.ac.id/register">Registrasi Online</a>
<a href="https://www.ut.ac.id/formulir">Formulir</a>

<a href="http://elearning.ut.ac.id/">Tutorial Online (Elearning UT)</a>
<a href="https://www.ut.ac.id/berita">Berita</a>
<a href="https://www.ut.ac.id/online-learning">Online Learning</a>
<a href="http://ecampus.ut.ac.id/">Ecampus</a>
<a href="https://www.ut.ac.id/pengumuman">Pengumuman</a>

<a href="http://hallo-ut.ut.ac.id/">Layanan Informasi dan Bantuan</a>
<a href="https://www.ut.ac.id/contact-center">Contact Center</a>
'''


@action.typing
def link(update: Update, context: CallbackContext):
    update.effective_message.reply_text(MESSAGE)
