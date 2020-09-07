from telegram import Update, Message
from config import TOKEN, SQLALCHEMY_DATABASE_URI
from core.context import CoreContext
from core.models import User
from core.session import message_wrapper

MESSAGE = """Selamat datang admin!
/admin ban userid untuk banned user
/admin status untuk menampilkan status
"""


@message_wrapper
def admin(update: Update, context: CoreContext):
    user = context.user
    args = context.args
    message: Message = update.message
    if not user.admin:
        if args and args[0] == TOKEN:
            user.admin = True
            context.session.commit()
            message.reply_text(MESSAGE)
        return
    session = context.session
    if 'status' in args:
        message.reply_text(f'DB {SQLALCHEMY_DATABASE_URI} ONLINE')
    elif 'ban' in args:
        ids = int(args[0])
        banned_user: User = session.query(User).get(ids)
        if banned_user:
            banned_user.banned = True
            session.commit()
            message.reply_text(f'{ids} dibanned')
        else:
            message.reply_text(f'{ids} tidak ditemukan')
