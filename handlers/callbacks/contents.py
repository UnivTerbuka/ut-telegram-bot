from logging import getLogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from moodle.core.course import BaseCourse

from core.context import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from libs.utils.helpers import build_menu, make_data
from config import CALLBACK_SEPARATOR

logger = getLogger(__name__)


@message_wrapper
@assert_token
def contents(update: Update, context: CoreContext):
    context.query.answer()
    datas = context.query.data.split(CALLBACK_SEPARATOR)
    # CONTENTS|course_id
    course_id = int(datas[1])
    buttons = list()
    sections = BaseCourse(context.moodle).get_contents(course_id)
    for section in sections:
        if section.uservisible:
            data = make_data('CONTENT', course_id, section.id)
            button = InlineKeyboardButton(section.name, callback_data=data)
            buttons.append(button)
    footer = [
        InlineKeyboardButton('Kembali', callback_data=f"COURSE|{course_id}"),
        InlineKeyboardButton('Tutup', callback_data='CLOSE')
    ]
    keyboard = build_menu(buttons, footer_buttons=footer)
    context.query.edit_message_text(
        'Daftar sesi', reply_markup=InlineKeyboardMarkup(keyboard))
    return -1
