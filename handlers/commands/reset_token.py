from telegram import Update
from telegram.ext import CallbackContext

msg = """
Cara reset Token:
1. Masuk Elearning
2. Dasbor
3. Preferensi
4. Akun Pengguna
5. Kunci Keamanan
6. Set Ulang (Kolom Operasi & Baris Moodle mobile web service)
"""


def reset_token(update: Update, context: CallbackContext):
    update.effective_chat.send_message(msg)
