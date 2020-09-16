from telegram import Update, Message
from core.context import CoreContext
from core.decorator import only_users
from core.session import message_wrapper
from config import DEVS
from libs.elearning.utils import is_valid_token


@only_users(DEVS)
@message_wrapper
def start_elearning(update: Update, context: CoreContext):
    message: Message = update.effective_message
    try:
        token = message.text.split('-')[-1]
    except Exception:
        return -1
    if not is_valid_token(token):
        message.reply_text('Token tidak valid!')
    else:
        context.user.token = token
        context.save()
        context.moodle.token = token
        site_info = context.moodle.core.webservice.get_site_info()
        message.reply_text(f'Selamat datang {site_info.fullname}.'
                           '\nSekarang Anda bisa menggunakan /elearning')
    return -1
