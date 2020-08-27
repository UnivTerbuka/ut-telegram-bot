import logging
from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext, Job
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
        callback_query.answer('Sedang mengunduh halaman, harap bersabar..')
        return -1
    else:
        callback_query.answer('Mengunduh halaman...')
        try:
            job = Job(callback=job_modul,
                      context=(chat_id, message_id, data),
                      name=job_name,
                      repeat=False)
            job.run(context.dispatcher)
        except Exception as e:
            logger.exception(e)
            callback_query.edit_message_text(
                'Terjadi error saat mengunduh halaman')
    return -1
