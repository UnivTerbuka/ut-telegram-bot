from telegram import Update, Message
from core.context import CoreContext
from core.session import message_wrapper
from libs.elearning.utils import is_valid_token


@message_wrapper
def start(update: Update, context: CoreContext):
    message: Message = update.effective_message
    try:
        token = message.text.split('-')[-1]
    except Exception:
        return -1
    if not is_valid_token(token):
        message.reply_text('Token tidak valid!')
    elif context.user.token == token:
        message.reply_text('Token sudah diatur (masih sama).')
    else:
        context.user.token = token
        context.session.commit()
        message.reply_text('Berhasil mengatur token elearning')
    return -1
