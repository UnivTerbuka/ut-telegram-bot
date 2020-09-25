from logging import getLogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from moodle.core.course import BaseCourse

from core.context import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from libs.elearning.course import course_text
from libs.utils.helpers import build_menu, make_data
from config import CALLBACK_SEPARATOR

logger = getLogger(__name__)


@message_wrapper
@assert_token
def course(update: Update, context: CoreContext):
    context.query.answer()
    datas = context.query.data.split(CALLBACK_SEPARATOR)
    # COURSE|course_id
    course_id = int(datas[-1])
    courses = BaseCourse(context.moodle).get_courses_by_field('id', course_id)
    if not courses:
        context.query.edit_message_text('Kursus tidak ditemukan.')
        return -1
    course_ = courses[0]
    buttons = [
        InlineKeyboardButton('Daftar Sesi',
                             callback_data=make_data('CONTENTS', course_id)),
        InlineKeyboardButton('Daftar Forum',
                             callback_data=make_data('FORUMS', course_id))
    ]
    keyboard = build_menu(
        buttons,
        footer_buttons=InlineKeyboardButton('Tutup', callback_data='CLOSE'),
    )
    context.query.edit_message_text(
        text=course_text(course_),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return -1
