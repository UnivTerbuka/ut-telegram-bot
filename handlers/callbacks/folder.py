from bleach import clean as clean_html
from logging import getLogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from moodle.mod.folder import BaseFolder

from core import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from libs.utils.helpers import build_menu
from config import CALLBACK_SEPARATOR, BLEACH_CONFIG

logger = getLogger(__name__)


@message_wrapper
@assert_token
def folder(update: Update, context: CoreContext):
    context.query.answer()
    datas = context.query.data.split(CALLBACK_SEPARATOR)
    # FOLDER|course_id|folder_id
    course_id = int(datas[1])
    folder_id = int(datas[2])
    base_folder = BaseFolder(context.moodle)
    folders = base_folder.get_folders_by_courses([course_id])
    if not folders:
        context.query.edit_message_text("Data tidak ditemukan!")
        return -1
    for folder in folders:
        if folder.id == folder_id:
            break
    buttons = list()
    for file in folder.introfiles:
        if file.isexternalfile:
            button = InlineKeyboardButton(file.filename, file.fileurl)
        else:
            button = InlineKeyboardButton(
                file.filename,
                switch_inline_query_current_chat=file.fileurl,
            )
        buttons.append(button)
    text = folder.name + "\n\n"
    text += clean_html(folder.intro, **BLEACH_CONFIG)
    keyboard = build_menu(buttons)
    context.query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    return -1


folder_pattern = r"^FOLDER\|\d+\|\d+$"
