from bleach import clean as clean_html
from logging import getLogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from typing import List

from moodle import MoodleException
from moodle.core.course import BaseCourse, ContentOption

from core.context import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from libs.utils.helpers import make_data
from config import CALLBACK_SEPARATOR, BLEACH_CONFIG

logger = getLogger(__name__)


@message_wrapper
@assert_token
def content(update: Update, context: CoreContext):
    context.query.answer()
    datas = context.query.data.split(CALLBACK_SEPARATOR)
    # CONTENT|course_id|section_id
    course_id = int(datas[1])
    section_id = int(datas[2])
    try:
        options = [ContentOption('sectionid', str(section_id))]
        sections = BaseCourse(context.moodle).get_contents(course_id, options)
    except MoodleException as me:
        logger.exception(me.message)
        return -1
    num = 0
    text = ''
    completions: List[InlineKeyboardButton] = list()
    keyboard: List[List[InlineKeyboardButton]] = list()
    for section in sections:
        text += clean_html(section.summary, **BLEACH_CONFIG)
        for module in section.modules:
            if module.modname == 'label':
                continue
            num += 1
            button_text = ''
            buttons: List[InlineKeyboardButton] = list()
            if module.completion and module.completion != 0:
                state = module.completiondata.state
                if state == 0:
                    # incomplete
                    if module.completion == 1:
                        button_text += str(num)
                        data = make_data('COMPLETION', course_id, module.id)
                        button = InlineKeyboardButton(
                            f"{num} ❌",
                            callback_data=data,
                        )
                        completions.append(button)
                    button_text += '❌ '
                elif state == 1:
                    # complete
                    button_text += '✅ '
                elif state == 2:
                    # complete pass
                    button_text += '☑️ '
                elif state == 3:
                    # complete fail
                    button_text += '❎ '
            if module.modname == 'forum':
                # FORUM|course_id|forum_id
                button_text += module.name
                data = make_data('FORUM', course_id, module.instance)
                button = InlineKeyboardButton(button_text, callback_data=data)
                buttons.append(button)
            elif module.modname == 'resource':
                # RESOURCE|course_id|resource_id
                button_text += module.name
                data = make_data('RESOURCE', course_id, module.instance)
                button = InlineKeyboardButton(button_text, callback_data=data)
                buttons.append(button)
            else:
                button_text += module.name
                data = make_data('MODULE', module.id)
                button = InlineKeyboardButton(button_text, callback_data=data)
                buttons.append(button)
            keyboard.append(buttons)
    footer = [
        InlineKeyboardButton('Kembali',
                             callback_data=make_data('CONTENTS', course_id)),
        InlineKeyboardButton('Tutup', callback_data='CLOSE')
    ]
    if completions:
        keyboard.append(completions)
    keyboard.append(footer)
    context.query.edit_message_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard))
    return -1
