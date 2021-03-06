from __future__ import annotations
from bs4 import Tag
from dacite import from_dict
from dataclasses import dataclass
from typing import Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.utils.helpers import create_deep_linked_url
from config import URL_LOGO, BOT_USERNAME
from ..rbv import Modul
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
            self.modul = self.modul if self.modul else self.title.split("-")[0].strip()
        except Exception:
            self.modul = ""
        self.rbv_url = (
            self.rbv_url
            if self.rbv_url
            else f"http://www.pustaka.ut.ac.id/reader/index.php?modul={self.modul}"
            if self.modul
            else None
        )
        self.bookimages_url = (
            self.bookimages_url
            if self.bookimages_url
            else f"http://bahanajar.ut.ac.id/bookimages/{self.id}.jpg"
        )
        self.bookdetail_url = (
            self.bookdetail_url
            if self.bookdetail_url
            else f"http://bahanajar.ut.ac.id/books/bookdetail/{self.id}"
        )
        try:
            kode = Modul.validate(self.modul)
            self.depp_link_url = create_deep_linked_url(BOT_USERNAME, f"READ-{kode}")
        except Exception:
            self.depp_link_url = create_deep_linked_url(BOT_USERNAME, "READ")

    def __str__(self) -> str:
        return self.text

    @classmethod
    def from_bkthumb(cls, bkthumb: Tag) -> Book:
        data = {
            "id": int(str(bkthumb.find("a")["href"]).split("/")[-1]),
            "title": bkthumb.find("h6").text,
            "author": bkthumb.find("span").text,
        }
        return from_dict(cls, data)

    @classmethod
    def from_newb_bg(cls, newb_bg: Tag) -> Book:
        data = {
            "id": int(newb_bg.find("img")["src"].split("/")[-1].split(".")[0]),
            "title": newb_bg.find("span", class_="book_name").text,
            "author": newb_bg.find("span", class_="au_name").text,
        }
        return from_dict(cls, data)

    @property
    def text(self) -> str:
        thumb = format_html.href("\u200c", self.bookimages_url)
        texts = f"Penulis : {format_html.code(self.author)}"
        texts += f"Buku : {format_html.code(self.title)}"
        texts += f"Kode : {format_html.code(self.modul)} " + thumb
        texts += format_html.href("Baca di rbv", self.rbv_url)
        texts += format_html.href("Baca di telegram", self.depp_link_url)
        return texts

    @property
    def reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton("Detail", url=self.bookdetail_url)],
            [InlineKeyboardButton("Baca Sekarang", url=self.depp_link_url)],
            [InlineKeyboardButton("Ruang Baca Virtual", url=self.rbv_url)],
        ]
        return InlineKeyboardMarkup(keyboard)

    @property
    def inline_query_article(self) -> InlineQueryResultArticle:
        return InlineQueryResultArticle(
            id=f"{self.id}|{self.modul}",
            title=self.title,
            description=f"Bahan ajar, {self.modul} by {self.author}",
            thumb_url=URL_LOGO,
            input_message_content=InputTextMessageContent(
                message_text=self.text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False,
            ),
            reply_markup=self.reply_markup,
            thumb_height=316,
            thumb_width=316,
        )
