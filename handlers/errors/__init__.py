import sys
import traceback
from telegram.error import (
    TelegramError,
    Unauthorized,
    BadRequest,
    TimedOut,
    ChatMigrated,
    NetworkError,
)
from telegram.utils.helpers import mention_html
from config import DEVS


def allert_devs(update, context, silent=True):
    devs = DEVS
    if not silent and update.effective_message:
        text = (
            "Hei."
            f"Maaf terjadi error / kesalahan <code>{context.error}</code>"
            " ketika memproses permintaan anda. Mohon bersabar..."
            "\nSaya akan memberitahu @hexatester tentang error ini."
            "Terimakasih..."
        )
        update.effective_message.reply_text(text)
    trace = "".join(traceback.format_tb(sys.exc_info()[2]))
    payload = ""
    if update.effective_user:
        payload += " with the user " + mention_html(
            update.effective_user.id, update.effective_user.first_name
        )
    if update.effective_chat:
        payload += f" within the chat <i>{update.effective_chat.title}</i>"
        if update.effective_chat.username:
            payload += f" (@{update.effective_chat.username})"
    if update.poll:
        payload += f" with the poll id {update.poll.id}."
    text = (
        f"Hey.\n The error <code>{context.error}</code> happened{payload}."
        f"\n\nThe full traceback:\n\n<code>{trace}"
        f"</code>"
    )
    for dev_id in devs:
        context.bot.send_message(dev_id, text)
    raise context.error


def error_callback(update, context):
    try:
        raise context.error
    except Unauthorized:
        # remove update.message.chat_id from conversation list
        return
    except BadRequest:
        # handle malformed requests - read more below!
        return allert_devs(update, context)
    except TimedOut:
        # handle slow connection problems
        return
    except NetworkError:
        # handle other connection problems
        return
    except ChatMigrated:
        # the chat_id of a group has changed, use e.new_chat_id instead
        return
    except TelegramError:
        # handle all other telegram related errors
        return allert_devs(update, context)
    return allert_devs(update, context, silent=False)
