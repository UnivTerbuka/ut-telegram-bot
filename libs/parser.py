from bs4 import BeautifulSoup, Tag
from typing import Union
from urllib.parse import urlsplit, parse_qs
from .config import HTML_PARSER


def query_to_dict(text: str, url=True) -> dict:
    if url:
        query = urlsplit(text).query
    else:
        query = text
    params = parse_qs(query)
    return {k: v[0] for k, v in params.items()}


def simplify_html(soup: Union[Tag, str]) -> str:
    if not soup:
        return ''
    soup = soup if isinstance(soup, Tag) else BeautifulSoup(soup, HTML_PARSER)
    tags = {
        '<div>': '',
        '</div>': '\n',
        '<br>': '\n'
    }
    string = ''
    for children in soup.children:
        string += str(children).strip()
    for tag in tags:
        string = string.replace(tag, tags[tag])
    return string
