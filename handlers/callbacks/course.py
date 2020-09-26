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

    moodle_course = BaseCourse(context.moodle)
    courses = moodle_course.get_courses_by_field('id', course_id)
    if not courses:
        context.query.edit_message_text('Kursus tidak ditemukan.')
        return -1
    course_ = courses[0]

    try:
        sections = moodle_course.get_contents(course_.id)
    except Exception:
        pass

    buttons = list()
    if sections:
        for section in sections:
            if section.uservisible:
                data = make_data('CONTENT', course_id, section.id, 0)
                button = InlineKeyboardButton(section.name, callback_data=data)
                buttons.append(button)
    else:
        data = make_data('FORUMS', course_id)
        button = InlineKeyboardButton('Daftar Forum', callback_data=data)
        buttons.append(button)
    keyboard = build_menu(
        buttons,
        footer_buttons=InlineKeyboardButton('Tutup', callback_data='CLOSE'),
    )
    context.query.edit_message_text(
        text=course_text(course_),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return -1
