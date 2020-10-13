import logging
from dacite import from_dict
from requests.exceptions import ConnectionError
from telegram.ext import CallbackContext, Job
from core.utils.helpers import editor
from libs.rbv import Buku

logger = logging.getLogger(__name__)


def baca(context: CallbackContext):
    job: Job = context.job
    chat_id, code, message_id = job.context
    edit_text = editor(context.bot, chat_id, message_id)
    data = {"id": code}
    try:
        buku: Buku = from_dict(Buku, data)
        if buku:
            edit_text(buku.text, reply_markup=buku.reply_markup)
            # bot.send_message(chat_id, buku.text, reply_markup=buku.reply_markup)
        else:
            edit_text(f"Buku {code} tidak ditemukan di rbv\n")
            # bot.send_message(chat_id, f"Buku {code} tidak ditemukan di rbv\n")
    except ConnectionError:
        edit_text("Tidak dapat menghubungi rbv.")
        # bot.send_message(chat_id, "Tidak dapat menghubungi rbv.")
    except Exception as E:
        logger.exception(E)
        edit_text("Tidak dapat menghubungi rbv.")
        # bot.send_message(chat_id, "Tidak dapat menghubungi rbv.")
    return -1
