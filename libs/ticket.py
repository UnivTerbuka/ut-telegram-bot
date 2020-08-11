import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Union,  Optional
from .config import HEADERS

URL = 'http://hallo-ut.ut.ac.id/status'


@dataclass
class Ticket:
    nomor: str
    nama: Optional[str]
    judul: Optional[str]
    dibalas: Optional[str]
    email: Optional[str]
    topik: Optional[str]
    pesan: Optional[str]
    balasan: Optional[str]

    @classmethod
    def from_nomor(cls, noticket: str):
        params = {
            'noticket': noticket
        }
        res = requests.get(URL, params=params, headers=HEADERS)
        if not res.ok or 'Tiket Tidak Ditemukan, silakan Lakukan Pencarian Ulang' in res.text:
            return
        soup: BeautifulSoup = BeautifulSoup(res.text, 'lxml')
        table = soup.find('table', class_='table')
        th = table.findAll('th')
        td = table.findAll('td')
        return cls(
            nomor=td[11].text,
            nama=th[2].text,
            judul=th[6].text,
            dibalas=td[8].contents[1].text,
            email=td[2].text,
            topik=td[6].text,
            pesan=td[15].text,
            balasan=td[8].text,
        )

    def __str__(self):
        return self.string

    @property
    def string(self):
        strs = [
            'Nama : ' + self.nama,
            'Judul : ' + self.judul,
            'Email : ' + self.email,
            'Topik : ' + self.topik,
            'Nomor : ' + self.nomor,
            'Pesan : ',
            self.pesan,
            'Balasan : ',
            self.balasan,
        ]
        return '\n'.join(strs)
