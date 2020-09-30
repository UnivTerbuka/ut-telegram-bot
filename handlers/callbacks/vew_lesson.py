from logging import getLogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from moodle.mod.lesson import BaseLesson

from core.context import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from libs.utils.helpers import make_data
from config import CALLBACK_SEPARATOR

logger = getLogger(__name__)


@message_wrapper
@assert_token
def view_lesson(update: Update, context: CoreContext):
    context.query.answer()
    datas = context.query.data.split(CALLBACK_SEPARATOR)
    # LESSON|course_id|lesson_id
    course_id = int(datas[1])
    lesson_id = int(datas[2])
    base_lesson = BaseLesson(context.moodle)
    res = base_lesson.view_lesson(lesson_id)
    logger.debug(repr(res))
    back_data = make_data("COURSE", course_id)
    keyboard = [
        [
            InlineKeyboardButton("< Kembali", callback_data=back_data),
            InlineKeyboardButton("Tutup ❌", callback_data="Tutup ❌"),
        ]
    ]
    context.query.edit_message_text(
        "Berhasil ✅" if res else "Gagal ❌",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return -1


view_lesson_pattern = r"^LESSON\|\d+\|\d+$"
