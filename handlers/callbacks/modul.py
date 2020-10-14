import logging
from requests.exceptions import ConnectionError
from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext
from telegram.error import BadRequest
from libs.utils.helpers import make_button
from handlers.jobs.modul import modul as job_modul

# Data : MODUL|SUBFOLDER|DOC|END|PAGE
# Data : MODUL|MNAU1234|M1|12|1

logger = logging.getLogger(__name__)


def modul(update: Update, context: CallbackContext):
    callback_query: CallbackQuery = update.callback_query

    data: str = callback_query.data
    chat_id: int = callback_query.message.chat_id
    message_id: int = callback_query.message.message_id

    job_name = f"{chat_id}|{data}"
    if context.job_queue.get_jobs_by_name(job_name):
        callback_query.answer("Masih menghubungi rbv...")
        return -1
    else:
        callback_query.answer()

    try:
        job_modul(context, chat_id, message_id, data)
    except ConnectionError:
        callback_query.edit_message_text(
            "Tidak dapat menghubungi rbv, mohon coba beberapa saat lagi.",
            reply_markup=make_button("Coba lagi", data),
        )
    except BadRequest:
        callback_query.edit_message_text(
            "Mohon untuk tidak menekan tombol berkali-kali.",
            reply_markup=make_button("< Kembali", data),
        )
    except Exception as e:
        logger.exception(e)
        callback_query.edit_message_text(
            f"Server error ({e}), "
            "silahkan coba beberapa saat lagi atau pm @hexatester.",
            reply_markup=make_button("< Kembali", data),
        )
        raise e
    finally:
        return -1


modul_pattern = r"^MODUL\|[A-Z]{4}\d+\|\S+\|\d+\|(txt|img)$"
