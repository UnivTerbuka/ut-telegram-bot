import os
import yaml
from dacite import from_dict
from dataclasses import dataclass
from telegram import (InlineQueryResultDocument, InputTextMessageContent,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from typing import List
from uuid import uuid4
from config import ROOT_PATH
from libs.utils.format_html import href

FILENAME = 'pdf.yaml'


@dataclass
class Pdf:
    title: str
    topic: str
    url: str
    caption: str = ''

    def __post_init__(self):
        self.caption = self.caption or self.title
        self.text = "{}\n{}".format(self.caption, href('Download', self.url))
        self.reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Download', url=self.url)]])

    @property
    def result_document(self) -> InlineQueryResultDocument:
        return InlineQueryResultDocument(
            id=uuid4(),
            title=self.title,
            description=self.topic,
            document_url=self.url,
            mime_type='application/pdf',
            input_message_content=InputTextMessageContent(
                self.text, disable_web_page_preview=False),
            reply_markup=self.reply_markup)


def get_pdf() -> List[Pdf]:
    pdf_yaml = os.path.join(ROOT_PATH, FILENAME)

    with open(pdf_yaml, 'rb') as f:
        datas = yaml.load(f, Loader=yaml.FullLoader)
    return [from_dict(Pdf, data) for data in datas if data]
