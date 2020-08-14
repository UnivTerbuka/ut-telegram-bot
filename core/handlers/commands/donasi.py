from telegram import Update
from telegram.ext import CallbackContext

MESSAGE = '''
Untuk donasi, kritik, saran, dan sebagainya silahkan PM @hexatester
Terimakasih
'''


def donasi(update: Update, context: CallbackContext):
    update.effective_message.reply_text(MESSAGE)
