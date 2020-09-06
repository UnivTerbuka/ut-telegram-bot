from cachetools import TTLCache, cached
from logging import getLogger
from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext
from telegram.utils.helpers import create_deep_linked_url
from threading import RLock

# from config import BOT_USERNAME
from libs.short_link import lookup, shorten
from libs.utils.helpers import make_button

logger = getLogger(__name__)
LOCK = RLock()
CACHE = TTLCache(20, 5 * 60)
BOT_USERNAME = 'UniversitasTerbukaBot'
DOMAIN = 'https://sl.ut.ac.id/'


def ending(book: str, i: int) -> str:
    prefix = 'BACA-BACA-BACA'[:i]
    return prefix + '-' + book if prefix else book


@cached(CACHE, lock=LOCK)
def get_book(book: str, i=0) -> str:
    url = create_deep_linked_url(BOT_USERNAME, f"READ-{book}")
    end = ending(book, i)
    res = lookup(end)
    if res == url:
        return DOMAIN + end
    res = shorten(url, end)
    if res:
        return res
    if i > 4:
        return url
    return get_book(book, i + 1)


def short(update: Update, context: CallbackContext):
    callback_query: CallbackQuery = update.callback_query
    callback_query.answer()
    # SHORT|ABCD1234
    data = str(callback_query.data)
    modul = data[6:14]

    url = get_book(modul)
    back = make_button('Kembali', callback_data='BUKU|' + modul)
    callback_query.edit_message_text(f'Share modul {modul} dengan link ' + url,
                                     reply_markup=back)
    return -1
