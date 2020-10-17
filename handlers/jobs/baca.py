from dacite import from_dict
from requests.exceptions import ConnectionError
from telegram.ext import CallbackContext
from core.utils.helpers import editor
from libs.rbv import Buku


def baca(context: CallbackContext, chat_id, message_id, code):
    edit_text = editor(context.bot, chat_id, message_id)
    data = {"id": code}
    try:
        buku: Buku = from_dict(Buku, data)
        if buku:
            edit_text(buku.text, reply_markup=buku.reply_markup)
        else:
            edit_text(f"Buku {code} tidak ditemukan di rbv\n")
    except ConnectionError:
        edit_text("Tidak dapat menghubungi rbv.")
    except Exception as E:
        edit_text(f"Terjadi error!\n{E}")
        raise E
    finally:
        return -1
