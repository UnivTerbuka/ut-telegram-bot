from logging import getLogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from moodle.core.course import BaseCourse

from core import CoreContext, assert_token, message_wrapper
from libs.elearning.course import course_text
from libs.utils.helpers import build_menu, make_data, make_button
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
    try:
        courses = moodle_course.get_courses_by_field("id", course_id)
    except Exception as e:
        logger.exception(e)
        reply_markup = make_button("Coba lagi", context.query.data)
        context.query.edit_message_text(
            "Gagal mendapatkan kursus.",
            reply_markup=reply_markup,
        )
        raise e
    if not courses:
        context.query.edit_message_text("Kursus tidak ditemukan.")
        return -1
    course_ = courses[0]

    buttons = list()
    sections = moodle_course.get_contents(course_.id)
    for section in sections:
        if not section.uservisible:
            continue
        data = make_data("CONTENT", course_id, section.id, 0)
        button = InlineKeyboardButton(section.name, callback_data=data)
        buttons.append(button)
    if not buttons:
        data = make_data("FORUMS", course_id)
        button = InlineKeyboardButton("Daftar Forum", callback_data=data)
        buttons.append(button)
    keyboard = build_menu(
        buttons,
        footer_buttons=InlineKeyboardButton("Tutup ❌", callback_data="CLOSE"),
    )
    context.query.edit_message_text(
        text=course_text(course_),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return -1


course_pattern = r"^COURSE\|\d+$"
