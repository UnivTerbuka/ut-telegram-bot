from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, Job
from core.utils import action

MESSAGE = '''
Tidak ada yang bisa dibatalkan...
'''


@action.typing
def cancel(update: Update, context: CallbackContext):
    if 'job' in context.chat_data:
        job: Job = context.chat_data['job']
        job.schedule_removal()
    update.effective_message.reply_text(
        MESSAGE,
        reply_markup=ReplyKeyboardRemove(),
    )
    return -1
