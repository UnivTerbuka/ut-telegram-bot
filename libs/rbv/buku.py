import os
import pytesseract
from bs4 import BeautifulSoup, Tag
from dacite import from_dict
from dataclasses import dataclass
from io import BytesIO
from PIL import Image
from typing import List, Optional
from .modul import Modul
from .base import READER_URL, RETRY
from .utils import fetch_page

TESSERACT_CMD = os.environ.get('TESSERACT_CMD')
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD if TESSERACT_CMD else r'C:\Program Files\Tesseract-OCR\tesseract.exe'


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
        if self.modul:
            pass
        else:
            self.fetch()

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
    def url(self):
        return f"http://www.pustaka.ut.ac.id/reader/index.php?modul={self.id}"

    def __iter__(self):
        return iter(self.modul)

    def __bool__(self):
        return bool(self.modul)
