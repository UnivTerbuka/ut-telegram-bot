from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext, Job
from core.utils import action
from typing import Tuple


@action.typing
def cancel_job(update: Update, context: CallbackContext):
    callback_query: CallbackQuery = update.callback_query
    callback_query.answer()
    data: str = callback_query.data
    job_name = data.lstrip("CANCEL|")
    jobs: Tuple[Job] = context.job_queue.get_jobs_by_name(job_name)
    if jobs:
        for job in jobs:
            if job.removed:
                pass
            else:
                job.schedule_removal()
        callback_query.edit_message_text("Berhasil.")
    else:
        callback_query.edit_message_text("OK.")
    return -1
