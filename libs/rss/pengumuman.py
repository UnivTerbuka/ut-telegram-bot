import bleach
from requests import get as urlget
from dataclasses import dataclass
from html import unescape
from telegram import InlineQueryResultArticle, InputTextMessageContent
from typing import Optional, List
from uuid import uuid4
from xml.etree import ElementTree
from config import BLEACH_CONFIG, HEADERS
from libs.utils.format_html import href

URL = 'https://www.ut.ac.id/pengumuman/rss.xml'


@dataclass
class Pengumuman:
    title: str
    link: str
    description: str
    pubDate: Optional[str] = ''
    creator: Optional[str] = ''

    def __post_init__(self) -> None:
        self.title = bleach.clean(unescape(self.title), tags=[])
        self.description = bleach.clean(text=unescape(self.description),
                                        **BLEACH_CONFIG)
        texts = [
            href(self.title, self.link),
            self.description,
        ]
        self.text = '\n'.join(texts)

    @property
    def result_article(self) -> InlineQueryResultArticle:
        return InlineQueryResultArticle(
            id=uuid4(),
            title=self.title,
            description=f'{self.pubDate} oleh {self.creator}',
            input_message_content=InputTextMessageContent(self.text))


def get_pengumuman() -> List[Pengumuman]:
    try:
        res = urlget(URL, headers=HEADERS)
    except Exception:
        return []
    if not res.ok:
        return []
    pengumuman = ElementTree.fromstring(res.text)
    results: List[Pengumuman] = []
    for item in pengumuman.xpath('/rss/channel/item'):
        results.append(
            Pengumuman(
                title=item.xpath("./title/text()")[0],
                link=item.xpath("./link/text()")[0],
                description=item.xpath("./description/text()")[0],
                pubDate=item.xpath("./pubDate/text()")[0],
                creator=item.xpath("./dc:creator/text()")[0],
            ))
    return results
