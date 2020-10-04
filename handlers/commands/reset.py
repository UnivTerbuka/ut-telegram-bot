from telegram import Update
from core import CoreContext
from core.session import message_wrapper


@message_wrapper
def reset(update: Update, context: CoreContext):
    if not context.user.token:
        context.chat.send_message("Anda sudah keluar fitur elearning.")
        return -1
    context.user.token = None
    context.save()
    context.message.reply_text("Berhasil keluar fitur elearning, token dihapus.")
    return -1
