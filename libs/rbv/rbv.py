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
from urllib.parse import urlencode, urlsplit, parse_qs
try:
    from PIL import Image
except ImportError:
    import Image
from ..base import BaseRequests
from ..config import HEADERS, IMG_URL, IMG_PATH
from ..parser import query_to_dict

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
    res = session.get(modul.url, params=params)
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
    res = session.post(modul.url, params=params, data=data)
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
    end: Optional[int]
    start: Optional[int] = 1
    fetch: bool = True

    def __post_init__(self):
        self.subfolder = self.modul + '/'
        self.from_data = get_modul
        if not (self.start or self.end) and self.fetch:
            res: Response = login(self, 10)
            if res:
                pass

    def __call__(self, page: int = 1) -> Union[str, None]:
        return self.get_page(page)

    def __getitem__(self, page: int = 1) -> Union[str, None]:
        return self.get_page(page)

    def get_page(self, page: int = 1) -> Union[str, None]:
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


@cached(CACHE, key=hash_key, lock=LOCK)
def get_modul(data: dict):
    return from_dict(Modul, data)


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


class Rbv:
    def __init__(self, username: str = 'mahasiswa', password: str = 'utpeduli'):
        self.username = username
        self.password = password
        self.auth = False
        self.pages = {}

    def page_from_data(self, data: dict, page: int, url: bool = False):
        modul: Modul = get_modul(data)
        if modul(page):
            return modul.url_path(page) if url else modul.abspath(page)

    def get(self, modul: Union[Modul, str], datas=None) -> List[Modul]:
        datas = datas if datas else []
        modul = modul if isinstance(modul, Modul) else Modul(modul)
        res = login(modul, 10)
        if not res:
            return
        soup: BeautifulSoup = BeautifulSoup(res.text, 'lxml')

        def parse_th(tr: List[BeautifulSoup]) -> List[Modul]:
            for th in tr:
                a: BeautifulSoup = th.find('a')
                query: dict = query_to_dict(a['href'], False)
                datas.append(
                    Modul(
                        modul=modul.modul,
                        name=a.text,
                        doc=query.get('doc')
                    )
                )
        return parse_th(soup)

    def search(self, query: str):
        pass
