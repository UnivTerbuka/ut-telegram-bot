import os
import pytesseract
from bs4 import BeautifulSoup
from cachetools import TTLCache, cached
from cachetools.keys import _HashedTuple
from dacite import from_dict
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from PIL import Image
from requests import Session, Response
from threading import RLock
from typing import Optional, Union, List
from urllib.parse import urlencode
from core.config import HEADERS, IMG_URL, IMG_PATH
try:
    from PIL import Image
except ImportError:
    import Image
from ..base import BaseRequests

# https://www.pustaka.ut.ac.id/lib/adbi4130-pengantar-administrasi-niaga/

INDEX = 'http://www.pustaka.ut.ac.id/reader/index.php'
session: Session = BaseRequests()

TESSERACT_CMD = os.environ.get('TESSERACT_CMD')
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD if TESSERACT_CMD else r'C:\Program Files\Tesseract-OCR\tesseract.exe'

BASE_URL = 'http://www.pustaka.ut.ac.id/reader/index.php'
BASE_IMG_URL = 'http://www.pustaka.ut.ac.id/reader/services/view.php'
CACHE = TTLCache(50, 300)
LOCK = RLock()

session = Session()
session.headers.update(HEADERS)


def hash_key(data: dict):
    return _HashedTuple(
        (data['modul'], data['doc'])
    )


def login(modul, retry=0, username: str = 'mahasiswa', password: str = 'utpeduli') -> Union[Response, None]:
    params = modul.params
    res = session.get(INDEX, params=params)
    if not res.ok:
        if retry > 0:
            retry -= 1
            return login(modul, retry, username, password)
        return
    soup: BeautifulSoup = BeautifulSoup(res.text, features="lxml")
    captcha_image_url = soup.find('img')['src']
    res = session.get(captcha_image_url)
    with BytesIO(res.content) as img_bytes:
        img = Image.open(img_bytes)
        captcha: str = pytesseract.image_to_string(img)
    if captcha:
        captcha = captcha.strip()
        if '\n' in captcha:
            captcha = captcha.split('\n')[0]
    else:
        captcha = ''
    data = {
        '_submit_check': '1',
        'username': username,
        'password': password,
        'ccaptcha': captcha,
        'submit': 'Submit'
    }
    res = session.post(INDEX, params=params, data=data)
    if not res.ok or 'Perhatian: Kode Captcha tidak sesuai!' in res.text:
        if retry > 0:
            retry -= 1
            return login(modul, retry)
        return
    return res


@dataclass
class Modul:
    modul: str
    name: Optional[str]
    doc: Optional[str]
    start: Optional[int]
    end: Optional[int]

    def __post_init__(self):
        self.subfolder = self.modul + '/'

    def __call__(self, page: int) -> Union[str, None]:
        return self.get_page(page)

    def __getitem__(self, page: int) -> Union[str, None]:
        return self.get_page(page)

    def get_page(self, page: int) -> Union[str, None]:
        # Cek apa file sudah terdownload
        if os.path.isfile(self.abspath(page)):
            return self.url_path
        # Check jika page diantara start dan end
        if page > self.end or page < self.start:
            return
        # Check jika bisa langsung didownload
        if download(self, page):
            return self.url_path
        res = session.get(self.url)
        if not 'table' in res.text:
            logged_in = login(self, 10)
            if not logged_in:
                return
        if os.path.isfile(self.abspath(page)) or download(self, page):
            return self.url_path

    @classmethod
    @cached(CACHE, key=hash_key, lock=LOCK)
    def from_data(cls, data: dict):
        return from_dict(cls, data)

    @property
    def params(self):
        if self.doc:
            return {
                'subfolder': self.subfolder,
                'doc': self.doc,
            }
        else:
            return {
                'modul': self.modul
            }

    @property
    def url(self) -> str:
        return BASE_URL + '?' + urlencode(self.params)

    def doc_url(self, page: int, format: str = 'jpg') -> str:
        # http://www.pustaka.ut.ac.id/reader/services/view.php?doc=M9&format=jsonp&subfolder=MSIM4103/&page=30&callback=jQuery19108331928047621886_1597119542031
        # return ?doc=DAFIS&format=text&subfolder=MSIM4103/&page=5
        params = {
            'doc': self.doc,
            'format': format,
            'subfolder': self.subfolder,
            'page': page
        }
        return BASE_IMG_URL + '?' + urlencode(params)

    def filename(self, page: int) -> str:
        return f"{self.doc}-{page}.jpg"

    def abspath(self, page: int) -> str:
        modul_path = os.path.join(IMG_PATH, self.modul)
        Path(modul_path).mkdir(parents=True, exist_ok=True)
        return os.path.join(modul_path, self.filename(page))

    def url_path(self, page: int) -> str:
        urls = [IMG_URL, self.modul, self.filename(page)]
        return "".join(urls)


def download(modul: Modul, page: int, filepath: str = None, rewrite: bool = False) -> bool:
    if os.path.isfile(modul.abspath(page)) and not rewrite:
        return True
    try:
        filepath = filepath if filepath else modul.abspath(page)
        img_url = modul.doc_url(page)
        res: Response = session.get(img_url)
        if not res.ok:
            return False
        with BytesIO(res.content) as img:
            image = Image.open(img)
            image.save(filepath)
        return True
    except:
        return False


class Rbv(BaseRequests):
    def __init__(self, username: str = 'mahasiswa', password: str = 'utpeduli'):
        self.username = username
        self.password = password
        self.auth = False
        self.pages = {}

    def __call__(self, modul: Modul, page: int, url: bool = False):
        return modul.url_path(page) if url else modul.abspath(page)

    def parse_page(self, soup: BeautifulSoup, doc: str):
        pass

    def search(self, query: str):
        pass
