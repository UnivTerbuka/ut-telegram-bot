import logging
from dacite import from_dict
from telegram.ext import CallbackContext, Job
from libs.rbv import Buku

logger = logging.getLogger(__name__)


def baca(context: CallbackContext):
    job: Job = context.job
    chat_id, code = job.context
    data = {"id": code}
    try:
        buku: Buku = from_dict(Buku, data)
        if buku:
            context.bot.send_message(chat_id, buku.text, reply_markup=buku.reply_markup)
        else:
            context.bot.send_message(
                chat_id,
                f"Buku {code} tidak ditemukan di rbv\n"
                "Pastikan kode buku 8 karakter (4 huruf 4 angka)"
                "Jika kode melebihi 8 karakter,\n"
                "Maka yang dituliskan adalah 8 karakter pertama.",
            )
    except Exception as E:
        logger.exception(E)
        context.bot.send_message(chat_id, "Tidak dapat menghubungi rbv.")
    return -1
