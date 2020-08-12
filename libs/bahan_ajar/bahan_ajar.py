import requests
from bs4 import BeautifulSoup
from dacite import from_dict
from dataclasses import dataclass
from requests import Session
from typing import Optional, List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode, Update
from urllib.parse import quote_plus
from uuid import uuid4
from ..rbv import Modul
from ..base import HEADERS
from ..config import URL_LOGO
from ..utils import format_html


@dataclass
class Book:
    id: int
    title: str
    author: str
    modul: Optional[str]
    epub_url: Optional[str]
    bookimages_url: Optional[str]
    bookdetail_url: Optional[str]
    rbv_url: Optional[str]

    def __post_init__(self):
        try:
            self.modul = self.modul if self.modul else self.title.split(
                '-')[0].strip()
        except:
            self.modul = ''
        self.rbv_url = self.rbv_url if self.rbv_url else f"http://www.pustaka.ut.ac.id/reader/index.php?modul={self.modul}" if self.modul else None
        self.epub_url = self.epub_url if self.epub_url else f"http://bahanajar.ut.ac.id/epub/cbc_files/{self.id}.epub"
        self.bookimages_url = self.bookimages_url if self.bookimages_url else f"http://bahanajar.ut.ac.id/bookimages/{self.id}.jpg"
        self.bookdetail_url = self.bookdetail_url if self.bookdetail_url else f"http://bahanajar.ut.ac.id/books/bookdetail/{self.id}"

    @classmethod
    def from_bkthumb(cls, bkthumb: BeautifulSoup):
        data = {
            'id': int(str(bkthumb.find('a')['href']).split('/')[-1]),
            'title': bkthumb.find('h6').text,
            'author': bkthumb.find('span').text,
        }
        return from_dict(cls, data)

    @classmethod
    def from_newb_bg(cls, newb_bg: BeautifulSoup):
        data = {
            'id': int(newb_bg.find('img')['src'].split('/')[-1].split('.')[0]),
            'title': newb_bg.find('span', class_='book_name').text,
            'author': newb_bg.find('span', class_='au_name').text,
        }
        return from_dict(cls, data)

    @property
    def text(self):
        texts = [
            f"Judul : {format_html.code(self.title)}",
            f"Penulis : {format_html.code(self.author)}",
            f"Modul : {format_html.code(self.modul)}",
            format_html.href('\u200c', self.bookimages_url)
        ]
        return '\n'.join(texts)

    @property
    def reply_markup(self):
        keyboard = [
            [InlineKeyboardButton('Detail', url=self.bookdetail_url)],
            [InlineKeyboardButton('Ruang Baca Virtual', url=self.rbv_url)],
        ]
        return InlineKeyboardMarkup(keyboard)

    @property
    def inline_query_article(self):
        return InlineQueryResultArticle(
            id=f"{self.id}|{self.modul}",
            title=self.title,
            description=f"{self.modul} by {self.author}",
            thumb_url=URL_LOGO,
            input_message_content=InputTextMessageContent(
                message_text=self.text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False),
            reply_markup=self.reply_markup,
            thumb_height=316,
            thumb_width=316,
        )


class BahanAjar:
    def __init__(self, email: str, password: str, login: bool = True):
        self.session: Session = Session()
        self.session.headers.update(HEADERS)
        self.email = email
        self.password = password
        self._my_books: List[Book] = []
        if login:
            self.login()

    def login(self, email: str = None, password: str = None) -> bool:
        email = email if email else self.email
        password = password if password else self.password
        url = f"http://bahanajar.ut.ac.id/Homes/login_frame/{email}/{password}//////?service="
        res = self.session.post(url)
        return res.ok

    @property
    def my_books(self) -> List[Book]:
        if self._my_books:
            return self._my_books
        url = 'http://bahanajar.ut.ac.id/Homes/my_books'
        res = self.session.get(url)
        if not res.ok or 'No books are available' in res.text:
            return []
        soup: BeautifulSoup = BeautifulSoup(res.text, 'lxml')
        soup = soup.find('div', id='bookHolder').find_all(
            'div', class_='publib_bkthumb')
        if not len(soup) > 0:
            return []
        else:
            self._my_books = [Book.from_bkthumb(bktm) for bktm in soup]
        return self._my_books

    @my_books.deleter
    def my_books(self):
        del self._my_books

    @staticmethod
    def search(query: str, start: int = 0) -> List[Book]:
        url = f'http://bahanajar.ut.ac.id/ebookstore/ajax_load_search_books/0/{quote_plus(query)}'
        res = requests.get(url)
        if not res.ok:
            return []
        soup: BeautifulSoup = BeautifulSoup(res.text, 'lxml')
        soup = soup.find('div', class_='book_stnd').find_all(
            'div', class_='newb_bg')
        if not len(soup) > 0:
            return []
        return [Book.from_newb_bg(newb_bg) for newb_bg in soup]
