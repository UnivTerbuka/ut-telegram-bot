import os
from logging import getLogger

from bs4 import BeautifulSoup
from cachetools import cached, TTLCache
from dacite import from_dict
from dataclasses import dataclass
from pathlib import Path
from telegram.utils.helpers import create_deep_linked_url
from threading import RLock
from typing import Optional, Union
from urllib.parse import urlparse, parse_qsl
from config import IMG_PATH, IMG_URL, CALLBACK_SEPARATOR, BOT_USERNAME
from .utils import download, fetch_page
from ..utils import format_html

LOCK = RLock()
CACHE = TTLCache(50, 10 * 60)
logger = getLogger(__name__)


@dataclass
class Modul:
    nama: Optional[str]
    url: Optional[str]
    subfolder: Optional[str]
    doc: Optional[str]
    end: Optional[int]

    def __post_init__(self):
        self.url = self.url if self.url else f"http://www.pustaka.ut.ac.id/reader/index.php?subfolder={self.subfolder}/&doc={self.doc}.pdf"  # NOQA
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
            if self.fetch():
                logger.debug('Berhasil mendapatkan modul {}'.format(
                    repr(self)))
            else:
                logger.debug('Gagal mendapatkan modul {}'.format(repr(self)))

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
        url = f"http://www.pustaka.ut.ac.id/reader/services/view.php?doc={self.doc}&format=jpg&subfolder={self.subfolder}/&page={page}"  # NOQA
        if download(url, page, self.abspath(page), self.url, self.doc,
                    self.subfolder):
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

    def deep_linked_page(self, page: int) -> str:
        return create_deep_linked_url(
            BOT_USERNAME,
            payload=f"READ-{self.subfolder}-{self.doc}-{page}"
        )

    @classmethod
    def from_data(cls, data: Union[list, str]):
        if type(data) == list:
            datas = data
        else:
            datas = data.split(CALLBACK_SEPARATOR)

        @cached(CACHE, lock=LOCK)
        def get(subfolder, doc, end):
            data = {
                'subfolder': subfolder,
                'doc': doc,
                'end': end,
            }
            return from_dict(cls, data)

        return (get(subfolder=datas[1], doc=datas[2],
                    end=int(datas[3])), int(datas[4]))

    def message_page(self, page: int) -> str:
        nama = self.nama if self.nama else self.subfolder
        texts = [
            f"Buku : {format_html.code(nama)}",
            f"Modul : {format_html.code(self.doc)}",
            format_html.href('\u200c', self.get_page(page)),
            f"Halaman {page} dari {self.end} halaman.",
            "Klik tahan tombol Share, untuk membagikan halaman...",
        ]
        return '\n'.join(texts)

    def callback_data(self, page: int = 1, name: str = 'MODUL') -> str:
        datas = [name, self.subfolder, self.doc, str(self.end), str(page)]
        return CALLBACK_SEPARATOR.join(datas)

    @staticmethod
    def is_valid(id: str) -> bool:
        if ' ' in id:
            return False
        if '\n' in id:
            return False
        if not id[0:4].isalpha():
            return False
        if not id[4:].isdigit():
            return False
        return True

    @classmethod
    def validate(cls, id: str) -> str:
        assert cls.is_valid(id)
        return id[0:8].upper()
