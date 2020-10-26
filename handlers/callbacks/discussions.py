from logging import getLogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from moodle.mod.forum import BaseForum

from core import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from config import CALLBACK_SEPARATOR
from libs.utils.helpers import build_menu, make_data

logger = getLogger(__name__)


@message_wrapper
@assert_token
def discussions(update: Update, context: CoreContext):
    datas = context.query.data.split(CALLBACK_SEPARATOR)
    # DISCUSSIONS|course_id|forum_id|page
    course_id = int(datas[1])
    forum_id = int(datas[2])
    page = int(datas[3])

    base_forum = BaseForum(context.moodle)
    discussions = base_forum.get_forum_discussions(
        forumid=forum_id,
        sortorder=1,
        page=page,
    )
    context.query.answer()

    buttons = list()
    for discussion in discussions:
        name = discussion.name
        text = name[:30]
        if len(name) > 30:
            text += "..."
        text += f" by {discussion.userfullname}"
        data = make_data("DISCUSSION", course_id, forum_id, discussion.id, 0)
        button = InlineKeyboardButton(text, callback_data=data)
        buttons.append(button)
    header = list()
    if page > 1:
        data = make_data("DISCUSSIONS", course_id, forum_id, page - 1)
        button = InlineKeyboardButton("Sebelumnya", callback_data=data)
        header.append(button)
    if len(buttons) >= 9:
        data = make_data("DISCUSSIONS", course_id, forum_id, page + 1)
        button = InlineKeyboardButton("Selanjutnya", callback_data=data)
        header.append(button)
    back_data = make_data("FORUM", course_id, forum_id)
    footer = [
        InlineKeyboardButton("< Kembali", callback_data=back_data),
        InlineKeyboardButton("Tutup ❌", callback_data="CLOSE"),
    ]
    keyboard = build_menu(buttons, header_buttons=header, footer_buttons=footer)

    context.query.edit_message_text(
        "Daftar diskusi", reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return -1


discussions_pattern = r"^DISCUSSIONS\|\d+\|\d+\|\d+$"
