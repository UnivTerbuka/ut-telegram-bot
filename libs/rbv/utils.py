import os
from bs4 import BeautifulSoup, Tag
from logging import getLogger
from requests import Response
from .base import SESSION, USERNAME, PASSWORD
from .page import Page

logger = getLogger(__name__)


def get_chaptcha(soup: Tag) -> str:
    c = ''
    try:
        ccaptcha: Tag = soup.find('input', {'name': 'ccaptcha'})
        q: str = ccaptcha.previous.strip().lower().split()
        # 'Berapa hasil dari 3 + 9 ='
        a = q[3]
        n = q[4]
        b = q[5]
        if n == '+':
            c = int(a) + int(b)
        elif n == '-':
            c = int(a) - int(b)
        elif n == '/' or n == ':':
            c = int(a) / int(b)
        elif n == '*' or n == 'x':
            c = int(a) * int(b)
    except Exception as E:
        logger.exception(E)
    finally:
        return str(c)


def fetch_page(url: str,
               retry: int = 0,
               res: Tag = None,
               username: str = USERNAME,
               password: str = PASSWORD) -> Response:
    if not res:
        res = SESSION.get(url)
        if not res.ok or not res.text:
            if retry > 0:
                retry -= 1
                return fetch_page(url, retry)
            return
    soup = BeautifulSoup(res.text, "lxml")
    captcha = get_chaptcha(soup)
    data = {
        '_submit_check': '1',
        'username': USERNAME,
        'password': PASSWORD,
        'ccaptcha': captcha,
        'submit': 'Submit'
    }
    res = SESSION.post(url, data=data)
    if not res.ok or 'Kode Captcha tidak sesuai!' in res.text:
        if retry > 0:
            retry -= 1
            return fetch_page(url, retry, res)
        return
    return res


def get_file(url, filepath, headers=None):
    res: Response = SESSION.get(url, headers=headers)
    if not res.ok or res.encoding == 'UTF-8':
        return False
    with open(filepath, 'wb') as f:
        for chunk in res.iter_content(1024):
            f.write(chunk)
    return True


def download(url, page, filepath, module_url, doc, subfolder):
    if os.path.isfile(filepath):
        return True
    headers = {'Referer': module_url}
    if get_file(url, filepath, headers):
        return True
    res = fetch_page(module_url, 10)
    if not res or not res.ok:
        return False
    page = (page // 10 + 1) * 10
    jsonp_url = f'http://www.pustaka.ut.ac.id/reader/services/view.php?doc={doc}&format=jsonp&subfolder={subfolder}/&page={page}'  # NOQA
    res = SESSION.get(jsonp_url, headers=headers)
    if res.ok and get_file(url, filepath,
                           headers) and os.path.isfile(filepath):
        return True
    return False


def get_txt(filepath: str) -> str:
    val = ''
    with open(filepath, 'r', encoding='utf-8') as txt:
        val = txt.read()
    return val


def fetch_page_txt(page_number: int, module_url: str, doc: str,
                   subfolder: str) -> str:
    if Page.exist(subfolder, doc, page_number):
        return get_txt(Page.get_filepath(subfolder, doc, page_number))
    headers = {'Referer': module_url}
    page = (page_number // 10 + 1) * 10
    jsonp_url = f'http://www.pustaka.ut.ac.id/reader/services/view.php?doc={doc}&format=jsonp&subfolder={subfolder}/&page={page}'  # NOQA
    res = SESSION.get(jsonp_url, headers=headers)
    if not res.ok or not res.text:
        return ''
    if res.text == "Don't waste your time trying to access this file":
        res = fetch_page(module_url, 10)
        if not res or not res.ok:
            return ''
        return fetch_page_txt(page_number, module_url, doc, subfolder)
    pages = Page.from_jsonp(res.text)
    out = None
    for page in pages:
        page.save(subfolder, doc)
        if page.number == page_number:
            out = page
    return out.txt if out else ''
