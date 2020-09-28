from bleach import clean as clean_html
from logging import getLogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from moodle.mod.resource import BaseResource

from core.context import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from libs.utils.helpers import build_menu, make_data, make_button
from config import CALLBACK_SEPARATOR, BLEACH_CONFIG

logger = getLogger(__name__)


@message_wrapper
@assert_token
def resource(update: Update, context: CoreContext):
    context.query.answer()
    datas = context.query.data.split(CALLBACK_SEPARATOR)
    # RESOURCE|course_id|resource_id
    course_id = int(datas[1])
    resource_id = int(datas[2])
    base_res = BaseResource(context.moodle)
    try:
        resourses = base_res.get_resources_by_courses([course_id])
    except Exception as e:
        logger.exception(e)
        reply_markup = make_button('Coba lagi', context.query.data)
        context.query.edit_message_text(
            'Gagal mendapatkan informasi dokumen.',
            reply_markup=reply_markup,
        )
        raise e
    res = resourses.get(resource_id)
    if res:
        base_res.view_resource(res.id)
    else:
        context.query.edit_message_text('Dokumen tidak ditemukan!')
        return -1
    buttons = []
    for file in res.introfiles:
        if file.isexternalfile:
            button = InlineKeyboardButton(file.filename, url=file.fileurl)
        else:
            button = InlineKeyboardButton(
                file.filename, switch_inline_query_current_chat=file.fileurl)
        buttons.append(button)
    for file in res.contentfiles:
        if file.isexternalfile:
            button = InlineKeyboardButton(file.filename, url=file.fileurl)
        else:
            button = InlineKeyboardButton(
                file.filename, switch_inline_query_current_chat=file.fileurl)
        buttons.append(button)
    back_data = make_data('COURSE', course_id)
    footer = [
        InlineKeyboardButton('Kembali', callback_data=back_data),
        InlineKeyboardButton('Tutup', callback_data='Tutup')
    ]
    keyboard = build_menu(buttons, footer_buttons=footer)

    text = res.name + '\n\n'
    text += clean_html(res.intro, **BLEACH_CONFIG) + '\n'

    context.query.edit_message_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard))
    return -1


resource_pattern = r'^RESOURCE\|\d+\|\d+$'
