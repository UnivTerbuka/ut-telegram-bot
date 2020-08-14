import os
import pytesseract
from bs4 import BeautifulSoup, Tag
from io import BytesIO
from PIL import Image
from requests import Response
from .base import SESSION, USERNAME, PASSWORD, DOMAIN


def fetch_page(url: str, retry: int = 0, res: Tag = None, username: str = USERNAME, password: str = PASSWORD) -> Response:
    if not res:
        res = SESSION.get(url)
        if not res.ok:
            if retry > 0:
                retry -= 1
                return fetch_page(url, retry)
            return
    soup: Tag = BeautifulSoup(res.text, features="lxml")
    captcha_image_url = soup.find('img')['src']
    res = SESSION.get(DOMAIN + captcha_image_url)
    if not res.ok:
        if retry > 0:
            retry -= 1
            return fetch_page(url, retry)
        return
    with BytesIO() as img_bytes:
        for chunk in res.iter_content(1024):
            img_bytes.write(chunk)
        img = Image.open(img_bytes)
        captcha: str = pytesseract.image_to_string(img)
    if captcha:
        captcha = captcha.strip()
        if '\n' in captcha:
            captcha = captcha.split('\n')[0]
    else:
        captcha = ''
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
    headers = {
        'Referer': module_url
    }
    if os.path.isfile(filepath):
        return True
    if get_file(url, filepath, headers):
        return True
    res = fetch_page(module_url, 10)
    if not res or not res.ok:
        return False
    page = (page//10+1)*10
    jsonp_url = f'http://www.pustaka.ut.ac.id/reader/services/view.php?doc={doc}&format=jsonp&subfolder={subfolder}/&page={page}'
    res = SESSION.get(jsonp_url, headers=headers)
    if res.ok and get_file(url, filepath, headers) and os.path.isfile(filepath):
        return True
    return False
