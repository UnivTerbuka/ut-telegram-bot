import os
from bs4 import BeautifulSoup, Tag
from logging import getLogger
from requests import Response
from config import IMG_PATH
from .base import SESSION, USERNAME, PASSWORD, VERIVY
from .page import Page

logger = getLogger(__name__)


def get_chaptcha(soup: Tag) -> str:
    c = ""
    try:
        ccaptcha: Tag = soup.find("input", {"name": "ccaptcha"})
        q: str = ccaptcha.previous.strip().lower().split()
        # 'Berapa hasil dari 3 + 9 ='
        a = q[3]
        n = q[4]
        b = q[5]
        if n == "+":
            c = int(a) + int(b)
        elif n == "-":
            c = int(a) - int(b)
        elif n == "/" or n == ":":
            c = int(a) / int(b)
        elif n == "*" or n == "x":
            c = int(a) * int(b)
    except Exception as E:
        logger.exception(E)
    finally:
        return str(c)


def fetch_page(
    url: str,
    retry: int = 0,
    res: Tag = None,
    username: str = USERNAME,
    password: str = PASSWORD,
) -> Response:
    if not res:
        res = SESSION.get(url, verify=VERIVY)
        if not res.ok or not res.text:
            if retry > 0:
                retry -= 1
                return fetch_page(url, retry)
            return
    soup = BeautifulSoup(res.text, "lxml")
    captcha = get_chaptcha(soup)
    data = {
        "_submit_check": "1",
        "username": USERNAME,
        "password": PASSWORD,
        "ccaptcha": captcha,
        "submit": "Submit",
    }
    res = SESSION.post(url, data=data, verify=VERIVY)
    if not res.ok or "Kode Captcha tidak sesuai!" in res.text:
        if retry > 0:
            retry -= 1
            return fetch_page(url, retry, res)
        return
    return res


def get_file(url, filepath, headers=None):
    res: Response = SESSION.get(url, headers=headers, verify=VERIVY)
    if not res.ok or res.encoding == "UTF-8":
        return False
    with open(filepath, "wb") as f:
        for chunk in res.iter_content(1024):
            f.write(chunk)
    return True


def download(url, page, filepath, module_url, doc, subfolder):
    if os.path.isfile(filepath):
        return True
    headers = {"Referer": module_url}
    if get_file(url, filepath, headers):
        return True
    res = fetch_page(module_url, 10)
    if not res or not res.ok:
        return False
    page = (page // 10 + 1) * 10
    jsonp_url = f"http://www.pustaka.ut.ac.id/reader/services/view.php?doc={doc}&format=jsonp&subfolder={subfolder}/&page={page}"  # NOQA
    res = SESSION.get(jsonp_url, headers=headers, verify=VERIVY)
    if res.ok and get_file(url, filepath, headers) and os.path.isfile(filepath):
        return True
    return False


def get_txt(filepath: str) -> str:
    val = ""
    with open(filepath, "r", encoding="utf-8") as txt:
        val = txt.read()
    return val


def store_txt(filepath: str, txt: str) -> str:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(txt)
    return txt


def fetch_page_json(
    page_number: int, module_url: str, doc: str, subfolder: str, retry: int = 0
) -> str:
    page = (page_number // 10 + 1) * 10
    cache_filepath = os.path.join(IMG_PATH, f"{subfolder}-{doc}-{page}.txt")
    if os.path.isfile(cache_filepath):
        return get_txt(cache_filepath)
    headers = {"Referer": module_url}
    jsonp_url = f"http://www.pustaka.ut.ac.id/reader/services/view.php?doc={doc}&format=jsonp&subfolder={subfolder}/&page={page}"  # NOQA
    res = SESSION.get(jsonp_url, headers=headers)
    if not res.ok or not res.text:
        if retry > 10:
            raise ValueError("Buku / halaman tidak ditemukan.")
        return ""
    if res.text == "Don't waste your time trying to access this file":
        if retry > 10:
            raise ValueError("Buku / halaman tidak ditemukan.")
        res = fetch_page(module_url, 10)
        if not res or not res.ok:
            return ""
        return fetch_page_json(page_number, module_url, doc, subfolder, retry + 1)
    return store_txt(cache_filepath, res.text[1:-1])


def fetch_page_txt(page_number: int, module_url: str, doc: str, subfolder: str) -> str:
    if Page.exist(subfolder, doc, page_number):
        return get_txt(Page.get_filepath(subfolder, doc, page_number))
    jsonp = fetch_page_json(page_number, module_url, doc, subfolder)
    pages = Page.from_jsonp(jsonp)
    out = None
    for page in pages:
        page.save(subfolder, doc)
        if page.number == page_number:
            out = page
    return out.txt if out else ""


def get_max_page(url: str, subfolder: str, doc: str, page_number: int = 1) -> int:
    res = fetch_page(url, retry=1)
    if not res or not res.ok:
        return -1
    max_page = None
    soup = BeautifulSoup(res.text, "lxml")
    page = (page_number // 10 + 1) * 10
    try:
        max_page = int(soup.body.script.next.split(";")[0].split("=")[-1])
    except ValueError:
        headers = {"Referer": url}
        jsonp_url = f"http://www.pustaka.ut.ac.id/reader/services/view.php?doc={doc}&format=jsonp&subfolder={subfolder}/&page={page}"  # NOQA
        res = SESSION.get(jsonp_url, headers=headers)
        if not res.ok or not res.text:
            return -1
        pages = Page.from_jsonp(res.text)
        max_page = pages[0].pages
    finally:
        return max_page
