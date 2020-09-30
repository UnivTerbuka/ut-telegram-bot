from telegram import Update, MessageEntity
from telegram.ext import CallbackContext, Filters, CommandHandler, MessageHandler
from core.utils import action
from libs import shorten_link

COMMAND = "shortlink"

CREATE = range(1)


def valid_link(link: str = ""):
    return (
        link
        and (link.startswith("https://") or link.startswith("http://"))
        and " " not in link
    )


@action.typing
def short(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        "Kirimkan link yang akan dipendekkan...\n"
        "Diawali dengan https://... atau http://...\n"
        "/cancel untuk membatalkan"
    )
    return CREATE


@action.typing
def create(update: Update, context: CallbackContext):
    link: str = update.effective_message.text
    if link and not valid_link(link):
        update.effective_message.reply_text("Link tidak valid. :<")
    else:
        new_link = shorten_link(link)
        if new_link:
            update.effective_message.reply_text(
                f"""Sukses memendekan link {link}, menjadi {new_link}"""
            )
        else:
            update.effective_message.reply_text("Gagal memendekkan link")
    return -1


@action.typing
def invalid(update: Update, context: CallbackContext):
    update.effective_message.reply_text("Link tidak valid. :<")
    update.effective_message.reply_text(
        "Link tidak valid. :<\n"
        "Kirimkan link yang akan dipendekkan...\n"
        "Diawali dengan https://... atau http://...\n"
        "/cancel untuk membatalkan perintah"
    )


@action.typing
def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(f"/{COMMAND} telah dibatalkan")
    return -1


SHORTLINK = {
    "entry_points": [CommandHandler(COMMAND, short, Filters.private)],
    "states": {
        CREATE: [
            MessageHandler(Filters.text & Filters.entity(MessageEntity.URL), create)
        ]
    },
    "fallbacks": [CommandHandler("cancel", cancel)],
}
