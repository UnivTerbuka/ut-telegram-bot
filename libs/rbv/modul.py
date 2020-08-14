import os
from bs4 import BeautifulSoup
from dacite import from_dict
from dataclasses import dataclass
from pathlib import Path
from telegram import Update, CallbackQuery
from typing import List, Optional, Union
from urllib.parse import urlparse, parse_qsl
from .base import INDEX_URL
from .utils import download, fetch_page
from ..config import IMG_PATH, IMG_URL, CALLBACK_SEPARATOR
from ..utils import format_html


@dataclass
class Modul:
    nama: Optional[str]
    url: Optional[str]
    subfolder: Optional[str]
    doc: Optional[str]
    end: Optional[int]

    def __post_init__(self):
        self.url = self.url if self.url else f"http://www.pustaka.ut.ac.id/reader/index.php?subfolder={self.subfolder}/&doc={self.doc}.pdf"
        query = urlparse(self.url).query
        data = dict(parse_qsl(query))
        if not self.subfolder:
            self.subfolder = data.get('subfolder', 'DUMP')
        self.subfolder = self.subfolder.upper()
        if not self.doc:
            self.doc = data.get('doc', 'DUMP')
        if self.doc.endswith('.pdf'):
            self.doc = self.doc.rstrip('.pdf')
        self.doc = self.doc.upper()
        self.filepath = os.path.join(IMG_PATH, self.subfolder)
        if not self.end:
            self.fetch()

    def fetch(self) -> bool:
        res = fetch_page(self.url, retry=10)
        if not res or not res.ok:
            return False
        soup = BeautifulSoup(res.text, 'lxml')
        self.end = int(soup.body.script.next.split(';')[0].split('=')[-1])
        return True

    def get_page(self, page: int) -> str:
        if page < 0 or page > self.end:
            return
        url = f"http://www.pustaka.ut.ac.id/reader/services/view.php?doc={self.doc}&format=jpg&subfolder={self.subfolder}/&page={page}"
        if download(url, page, self.abspath(page), self.url, self.doc, self.subfolder):
            return self.absurl(page)
        return

    def abspath(self, page: int) -> str:
        # /BUKU/MODUL-HALAMAN.jpg
        filename = f"{self.doc}-{page}.jpg"
        Path(self.filepath).mkdir(parents=True, exist_ok=True)
        return os.path.join(self.filepath, filename)

    def absurl(self, page: int) -> str:
        urls = [IMG_URL, self.subfolder, f"{self.doc}-{page}.jpg"]
        return "/".join(urls)

    @classmethod
    def from_data(cls, data: str):
        datas = data.split(CALLBACK_SEPARATOR)
        data = {
            'subfolder': datas[1],
            'doc': datas[2],
            'end': int(datas[3])
        }
        return (from_dict(cls, data), int(datas[4]))

    def message_page(self, page: int):
        nama = self.nama if self.nama else self.subfolder
        texts = [
            f"Buku : {format_html.code(nama)}",
            f"Modul : {format_html.code(self.doc)}",
            format_html.href('\u200c', self.get_page(page)),
            f"Halaman {page} dari {self.end} halaman.",
        ]
        return '\n'.join(texts)

    def callback_data(self, page: int = 1):
        datas = ['MODUL', self.subfolder, self.doc, str(self.end), str(page)]
        return CALLBACK_SEPARATOR.join(datas)
