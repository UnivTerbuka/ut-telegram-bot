from .base import BaseRequests
from bs4 import BeautifulSoup
import requests
from config import POLR_KEY


def shorten_link(link: str, options='p', custom_ending=''):
    S = BaseRequests()
    res = S.get('https://sl.ut.ac.id/')
    if not res.ok:
        return
    soup: BeautifulSoup = BeautifulSoup(res.text, features="lxml")
    token = soup.find('input', attrs={'name': '_token'})['value']
    if custom_ending:
        data = {'link_ending': custom_ending}
        res = S.post('https://sl.ut.ac.id/api/v2/link_avail_check', data)
        if 'available' not in res.text:
            return
    data = {
        'link-url': link,
        'options': options,
        'custom-ending': custom_ending,
        '_token': token
    }
    res = S.post('https://sl.ut.ac.id/shorten', data=data)
    if res.ok:
        soup = BeautifulSoup(res.text, features="lxml")
        return soup.find('input', {'id': 'short_url'})['value']
    return


POLR = 'https://sl.ut.ac.id/api/v2/action/'


def lookup(url_ending: str,
           url_key: str = '',
           response_type: str = 'json') -> str:
    params = {
        'key': POLR_KEY,
        'url_ending': url_ending,
        'url_key': url_key,
        'response_type': response_type,
    }
    res = requests.get(POLR + 'lookup', params=params)
    result = ''
    try:
        result = res.json()['result']['long_url']
    except Exception:
        result = ''
    return result


def shorten(url: str,
            custom_ending: str,
            response_type: str = 'json',
            check: bool = False) -> str:
    if check:
        return lookup(custom_ending)
    params = {
        'key': POLR_KEY,
        'url': url,
        'custom_ending': custom_ending,
        'response_type': response_type,
    }
    res = requests.get(POLR + 'shorten', params=params)
    result = ''
    try:
        result = res.json()['result']
    except Exception:
        result = ''
    return result
