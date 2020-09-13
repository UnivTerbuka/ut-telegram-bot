import bleach
import requests
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from telegram import InlineQueryResultArticle, InputTextMessageContent
from typing import List
from uuid import uuid4
from config import BLEACH_CONFIG
from ..utils import format_html

ignored_tags = ['a', 'b', 'u', 'i', 's', 'code', 'pre']


@dataclass
class Faq:
    question: str
    answer: str
    source: str
    title: str = ''

    def __post_init__(self) -> None:
        self.answer = bleach.clean(self.answer, **BLEACH_CONFIG)
        self.title = self.question
        if '.' in self.question:
            try:
                self.question.index('.', -12)
            except ValueError:
                left, _, right = self.question.partition('.')
                self.title = left[:15] + '...' + right

    def __str__(self) -> str:
        text = ''
        text += format_html.italic(self.question)
        text += '\n\n'
        text += self.answer
        text += '\n'
        text += format_html.href('Sumber', self.source)
        return text

    @property
    def result_article(self) -> InlineQueryResultArticle:
        return InlineQueryResultArticle(
            id=uuid4(),
            title=self.question,
            description="FaQ, Informasi FaQ Hallo UT",
            input_message_content=InputTextMessageContent(
                str(self), disable_web_page_preview=True))


def parse_contents(contents: Tag) -> str:
    text = ''
    for content in contents:
        if isinstance(content, Tag):
            if content.name in ignored_tags:
                text += str(content)
            elif content.name == 'ul':
                text += parse_contents(content)
            elif content.name == 'br':
                text += '\n'
            elif content.name == 'li':
                text += '● ' + str(content) + '\n'
            else:
                text += str(content) + '\n'
            continue
        text += str(content)
    return text.strip()


def parse_div_panel(panel: Tag, url: str) -> Faq:
    a = panel.find('a')
    body = panel.find('div', class_='panel-body')
    answer = parse_contents(body)
    return Faq(question=a.get_text(strip=True),
               answer=answer or str(body),
               source=url + a['href'])


def get_faq(url='http://hallo-ut.ut.ac.id/informasi') -> List[Faq]:
    results: List[Faq] = list()
    try:
        res = requests.get(url)
        if not res.ok:
            return []
        soup = BeautifulSoup(res.text, 'lxml').find('div', {
            'id': 'accordion2',
            'class': 'panel-group'
        })
        for panel in soup.findAll('div', class_=['panel', 'panel-primary']):
            try:
                results.append(parse_div_panel(panel, url))
            except Exception:
                pass
    except Exception:
        pass
    return results
