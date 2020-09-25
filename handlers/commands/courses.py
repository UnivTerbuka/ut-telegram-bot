from logging import getLogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from typing import List

from moodle.core.course import BaseCourse

from core.context import CoreContext
from core.decorator import only_users, assert_token
from core.session import message_wrapper
from config import DEVS
from libs.utils.helpers import build_menu, make_data

logger = getLogger(__name__)


@only_users(DEVS, 'Fitur masih dalam pengembangan.')
@message_wrapper
@assert_token
def courses(update: Update, context: CoreContext):
    courses = BaseCourse(
        context.moodle).get_enrolled_courses_by_timeline_classification('all')
    if not courses:
        context.message.reply_text('Tidak ada kursus yang sedang diikuti.')
        return -1
    buttons: List[InlineKeyboardButton] = list()
    for course in courses:
        text = course.shortname or course.fullname
        if course.progress:
            text += f" {course.progress}%"
        data = make_data('COURSE', course.id)
        button = InlineKeyboardButton(text, callback_data=data)
        buttons.append(button)
    keyboard = build_menu(
        buttons=buttons,
        footer_buttons=InlineKeyboardButton('Tutup', callback_data='CLOSE'),
    )
    context.message.reply_text(
        'Daftar kursus yang diikuti',
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return -1
