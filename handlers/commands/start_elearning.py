from telegram import Update

from moodle.core.webservice import BaseWebservice

from core.context import CoreContext
from core.session import message_wrapper
from libs.elearning.utils import is_valid_token


@message_wrapper
def start_elearning(update: Update, context: CoreContext):
    try:
        token = context.message.text.split("-")[-1]
    except Exception:
        return -1
    if not is_valid_token(token):
        context.message.reply_text("Token tidak valid!")
        return -1
    context.user.token = token
    context.save()
    context.moodle.token = token
    site_info = BaseWebservice(context.moodle).get_site_info()
    context.message.reply_text(
        f"Selamat datang {site_info.fullname}."
        "\nSekarang Anda bisa menggunakan /elearning",
    )
    return -1
