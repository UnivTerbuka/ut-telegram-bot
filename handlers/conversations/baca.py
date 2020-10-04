import logging
import re
from dacite import from_dict
from telegram import Update, Message
from telegram.ext import CallbackContext, Filters, CommandHandler, MessageHandler, Job
from core.utils.helpers import resolve
from handlers.jobs.baca import baca as job_baca
from handlers.jobs.modul import modul as job_modul
from libs.rbv import Modul, Buku
from libs.utils.helpers import cancel_markup
from requests.exceptions import ConnectionError

COMMAND = "baca"
GET_BOOK = range(1)
logger = logging.getLogger(__name__)


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
        message: Message = update.effective_message
        chat_id = message.chat_id
        job_name = f"{chat_id}|BACA|{code}"
        if context.job_queue.get_jobs_by_name(job_name):
            update.effective_message.reply_text(
                "Sedang mencari buku...", reply_markup=cancel_markup(job_name)
            )
            return -1
        update.effective_message.reply_text("Mencari buku...")
        job = Job(
            callback=job_baca, context=(chat_id, code), name=job_name, repeat=False
        )
        job.run(context.dispatcher)
    else:
        update.effective_message.reply_text("Kode buku tidak valid")
    return -1


def baca(update: Update, context: CallbackContext):
    msg: str = update.effective_message.text
    if len(msg) > 5:
        answer(update, msg.lstrip("/baca "), context)
        return -1
    update.effective_message.reply_text(
        "Kode buku yang aka dibaca?\n"
        "<i>Maaf jika lambat..</i>\n"
        "/cancel untuk membatalkan"
    )
    return GET_BOOK


def get_buku(update: Update, context: CallbackContext):
    code: str = update.effective_message.text
    return answer(update, code, context)


def start(update: Update, context: CallbackContext):
    code: str = update.effective_message.text
    # /start READ-ABCD1234
    # /start READ-ABCD123456
    if len(code) == 20 or len(code) == 22:
        code: str = context.args[0][5:]
        return answer(update, code, context)

    # /start READ-ABCD1234-DOC-PAGE
    # /start READ-ABCD123456-DOC-PAGE
    match = re.match(r"^\/start READ-([A-Z]{4}\d{4,6})-([A-Z0-9]+)-(\d+)$", code)
    groups = match.groups()
    if not match or len(groups) != 3:
        update.effective_message.reply_text("Kode buku tidak valid")
        return -1

    subfolder, doc, page = groups
    page = int(page)
    message = update.effective_message.reply_text("Mencari halaman...")
    message = resolve(message, Message)
    try:
        buku: Buku = from_dict(Buku, {"id": subfolder})
        if not buku:
            message.edit_text("Buku tidak ditemukan.")
            return -1

        modul: Modul = buku.get_modul(doc)
        if not modul:
            message.edit_text("Modul tidak ditemukan.")
            return -1

        chat_id = update.effective_message.chat.id
        data = f"MODUL|{subfolder}|{doc}|{modul.end}|{page}"
        job_name = f"{chat_id}|{data}"

        job = Job(
            callback=job_modul,
            context=(chat_id, message.message_id, data),
            name=job_name,
            repeat=False,
        )
        job.run(context.dispatcher)
    except ConnectionError:
        message.edit_text(
            "Tidak dapat menghubungi rbv, silahkan coba beberapa saat lagi."
        )
    except Exception as E:
        logger.exception(E)
        message.edit_text("Terjadi error.")
        raise E
    return -1


def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(f"/{COMMAND} telah dibatalkan")
    delete_data(context.user_data)
    return -1


BACA = {
    "name": COMMAND,
    "entry_points": [
        CommandHandler(COMMAND, baca, Filters.private),
        CommandHandler(
            "start",
            start,
            filters=Filters.regex(r"^\/start READ-[A-Z]{4}\d{4,6}$") & Filters.private,
        ),
        CommandHandler(
            "start",
            start,
            filters=Filters.regex(r"^\/start READ-([A-Z]{4}\d{4,6})-([A-Z0-9]+)-(\d+)$")
            & Filters.private,
        ),
    ],
    "states": {
        GET_BOOK: [
            MessageHandler(
                Filters.text & Filters.regex(r"^[a-zA-Z]{4}\d{4,6}$"), get_buku
            )
        ]
    },
    "fallbacks": [CommandHandler("cancel", cancel)],
    "conversation_timeout": 180,
}
