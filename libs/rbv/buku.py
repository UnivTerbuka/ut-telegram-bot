import json
import os
from logging import getLogger

from bs4 import BeautifulSoup, Tag
from dacite import from_dict
from dataclasses import dataclass, asdict
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import create_deep_linked_url
from typing import List, Optional
from config import IMG_PATH, BOT_USERNAME
from .modul import Modul
from .base import READER_URL, RETRY
from .utils import fetch_page
from ..utils import helpers

logger = getLogger(__name__)


def parse_th(th: Tag):
    a: Tag = th.find('a')
    return {'nama': a.text, 'url': READER_URL + a.attrs.get('href', '')}


@dataclass
class Buku:
    id: str
    modul: Optional[List[Modul]]
    initial: bool = True

    def __post_init__(self):
        self.id = self.id.upper()
        self.modul = self.modul if self.modul else []
        self.path = os.path.join(IMG_PATH, self.id)
        self.config_path = os.path.join(IMG_PATH, f'{self.id}.json')
        if os.path.isfile(self.config_path):
            with open(self.config_path, 'r') as f:
                datas: dict = json.load(f)
            for data in datas:
                self.modul.append(from_dict(Modul, datas[data]))
            logger.debug('Buku dari cache {}'.format(repr(self)))
        elif self.initial and self.fetch() and self.modul:
            datas = {}
            for modul in self.modul:
                datas[modul.doc] = asdict(modul)
            with open(self.config_path, 'w') as f:
                json.dump(datas, f)
            logger.debug('Berhasil mendapatkan buku {}'.format(repr(self)))

    def get_modul(self, doc: str) -> Optional[Modul]:
        for modul in self.modul:
            if modul.doc == doc:
                return modul

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
    def deep_linked_url(self) -> str:
        id_ = Modul.validate(self.id)
        return create_deep_linked_url(BOT_USERNAME, f"READ-{id_}")

    @property
    def baca_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = [[
            InlineKeyboardButton('Baca di telegram', url=self.deep_linked_url)
        ], [InlineKeyboardButton('Baca di rbv', url=self.url)]]
        return InlineKeyboardMarkup(keyboard)

    @property
    def reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = []
        for modul in self.modul:
            nama = modul.nama if modul.nama else modul.doc
            keyboard.append(
                InlineKeyboardButton(nama,
                                     callback_data=modul.callback_data()))
        share_data = 'SHORT|' + self.id
        footer = [
            InlineKeyboardButton('Share 🢅', callback_data=share_data),
            InlineKeyboardButton('Tutup ❌', callback_data='CLOSE')
        ]
        menu = helpers.build_menu(buttons=keyboard,
                                  n_cols=2,
                                  header_buttons=InlineKeyboardButton(
                                      'Ruang Baca Virtual', url=self.url),
                                  footer_buttons=footer)
        return InlineKeyboardMarkup(menu)

    @property
    def text(self) -> str:
        return f"Buku {self.id}"

    @property
    def url(self) -> str:
        return f"http://www.pustaka.ut.ac.id/reader/index.php?modul={self.id}"

    def __len__(self):
        return len(self.modul)

    def __iter__(self):
        return iter(self.modul)

    def __bool__(self) -> bool:
        return bool(self.modul)
