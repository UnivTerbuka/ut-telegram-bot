import bleach
from bs4 import BeautifulSoup
from datetime import datetime
from requests import get as urlget
from dataclasses import dataclass, field
from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from typing import Optional, List
from uuid import uuid4
from config import BLEACH_CONFIG, HEADERS
from libs.utils.format_html import href

URL = "https://www.ut.ac.id/pengumuman/rss.xml"


def fix_domain(text: str) -> str:
    return text.replace('href="', 'href="https://www.ut.ac.id')


@dataclass
class Pengumuman:
    title: str
    link: str
    description: str
    pubdate: Optional[datetime] = field(default_factory=datetime.now)
    creator: Optional[str] = ""

    def __post_init__(self) -> None:
        self.link = self.link.strip()
        self.title = bleach.clean(self.title, tags=[], strip=True)
        self.description = bleach.clean(text=self.description, **BLEACH_CONFIG)
        self.description = fix_domain(self.description)
        if type(self.pubdate) is str:
            self.pubdate = datetime.strptime(
                self.pubdate,
                "%a, %d %b %Y %H:%M:%S %z",
            )
        self.date_str = self.pubdate.strftime("%d/%m/%Y")

    @property
    def text(self) -> str:
        texts = [
            href(self.title, self.link),
            f"Pengumuman tanggal {self.date_str} oleh {self.creator}",
            self.description,
        ]
        return "\n".join(texts).strip()

    @property
    def reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [[InlineKeyboardButton("Baca selengkapnya...", url=self.link)]]
        )

    @property
    def result_article(self) -> InlineQueryResultArticle:
        return InlineQueryResultArticle(
            id=uuid4(),
            title=self.title,
            description=f"Pengumuman, {self.date_str} oleh {self.creator}",
            input_message_content=InputTextMessageContent(self.text),
            reply_markup=self.reply_markup,
        )


def get_pengumuman() -> List[Pengumuman]:
    try:
        res = urlget(URL, headers=HEADERS)
    except Exception:
        return []
    if not res.ok:
        return []
    pengumuman = BeautifulSoup(res.text, "lxml")
    results: List[Pengumuman] = []
    for item in pengumuman.find_all("item"):
        results.append(
            Pengumuman(
                title=str(item.find("title").text),
                link=str(item.find("link").next),
                description=str(item.find("description").text),
                pubdate=str(item.find("pubdate").text),
                creator=str(item.find("dc:creator").text),
            )
        )
    return results
