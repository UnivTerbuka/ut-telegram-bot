from logging import getLogger
from telegram import Update
from core.context import CoreContext
from core.decorator import only_users, assert_token
from core.session import message_wrapper
from config import DEVS
from libs.elearning.course import course_buttons

logger = getLogger(__name__)


@only_users(DEVS, 'Fitur masih dalam pengembangan.')
@message_wrapper
@assert_token
def courses(update: Update, context: CoreContext):
    try:
        courses = (context.moodle.core.course.
                   get_enrolled_courses_by_timeline_classification('all'))
    except Exception as e:
        logger.debug('User {} karena {}'.format(repr(context.user), e))
        context.message.reply_text('Gagal mendapatkan kursus')
        return -1
    context.message.reply_text(
        'Daftar kursus yang diikuti',
        reply_markup=course_buttons(courses),
    )
    return -1
