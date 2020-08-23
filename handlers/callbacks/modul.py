from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext
from handlers.jobs.modul import modul as job_modul

# Data : MODUL|SUBFOLDER|DOC|END|PAGE
# Data : MODUL|MNAU1234|M1|12|1


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
        context.job_queue.run_once(
            callback=job_modul,
            when=1,
            context=(chat_id, message_id, data),
            name=job_name,
        )
    return -1
