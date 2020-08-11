from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext
from requests import Session
from dataclasses import dataclass
from typing import Optional, Union
from dacite import from_dict
from bs4 import BeautifulSoup
from cachetools import cachedmethod, TTLCache
from cachetools.keys import _HashedTuple
from threading import RLock
from operator import attrgetter
from functools import partial

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'
}


USERNAME = 'mahasiswa'
PASSWORD = 'utpeduli'
SEPARATOR = '|'
URL = 'http://www.pustaka.ut.ac.id/reader/index.php'
LOCK = RLock()

session = Session()
session.headers.update(HEADERS)


def hash_key(data: dict):
    return _HashedTuple(
        (data['modul'], data['doc'])
    )


def modul_decorator(func):
    def real_modul(self, update, page):
        return func(self, update, page)
    return real_modul


@dataclass
class Modul:
    modul: str
    doc: Optional[str]
    start: Optional[int]
    end: Optional[int]

    def __post_init__(self):
        self.subfolder = self.modul + '/'

    @modul_decorator
    def __call__(self, update: Update, page: int):
        pass

    def create_button(self, page: int):
        return

    def create_data(self, page: int = 1, start: int = None, end: int = None):
        # Data : modul|doc|start|end|page
        start = start if start else self.start
        end = end if end else self.end
        data = [self.modul, self.doc, start, end, page]
        return SEPARATOR.join(data)

    @classmethod
    def from_data(cls, data: str):
        return from_dict(
            data_class=cls,
            data=data if type(data) == dict else cls.parse_data(data)
        )

    @staticmethod
    def parse_data(data: Union[str, dict]) -> dict:
        datas: list = data.split(SEPARATOR)
        return {
            'modul': datas[0],
            'doc': datas[1],
            'start': datas[2],
            'end': datas[3]
        }


class Rbv:
    def __init__(self):
        self.cache = TTLCache(50, 300)

    def __call__(self, update: Update, context: CallbackContext):
        if not update.callback_query:
            return
        callback_query: CallbackQuery = update.callback_query
        callback_query.answer()
        data: dict = Modul.parse_data(callback_query.data)
        modul: Modul = self.get_modul(data)
        if modul:
            modul(update, data.get('page', 1))
        else:
            callback_query.edit_message_text(
                'Terjadi error / buku tidak ditemukan...'
            )

    @cachedmethod(attrgetter('cache'), key=hash_key, lock=LOCK)
    def get_modul(self, data) -> Modul:
        return Modul.from_data(data)


CallbackRbv = Rbv()
