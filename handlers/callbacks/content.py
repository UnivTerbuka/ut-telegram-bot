from bleach import clean as clean_html
from logging import getLogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import MAX_MESSAGE_LENGTH
from typing import List
from urllib.parse import unquote

from moodle import MoodleException
from moodle.core.course import BaseCourse, ContentOption

from core import CoreContext, assert_token, message_wrapper
from libs.utils.helpers import make_data
from config import CALLBACK_SEPARATOR, BLEACH_CONFIG, MOODLE_D

logger = getLogger(__name__)
SUPPORTED_MOD = ["forum", "resource", "lesson", "url"]


@message_wrapper
@assert_token
def content(update: Update, context: CoreContext):
    context.query.answer()
    datas = context.query.data.split(CALLBACK_SEPARATOR)
    # CONTENT|course_id|section_id|page
    course_id = int(datas[1])
    section_id = int(datas[2])
    page = int(datas[3])
    try:
        options = [ContentOption("sectionid", str(section_id))]
        sections = BaseCourse(context.moodle).get_contents(course_id, options)
    except MoodleException as me:
        logger.exception(me.message)
        return -1
    num = 0
    text = ""
    completions: List[InlineKeyboardButton] = list()
    keyboard: List[List[InlineKeyboardButton]] = list()
    for section in sections:
        text += clean_html(section.summary, **BLEACH_CONFIG)
        for module in section.modules:
            if module.modname == "label" and not module.completion:
                continue
            num += 1
            button_text = ""
            buttons: List[InlineKeyboardButton] = list()
            if module.completion and module.completion != 0:
                state = module.completiondata.state
                if state == 0:
                    # incomplete
                    if module.completion == 1:
                        button_text += str(num)
                        data = make_data("COMPLETION", course_id, module.id)
                        button = InlineKeyboardButton(
                            f"{num} ☑️",
                            callback_data=data,
                        )
                        completions.append(button)
                    button_text += "❌ "
                elif state == 1:
                    # complete
                    button_text += "✅ "
                elif state == 2:
                    # complete pass
                    button_text += "✔️ "
                elif state == 3:
                    # complete fail
                    button_text += "❎ "
            button_text += unquote(module.name)
            if module.modname in SUPPORTED_MOD:
                # FORUM|course_id|forum_id
                data = make_data(module.modname.upper(), course_id, module.instance)
                button = InlineKeyboardButton(button_text, callback_data=data)
                buttons.append(button)
            else:
                url = MOODLE_D + f"mod/{module.modname}/view.php?id={module.id}"
                button = InlineKeyboardButton(button_text, url)
                buttons.append(button)
            keyboard.append(buttons)
    if len(text) > MAX_MESSAGE_LENGTH:
        MESSAGE_LENGTH = len(text)
        header = list()
        if page > 0:
            data = make_data("CONTENT", course_id, section_id, page - 1)
            button = InlineKeyboardButton("Sebelumnya", callback_data=data)
            header.append(button)
        if MESSAGE_LENGTH >= (page + 1) * MAX_MESSAGE_LENGTH:
            data = make_data("CONTENT", course_id, section_id, page + 1)
            button = InlineKeyboardButton("Selanjutnya", callback_data=data)
            header.append(button)
        if header:
            keyboard.insert(0, header)
    back_data = make_data("COURSE", course_id)
    down_data = context.query.data.rstrip("|") + "|"
    footer = [
        InlineKeyboardButton("< Kembali", callback_data=back_data),
        InlineKeyboardButton("⬇️ Turunkan", callback_data=down_data),
        InlineKeyboardButton("Tutup ❌", callback_data="CLOSE"),
    ]
    if completions:
        keyboard.append(completions)
    keyboard.append(footer)
    if len(datas) > 4:
        context.chat.send_message(
            text[MAX_MESSAGE_LENGTH * page : MAX_MESSAGE_LENGTH * (page + 1)],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    else:
        context.query.edit_message_text(
            text[MAX_MESSAGE_LENGTH * page : MAX_MESSAGE_LENGTH * (page + 1)],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    return -1


content_pattern = r"^CONTENT\|\d+\|\d+\|\d+\|?$"
