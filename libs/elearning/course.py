from moodle.core.course import Course, CourseBTC, CoursesBTC
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import CALLBACK_SEPARATOR
from ..utils import format_html
from ..utils.helpers import build_menu


def buton_data(course: CourseBTC) -> str:
    return 'COURSE' + CALLBACK_SEPARATOR + str(course.id)


def course_buttons(courses: CoursesBTC,
                   index=0,
                   limit=10) -> InlineKeyboardMarkup:
    buttons = []
    for course in courses:
        buttons.append(
            InlineKeyboardButton(
                course.shortname or course.fullname,
                callback_data=buton_data(course),
            ))
    keyboard = build_menu(
        buttons=buttons,
        footer_buttons=InlineKeyboardButton('Tutup', callback_data='CLOSE'),
    )
    return InlineKeyboardMarkup(keyboard)


def course_text(course: Course) -> str:
    text = 'Kursus\n'
    text += format_html.code(course.fullname) + '\n'
    return text
