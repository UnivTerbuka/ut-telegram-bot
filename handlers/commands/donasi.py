from telegram import Update
from telegram.ext import CallbackContext
from core.utils import action

MESSAGE = '''
Untuk donasi, kritik, saran, dan sebagainya silahkan PM @hexatester
Terimakasih
'''


@action.typing
def donasi(update: Update, context: CallbackContext):
    update.effective_message.reply_text(MESSAGE)
