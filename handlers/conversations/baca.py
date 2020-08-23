from telegram import Update
from telegram.ext import (CallbackContext, Filters, CommandHandler,
                          MessageHandler)
from core.utils import action
from handlers.jobs.baca import baca as job_baca
from libs.rbv import Modul

COMMAND = 'baca'
GET_BOOK = range(1)


def delete_data(data: dict):
    if data and COMMAND in data:
        del data[COMMAND]


def set_data(data: dict, value):
    if data:
        data[COMMAND] = value


def get_data(data: dict):
    return data.get(COMMAND) if data else None


def answer(update: Update, code: str, context: CallbackContext = None):
    if Modul.is_valid(code):
        chat_id = update.message.chat_id
        job_name = f'BACA|{chat_id}|{code}'
        if context.job_queue.get_jobs_by_name(job_name):
            update.effective_message.reply_text('Sedang mencari buku...')
            return -1
        update.effective_message.reply_text('Mencari buku...')
        context.job_queue.run_once(callback=job_baca,
                                   when=1,
                                   context=(chat_id, code),
                                   name=job_name)
    else:
        update.effective_message.reply_text('Kode buku tidak valid')
    return -1


@action.typing
def baca(update: Update, context: CallbackContext):
    msg: str = update.effective_message.text
    if len(msg) > 5:
        answer(update, msg.lstrip('/baca '), context)
        return -1
    update.effective_message.reply_text('Kode buku yang aka dibaca?\n'
                                        '<i>Maaf jika lambat..</i>\n'
                                        '/cancel untuk membatalkan')
    return GET_BOOK


@action.typing
def get_buku(update: Update, context: CallbackContext):
    code: str = update.effective_message.text
    return answer(update, code, context)


def start(update: Update, context: CallbackContext):
    code: str = context.args[0][5:]
    return answer(update, code, context)


@action.typing
def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(f'/{COMMAND} telah dibatalkan')
    delete_data(context.user_data)
    return -1


BACA = {
    'name':
    COMMAND,
    'entry_points': [
        CommandHandler(COMMAND, baca),
        CommandHandler('start',
                       start,
                       filters=Filters.regex(r'/start READ-[a-zA-Z]{4}\d+$')),
    ],
    'states': {
        GET_BOOK: [
            MessageHandler(Filters.text & Filters.regex(r'^[A-Z]{4}\d+$'),
                           get_buku)
        ]
    },
    'fallbacks': [CommandHandler('cancel', cancel)],
    'conversation_timeout':
    180,
}
