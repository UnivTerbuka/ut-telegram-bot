from telegram import Update

from core import CoreContext
from core.session import message_wrapper
from libs.elearning.utils import is_valid_token


@message_wrapper
def start_elearning(update: Update, context: CoreContext):
    # /start TOKEN-1234568abcdefghick
    token = context.message.text.split("-")[-1]
    if not is_valid_token(token):
        context.message.reply_text("Token tidak valid!")
        return -1
    context.user.token = token
    # simpan token ke database
    context.save()
    context.message.reply_text("Sekarang Anda bisa menggunakan /elearning")
    return -1
