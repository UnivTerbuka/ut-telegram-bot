from logging import getLogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from moodle.core.completion import BaseCompletion

from core import CoreContext, assert_token, message_wrapper
from libs.utils.helpers import make_data
from config import CALLBACK_SEPARATOR

logger = getLogger(__name__)


@message_wrapper
@assert_token
def update_completion(update: Update, context: CoreContext):
    context.query.answer()
    datas = context.query.data.split(CALLBACK_SEPARATOR)
    # COMPLETION|course_id|module_id
    course_id = int(datas[1])
    module_id = int(datas[2])
    cmplt = BaseCompletion(context.moodle)
    res = cmplt.update_activity_completion_status_manually(module_id, 1)
    logger.debug(repr(res))
    back_data = make_data("COURSE", course_id)
    keyboard = [
        [
            InlineKeyboardButton("< Kembali", callback_data=back_data),
            InlineKeyboardButton("Tutup ❌", callback_data="Tutup ❌"),
        ]
    ]
    context.query.edit_message_text(
        "Berhasil ✅" if res.status else "Gagal ❌",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return -1


update_completion_pattern = r"^COMPLETION\|\d+\|\d+$"
