import logging
from telegram import Update, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, Job
from telegram.error import BadRequest
from handlers.jobs.modul import modul as job_modul

# Data : MODUL|SUBFOLDER|DOC|END|PAGE
# Data : MODUL|MNAU1234|M1|12|1

logger = logging.getLogger(__name__)


def back(data: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("< Kembali", callback_data=data)]]
    )


def modul(update: Update, context: CallbackContext):
    callback_query: CallbackQuery = update.callback_query

    data: str = callback_query.data
    chat_id: int = callback_query.message.chat_id
    message_id: int = callback_query.message.message_id

    job_name = f"{chat_id}|{data}"
    callback_query.answer()
    try:
        job = Job(
            callback=job_modul,
            context=(chat_id, message_id, data),
            name=job_name,
            repeat=False,
        )
        job.run(context.dispatcher)
    except BadRequest:
        callback_query.edit_message_text(
            "Mohon untuk tidak menekan tombol berkali-kali.", reply_markup=back(data)
        )
    except Exception as e:
        logger.exception(e)
        callback_query.edit_message_text(
            f"Server error ({e}), "
            "silahkan coba beberapa saat lagi atau pm @hexatester.",
            reply_markup=back(data),
        )
        raise e
    finally:
        return -1


modul_pattern = r"^MODUL\|[A-Z]{4}\d+\|\S+\|\d+\|(txt|img)$"
