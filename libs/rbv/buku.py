import json
import os
from bs4 import BeautifulSoup, Tag
from dacite import from_dict
from dataclasses import dataclass, asdict
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import create_deep_linked_url
from typing import List
from .modul import Modul
from .base import READER_URL, RETRY
from .utils import fetch_page
from ..config import IMG_PATH, IMG_URL, BOT_USERNAME


def parse_th(th: Tag):
    a: Tag = th.find('a')
    return {
        'nama': a.text,
        'url': READER_URL + a.attrs.get('href', '')
    }


@dataclass
class Buku:
    id: str
    modul: List[Modul] = []

    def __post_init__(self):
        self.path = os.path.join(IMG_PATH, self.id)
        self.config_path = os.path.join(self.path, 'MODULS.json')
        if os.path.isfile(self.config_path):
            with open(self.config_path, 'r') as f:
                datas: dict = json.load(f)
            for data in datas:
                self.modul.append(
                    from_dict(Modul, datas[data])
                )
        elif self.fetch() and self.modul:
            datas = {}
            for modul in self.modul:
                datas[modul.subfolder] = asdict(modul)
            with open(self.config_path, 'w') as f:
                json.dump(datas, f)

    def fetch(self) -> bool:
        res = fetch_page(self.url, RETRY)
        if not res or not res.ok:
            return False
        soup = BeautifulSoup(res.text, 'lxml')
        for th in soup.find_all('th'):
            data = parse_th(th)
            data['subfolder'] = self.id
            self.modul.append(from_dict(Modul, data))
        return True

    @property
    def baca_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = [
            [
                InlineKeyboardButton('Baca di telegram', url=create_deep_linked_url(
                    BOT_USERNAME, f"READ|{self.id}")
                )
            ],
            [
                InlineKeyboardButton('Baca di rbv', url=self.url)
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    @property
    def reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = [
        ]
        for modul in self.modul:
            nama = modul.nama if modul.nama else modul.doc
            keyboard.append(
                [
                    InlineKeyboardButton(
                        nama, callback_data=modul.callback_data()
                    )
                ]
            )
        keyboard.append(
            [InlineKeyboardButton('Tutup', callback_data='CLOSE')]
        )
        return InlineKeyboardMarkup(keyboard)

    @property
    def text(self) -> str:
        return f"Buku {self.id}"

    @property
    def url(self) -> str:
        return f"http://www.pustaka.ut.ac.id/reader/index.php?modul={self.id}"

    def __iter__(self):
        return iter(self.modul)

    def __bool__(self) -> bool:
        return bool(self.modul)
