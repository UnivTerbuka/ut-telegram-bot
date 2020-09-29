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
    text += '<i>Fitur masih dikembangkan, tolong tekan tombol Buka di elearning</i>'
    buttons: List[InlineKeyboardButton] = list()

    url = f'https://elearning.ut.ac.id/mod/{course_module.modname}/view.php?id={module_id}'
    button = InlineKeyboardButton('Buka di elearning', url)
    buttons.append(button)

    data = make_data(course_module.modname.upper(), course_module.course,
                     course_module.instance)
    button = InlineKeyboardButton(course_module.name, callback_data=data)
    buttons.append(button)

    back_data = make_data('CONTENT', course_module.course,
                          course_module.section, 0)
    footer = [
        InlineKeyboardButton('< Kembali', callback_data=back_data),
        InlineKeyboardButton('Tutup ❌', callback_data='CLOSE')
    ]
    keyboard = build_menu(buttons, footer_buttons=footer)

    context.query.edit_message_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard))
    return -1


module_pattern = r'^MODULE\|\d+$'
