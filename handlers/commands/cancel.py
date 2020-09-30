from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, Job

MESSAGE = """
Tidak ada yang bisa dibatalkan...
"""


def cancel(update: Update, context: CallbackContext):
    if "job" in context.chat_data:
        job: Job = context.chat_data["job"]
        job.schedule_removal()
    update.effective_message.reply_text(
        MESSAGE,
        reply_markup=ReplyKeyboardRemove(),
    )
    return -1
