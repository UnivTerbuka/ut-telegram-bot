from logging import getLogger
from telegram import Update, Message
from core.context import CoreContext
from core.decorator import only_users
from core.session import message_wrapper
from config import DEVS, DOMAIN
from . import SET_TOKEN

logger = getLogger(__name__)


@only_users(DEVS, 'Fitur masih dalam pengembangan.')
@message_wrapper
def elearning(update: Update, context: CoreContext):
    message: Message = update.effective_message
    if not context.user.token:
        message.reply_text(
            'Silahkan login untuk mendapatkan token elearning\n' + DOMAIN +
            'elearning.html')
        return -1
    if 'reset' in message.text:
        message.reply_text('Token berhasil direset.')
        context.user.token = None
        context.session.commit()
        logger.debug('Berhasil mereset token pengguna {}'.format(
            context.user.name))
        return -1
    message.reply_text('Masukan token elearning anda.')
    return SET_TOKEN
