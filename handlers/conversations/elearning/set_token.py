from telegram import Message, Update
from core.context import CoreContext
from core.session import message_wrapper


@message_wrapper
def set_token(update: Update, context: CoreContext):
    message: Message = update.effective_message
    if context.user and context.session:
        context.user.token = message.text
        context.session.commit()
    message.reply_text('Berhasil mengatur token elearning')
    return -1
