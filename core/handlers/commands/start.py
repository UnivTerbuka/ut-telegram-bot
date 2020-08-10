from telegram import Update, User
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext):
    user: User = update.effective_user
    update.effective_message.reply_text(
        f'Selamat datang {user.full_name}\n\n'
        'Daftar Perintah\n'
        '/start - Memulai bot\n'
        '/shortlink - Memendekan url dengan https://sl.ut.ac.id/\n'
        '/link - Daftar link UT\n'
        '/formulir - Daftar Formulir\n'
        '/dev - Daftar Pengembang\n'
    )
