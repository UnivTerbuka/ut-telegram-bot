import os
import requests
from bleach import clean as clean_html
from logging import getLogger
from telegram import Update
from telegram.error import BadRequest

from moodle.mod.resource import BaseResource, File, Resource

from core.context import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from libs.utils import format_html
from libs.utils.helpers import make_button
from config import CALLBACK_SEPARATOR, BLEACH_CONFIG, RES_PATH

logger = getLogger(__name__)


def forward_file(file: File, res: Resource, context: CoreContext):
    try:
        context.chat.send_document(file.fileurl)
        return
    except BadRequest:
        pass
    filename = f'{res.id}-{file.filename}'
    filepath = os.path.join(RES_PATH, filename)
    if os.path.isfile(filepath):
        context.chat.send_document(document=open(filepath, 'rb'))
        return
    try:
        with requests.get(file.fileurl, stream=True) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
        context.chat.send_document(document=open(filepath, 'rb'))
    except Exception as e:
        logger.exception(e)
    return


@message_wrapper
@assert_token
def resource(update: Update, context: CoreContext):
    context.query.answer('Mengirim dokumen...')
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

    text = res.name + '\n'
    text += clean_html(res.intro, **BLEACH_CONFIG) + '\n\n'
    files = list(res.introfiles)
    files.extend(list(res.contentfiles))

    if not files:
        context.send_message(text)
        return -1
    for file in files:
        url = file.fileurl
        if not file.isexternalfile:
            url += '?token' + context.moodle.token
        file.fileurl = url
        text += format_html.href(file.filename, url) + '\n'
    context.bot.send_message(context.chat.id, text)
    for file in files:
        forward_file(file, res, context)
    return -1


resource_pattern = r'^RESOURCE\|\d+\|\d+$'
