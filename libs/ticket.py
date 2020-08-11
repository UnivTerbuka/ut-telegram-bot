import requests
from bs4 import BeautifulSoup
from cachetools import cached, TTLCache
from dacite import from_dict
from dataclasses import dataclass, asdict
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from threading import RLock
from typing import Union,  Optional
from .config import HEADERS, CALLBACK_SEPARATOR
from .utils import format_html


CACHE = TTLCache(25, 60)
LOCK = RLock()
URL = 'http://hallo-ut.ut.ac.id/status'


@dataclass
class Ticket:
    nomor: str
    status: Optional[str]
    warning: Optional[str]
    nama: str = '-'
    judul: str = '-'
    dibalas: str = '-'
    email: str = '-'
    topik: str = '-'
    pesan: str = '-'
    balasan: str = '-'

    def __post_init__(self):
        self.callback_data = CALLBACK_SEPARATOR.join(['TICKET', self.nomor])
        self.url = f'http://hallo-ut.ut.ac.id/status?noticket={self.nomor}'

    def __dict__(self):
        return dict(self)

    @classmethod
    @cached(CACHE, lock=LOCK)
    def from_nomor(cls, noticket: str):
        if not cls.is_nomor_valid:
            return cls(noticket)
        params = {
            'noticket': noticket
        }
        res = requests.get(URL, params=params, headers=HEADERS)
        if not res.ok or 'Tiket Tidak Ditemukan, silakan Lakukan Pencarian Ulang' in res.text:
            return cls(noticket)
        soup: BeautifulSoup = BeautifulSoup(res.text, 'lxml')
        table = soup.find('table', class_='table')
        th = table.findAll('th')
        td = table.findAll('td')
        # data,
        status = soup.find(
            'div', class_=['col-md-4', 'col-sm-4']
        ).find('span').text
        data = ''
        data = {}
        data['status'] = status
        data['nomor'] = noticket
        data['nama'] = th[2].text
        data['judul'] = th[6].text
        data['email'] = td[2].text
        data['topik'] = td[6].text
        if status == 'CLOSE':
            data['nomor'] = td[11].text
            data['pesan'] = td[15].text
            data['dibalas'] = td[8].contents[1].text
            data['balasan'] = td[8].text
        elif status == 'OPEN':
            data['nomor'] = td[10].text
            data['pesan'] = td[14].text
        else:
            data['warning'] = f"status = {status} tidak dikenali, mohon hubugi @hexatester untuk mengimplementisakannya."
        return from_dict(cls, data)

    def __str__(self):
        return self.string

    @property
    def string(self):
        if not self.status:
            return 'Nomor tiket tidak valid'
        strs = [
            f'Nomor : {format_html.href(self.nomor, self.url)}',
            f'Status : {format_html.code(self.status)}',
            f'Dibalas : {format_html.code(self.dibalas)}',
            '',
            f'Oleh : {format_html.code(self.nama)} [{self.email}]',
            '',
            f'Judul : {format_html.code(self.judul)}',
            f'Topik : {format_html.code(self.topik)}',
            '',
            f'Pesan : {format_html.code(self.pesan)}',
            f'Balasan : {format_html.code(self.balasan)}',
        ]
        if self.warning:
            strs.append(f'Warning : {self.warning}')
        return '\n'.join(strs)

    @property
    def reply_markup(self):
        keyboard = [
            [InlineKeyboardButton('Detail', url=self.url)]
        ]
        if self.status == 'OPEN':
            keyboard[0].append(InlineKeyboardButton(
                'Refresh', callback_data=self.callback_data))
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def is_nomor_valid(ticket: str = ''):
        return len(ticket) == 20 and not ' ' in ticket
