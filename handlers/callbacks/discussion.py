from bleach import clean as clean_html
from logging import getLogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import MAX_MESSAGE_LENGTH

from moodle.mod.forum import BaseForum

from core.context import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from libs.utils import format_html
from libs.utils.helpers import build_menu, make_data
from config import CALLBACK_SEPARATOR, BLEACH_CONFIG

logger = getLogger(__name__)


@message_wrapper
@assert_token
def discussion(update: Update, context: CoreContext):
    context.query.answer()
    datas = context.query.data.split(CALLBACK_SEPARATOR)
    # DISCUSSION|course_id|forum_id|discussion_id|page
    course_id = int(datas[1])
    forum_id = int(datas[2])
    discussion_id = int(datas[3])
    page = int(datas[4])

    base_forum = BaseForum(context.moodle)
    posts = []
    try:
        posts = base_forum.get_discussion_posts(discussion_id)
    except Exception as e:
        logger.exception(e)
        context.query.edit_message_text('Gagal mendapatkan diskusi.')
        raise e
    text = 'Diskusi'
    for post in posts:
        if post.isdeleted:
            continue
        subject = post.replysubject or post.subject
        title = f'{subject} [{post.author.fullname}]'
        url = f'https://elearning.ut.ac.id/mod/forum/discuss.php?d={post.id}'
        text += format_html.href(title, url) + '\n'
        text += clean_html(post.message, **BLEACH_CONFIG) + '\n\n'
    header = list()
    if len(text) > MAX_MESSAGE_LENGTH:
        MESSAGE_LENGTH = len(text)
        if page > 0:
            data = make_data('DISCUSSION', course_id, forum_id, discussion_id, page - 1)
            button = InlineKeyboardButton('Sebelumnya', callback_data=data)
            header.append(button)
        if MESSAGE_LENGTH >= (page + 1) * MAX_MESSAGE_LENGTH:
            data = make_data('DISCUSSION', course_id, forum_id, discussion_id, page + 1)
            button = InlineKeyboardButton('Selanjutnya', callback_data=data)
            header.append(button)
    back_data = make_data('DISCUSSIONS', course_id, forum_id, 1)
    footer = [
        InlineKeyboardButton('Kembali', callback_data=back_data),
        InlineKeyboardButton('Tutup', callback_data='CLOSE')
    ]
    keyboard = build_menu(header_buttons=header, footer_buttons=footer)

    context.query.edit_message_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard))
    return -1


discussion_pattern = r'^DISCUSSION\|\d+\|\d+\|\d+\|\d+$'
