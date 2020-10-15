from telegram import Update

from core import CoreContext
from core.models import User
from core.session import message_wrapper

from config import DEVS

msg = """Selamat datang admin!
/admin ban userid untuk banned user
/admin status untuk menampilkan status
"""


@message_wrapper
def admin(update: Update, context: CoreContext):
    if context.user.id not in DEVS:
        return
    message = update.effective_message
    args = message.text.split(" ")
    if "status" in args:
        all_count = context.session.query(User).count()
        elearning_count = (
            context.session.query(User).filter(User.token is not None).count()
        )
        message.reply_text(
            f"Pengguna elearning <code>{elearning_count}</code>\n"
            f"Total pengguna <code>{all_count}</code>\n"
        )
    elif "ban" in args:
        ids = int(args[-1])
        session = context.session
        banned_user: User = session.query(User).get(ids)
        if banned_user:
            banned_user.banned = True
            session.commit()
            message.reply_text(f"{ids} dibanned")
        else:
            message.reply_text(f"{ids} tidak ditemukan")
    else:
        message.reply_text(msg)
    return -1
