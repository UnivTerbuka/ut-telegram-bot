from telegram import Update, Message
from core.context import CoreContext
from core.models import User
from core.session import message_wrapper

from config import DEVS

MESSAGE = """Selamat datang admin!
/admin ban userid untuk banned user
/admin status untuk menampilkan status
"""


@message_wrapper
def admin(update: Update, context: CoreContext):
    if context.user.id not in DEVS:
        return
    message: Message = update.message
    args = message.text.split(' ')
    if 'status' in args:
        count = context.session.query(User).count()
        message.reply_text(f'Pengguna aktif saat ini <code>{count}</code>')
    elif 'ban' in args:
        ids = int(args[-1])
        session = context.session
        banned_user: User = session.query(User).get(ids)
        if banned_user:
            banned_user.banned = True
            session.commit()
            message.reply_text(f'{ids} dibanned')
        else:
            message.reply_text(f'{ids} tidak ditemukan')
