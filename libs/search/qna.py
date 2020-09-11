import os
import yaml
from dacite import from_dict
from dataclasses import dataclass, field
from telegram import InlineQueryResultArticle, InputTextMessageContent
from typing import List
from uuid import uuid4
from config import STATIC_PATH


@dataclass
class QnA:
    answer: str
    question: str
    image: str = ''
    topic: str = '-'

    def __str__(self):
        img = f'<a href="{self.image}">\u200c</a>' if self.image else ''
        return '\n{}Topik : {}\nQ: {}\n A: {}'.format(
            img,
            self.topic,
            self.question,
            self.answer,
        )

    @property
    def result_article(self) -> InlineQueryResultArticle:
        return InlineQueryResultArticle(
            id=uuid4(),
            title=self.question,
            description=f"QnA, {self.topic}",
            input_message_content=InputTextMessageContent(
                str(self),
                disable_web_page_preview=False if self.image else True))


@dataclass
class Topic:
    topic: str
    qna: List[QnA] = field(default_factory=list)

    def __post_init__(self) -> None:
        for qna in self.qna:
            qna.topic = self.topic


def load_topics() -> List[Topic]:
    faq_yaml = os.path.join(STATIC_PATH, 'faq.yaml')

    with open(faq_yaml, 'rb') as f:
        datas = yaml.load(f, Loader=yaml.FullLoader)
    return [from_dict(Topic, data) for data in datas if data]


def get_qna() -> List[QnA]:
    topics = load_topics()
    qnas: List[QnA] = []
    for topic in topics:
        qnas.extend(topic.qna)
    return qnas
