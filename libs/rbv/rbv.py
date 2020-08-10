import os
import pytesseract
from dataclasses import dataclass
from typing import Union, Optional
from io import BytesIO
from bs4 import BeautifulSoup
from requests import Session
from urllib.parse import urlunparse

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


def login(self, username: str, password: str, captcha: str, params: dict) ->:
    data = {
        '_submit_check': '1',
        'username': username,
        'password': password,
        'ccaptcha': captcha,
        'submit': 'Submit'
    }
    res = session.post(INDEX, params=params, data=data)
    if not res.ok or 'Perhatian: Kode Captcha tidak sesuai!' in res.text:
        return
    return res


def parse_page(soup: BeautifulSoup):
    pass


@dataclass
class SubModul:
    name: str
    modul: str
    doc: str
    start: int = 0
    end: int = 0
    now: int = 0

    def __post_init__(self):
        self.subfolder = self.modul

    def __call__(self, username: str = 'mahasiswa', password: str = 'utpeduli'):
        pass

    @property
    def params(self):
        return {
            'subfolder': self.subfolder,
            'doc': self.doc
        }


@dataclass
class Modul:
    modul: str

    def __post_init__(self):
        pass

    def __call__(self, username: str = 'mahasiswa', password: str = 'utpeduli'):
        pass

    def parse_page(self, soup: BeautifulSoup):
        pass

    @property
    def params(self):
        return {
            'modul': self.modul
        }


class Rbv(BaseRequests):
    def __init__(self, modul: str, username: str = 'mahasiswa', password: str = 'utpeduli'):
        self.modul = modul
        self.username = username
        self.password = password
        self.auth = False
        self.pages = {}

    def login(self, try_again: int = 0) -> bool:
        params = {
            'MODUL': self.modul
        }
        res = session.get(INDEX, params=params)
        if not res.ok:
            if try_again > 0:
                try_again -= 1
                return self.login(try_again)
            return False
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
            'username': self.username,
            'password': self.password,
            'ccaptcha': captcha,
            'submit': 'Submit'
        }
        res = session.post(INDEX, params=params, data=data)
        if not res.ok or 'Perhatian: Kode Captcha tidak sesuai!' in res.text:
            if try_again > 0:
                try_again -= 1
                return self.login(try_again)
            return False
        return True

    def parse_page(self, soup: BeautifulSoup, doc: str):
        pass
