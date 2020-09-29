from logging import getLogger
from telegram import Update

from moodle.mod.resource import BaseResource

from core.context import CoreContext
from core.decorator import assert_token
from core.session import message_wrapper
from libs.utils.helpers import make_button
from config import CALLBACK_SEPARATOR

logger = getLogger(__name__)


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

    def send_file(file):
        url = file.fileurl
        if not file.isexternalfile:
            url += '?token=' + context.moodle.token
        context.chat.send_document(url)

    for file in res.introfiles:
        send_file(file)
    for file in res.contentfiles:
        send_file(file)

    return -1


resource_pattern = r'^RESOURCE\|\d+\|\d+$'
