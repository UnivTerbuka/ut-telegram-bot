from requests.exceptions import ConnectionError
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from typing import List

from moodle.core.course import BaseCourse

from core import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from core.utils.helpers import resolve
from libs.utils.helpers import build_menu, make_data


@message_wrapper
@assert_token
def courses(update: Update, context: CoreContext):
    message = context.message.reply_text("Mendapatkan kursus...")
    message = resolve(message, Message)
    try:
        courses = BaseCourse(
            context.moodle
        ).get_enrolled_courses_by_timeline_classification("all")
    except ConnectionError:
        message.edit_text("Elearning tidak merespon, coba beberapa saat lagi...")
        return -1
    except Exception as e:
        message.edit_text("Gagal mendapatkan kursus.")
        raise e
    if not courses:
        message.edit_text("Tidak ada kursus yang sedang diikuti.")
        return -1
    buttons: List[InlineKeyboardButton] = list()
    for course in courses:
        name = course.fullname or course.shortname
        text = name[:30]
        if len(name) > 30:
            text += "..."
        if course.progress:
            text += f" ({course.progress}%)"
        data = make_data("COURSE", course.id)
        button = InlineKeyboardButton(text, callback_data=data)
        buttons.append(button)
    keyboard = build_menu(
        buttons=buttons,
        footer_buttons=InlineKeyboardButton("Tutup ❌", callback_data="CLOSE"),
    )
    message.edit_text(
        "Daftar kursus yang diikuti",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return -1
