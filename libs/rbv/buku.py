import json
import os
import pytesseract
from bs4 import BeautifulSoup, Tag
from dacite import from_dict
from dataclasses import dataclass, asdict
from typing import List, Optional
from .modul import Modul
from .base import READER_URL, RETRY
from .utils import fetch_page
from ..config import IMG_PATH, IMG_URL


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
        else:
            raise NotImplementedError('Modul tidak dapat ditemukan')

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
