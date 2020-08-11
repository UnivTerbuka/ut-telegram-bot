import requests
from bs4 import BeautifulSoup
from dacite import from_dict
from dataclasses import dataclass, asdict
from typing import Union,  Optional
from .config import HEADERS
from .utils import format_html

URL = 'http://hallo-ut.ut.ac.id/status'


@dataclass
class Ticket:
    nomor: str
    status: Optional[str]
    nama: Optional[str]
    judul: Optional[str]
    dibalas: Optional[str]
    email: Optional[str]
    topik: Optional[str]
    pesan: Optional[str]
    balasan: Optional[str]
    warning: Optional[str]

    def __dict__(self):
        return dict(self)

    @classmethod
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
            data['dibalas'] = '-'
            data['balasan'] = '-'
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
            'Nama : ' + format_html.code(self.nama),
            'Email : ' + self.email,
            '',
            'Nomor : ' + format_html.code(self.nomor),
            'Status : ' + format_html.code(self.status),
            'Dibalas : ' + format_html.code(self.dibalas),
            '',
            'Topik : ' + format_html.code(self.topik),
            'Judul : ' + format_html.code(self.judul),
            '',
            'Pesan : ',
            format_html.code(self.pesan),
            'Balasan : ',
            format_html.code(self.balasan),
        ]
        if self.warning:
            strs.append('Warning : ' + self.warning)
        return '\n'.join(strs)

    @staticmethod
    def is_nomor_valid(ticket: str = ''):
        return len(ticket) == 20 and not ' ' in ticket
