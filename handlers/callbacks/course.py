from logging import getLogger
from telegram import Update
from core.context import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from libs.elearning.course import course_text
from libs.utils.helpers import make_button
from config import CALLBACK_SEPARATOR

logger = getLogger(__name__)


@message_wrapper
@assert_token
def course(update: Update, context: CoreContext):
    context.query.answer()
    datas = context.query.data.split(CALLBACK_SEPARATOR)
    # COURSE|course_id
    course_id = int(datas[-1])
    try:
        course = context.moodle.core.course.get_courses_by_field(
            'id', course_id)[0]
    except Exception as e:
        logger.debug('Error {}'.format(repr(e)))
        context.query.edit_message_text('Gagal mendapatkan kursus')
        return -1
    context.query.edit_message_text(
        text=course_text(course),
        reply_markup=make_button('Daftar Forum', f"FORUMS|{course_id}"),
    )
    return -1
