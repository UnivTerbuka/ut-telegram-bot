from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext


def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        "Tidak ada yang bisa dibatalkan...",
        reply_markup=ReplyKeyboardRemove(),
    )
    return -1
