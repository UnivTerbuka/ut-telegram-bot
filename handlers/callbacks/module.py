from logging import getLogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from typing import List

from moodle.core.course import BaseCourse

from core.context import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from libs.utils.helpers import build_menu, make_data
from config import CALLBACK_SEPARATOR

logger = getLogger(__name__)


@message_wrapper
@assert_token
def module(update: Update, context: CoreContext):
    context.query.answer()
    datas = context.query.data.split(CALLBACK_SEPARATOR)
    # MODULE|module_id
    module_id = int(datas[1])
    cm = None
    try:
        cm = BaseCourse(context.moodle).get_course_module(module_id)
    except Exception:
        pass
    if not cm:
        context.query.edit_message_text('Data tidak ditemukan.')
        return -1

    course_module = cm.cm
    text = course_module.name + '\n'
    buttons: List[InlineKeyboardButton] = list()

    data = make_data(course_module.modname.upper(), course_module.instance)
    button = InlineKeyboardButton(course_module.name, callback_data=data)
    buttons.append(button)

    footer = [
        InlineKeyboardButton('Kembali',
                             callback_data=make_data('CONTENTS',
                                                     course_module.course,
                                                     course_module.section)),
        InlineKeyboardButton('Tutup', callback_data='CLOSE')
    ]
    keyboard = build_menu(buttons, footer_buttons=footer)

    context.query.edit_message_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard))
    return -1
