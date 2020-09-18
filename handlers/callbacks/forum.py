from logging import getLogger
from telegram import Update
from core.context import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from config import CALLBACK_SEPARATOR
from libs.elearning.forum import forum_text

logger = getLogger(__name__)


@message_wrapper
@assert_token
def forum(update: Update, context: CoreContext):
    context.query.answer()
    datas = context.query.data.split(CALLBACK_SEPARATOR)
    # FORUM|course_id|forum_id
    course_id = int(datas[1])
    try:
        forums = context.moodle.mod.forum.get_forums_by_courses([course_id])
        if not forums:
            context.query.edit_message_text('Forum tidak ditemukan.')
            return -1
    except Exception as e:
        logger.debug('Error {}'.format(repr(e)))
        context.query.edit_message_text('Gagal mendapatkan forum')
        return -1
    forum_id = int(datas[2])
    for fo in forums:
        if fo.id != forum_id:
            continue
        text = forum_text(fo)
        context.query.edit_message_text(text)
        break
    return -1
