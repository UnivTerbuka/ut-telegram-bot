import bleach
from moodle.mod.forum import Forum
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List

from config import BLEACH_CONFIG
from ..utils import format_html
from ..utils.helpers import build_menu


def forum_buttons(forums: List[Forum]) -> InlineKeyboardMarkup:
    buttons: List[InlineKeyboardButton] = []
    for forum in forums:
        text = forum.name
        if forum.unreadpostscount and forum.unreadpostscount > 0:
            text += f' ({forum.unreadpostscount})'
        buttons.append(
            InlineKeyboardButton(
                text=text,
                callback_data=f"FORUM|{forum.course}|{forum.id}",
            ))
    keyboard = build_menu(
        buttons=buttons,
        n_cols=2,
        footer_buttons=InlineKeyboardButton('Tutup ❌', callback_data='CLOSE'),
    )
    return InlineKeyboardMarkup(keyboard)


def forum_text(forum: Forum) -> str:
    text = format_html.bold(forum.name) + '\n'
    text += format_html.italic(forum.type) + '\n'
    text += f'{forum.numdiscussions} diskusi' + '\n\n'
    text += bleach.clean(forum.intro, **BLEACH_CONFIG)
    return text
