from bleach import clean as clean_html
from logging import getLogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from urllib.parse import unquote

from moodle.mod.url import BaseUrl

from core import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from libs.utils import format_html
from libs.utils.helpers import build_menu, make_data
from config import CALLBACK_SEPARATOR, BLEACH_CONFIG

logger = getLogger(__name__)


@message_wrapper
@assert_token
def url(update: Update, context: CoreContext):
    datas = context.query.data.split(CALLBACK_SEPARATOR)
    # URL|course_id|url_id
    course_id = int(datas[1])
    url_id = int(datas[2])
    base_url = BaseUrl(context.moodle)
    urls = base_url.get_urls_by_courses([course_id])
    context.query.answer()
    url_ = None
    for url in urls.urls:
        if url.id == url_id:
            url_ = url
            break
    if not url_ or url_.id != url_id:
        return -1

    buttons = list()
    name = unquote(url_.name)
    disable_preview = True
    if url_.externalurl:
        disable_preview = False
        button = InlineKeyboardButton(name, url_.externalurl)
        buttons.append(button)
        name = format_html.href(name, url_.externalurl)

    text = name + "\n"
    text += clean_html(url_.intro, **BLEACH_CONFIG)

    for file in url_.introfiles:
        url = file.fileurl
        if not file.isexternalfile:
            url += "?token=" + context.moodle.token
        button = InlineKeyboardButton(file.filename, url)
        buttons.append(button)

    # TODO : Use CONTENT
    back_button = make_data("COURSE", course_id)
    footer = [
        InlineKeyboardButton("< Kembali", callback_data=back_button),
        InlineKeyboardButton("Tutup ❌", callback_data="CLOSE"),
    ]

    keyboard = build_menu(buttons, footer_buttons=footer)
    context.chat.send_message(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=disable_preview,
    )
    return -1


url_pattern = r"^URL\|\d+\|\d+$"
