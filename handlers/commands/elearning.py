from logging import getLogger
from telegram import Update

from moodle.core.webservice import BaseWebservice

from core.context import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper

logger = getLogger(__name__)


@message_wrapper
@assert_token
def elearning(update: Update, context: CoreContext):
    if 'reset' in context.message.text:
        context.user.token = None
        context.save()
        context.message.reply_text('Token berhasil direset.')
        logger.debug('Berhasil mereset token pengguna {}'.format(
            context.user.name))
        return -1
    info = BaseWebservice(context.moodle).get_site_info()
    text = 'Selamat datang ' + info.fullname + '\n'
    text += 'Perintah yang bisa dipakai\n'
    text += '/kursus - Untuk melihat daftar kursus'
    context.message.reply_text(text)
    return -1
