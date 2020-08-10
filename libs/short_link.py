from .base import BaseRequests
from bs4 import BeautifulSoup


def shorten_link(link: str, options='p', custom_ending=''):
    S = BaseRequests()
    res = S.get('https://sl.ut.ac.id/')
    if not res.ok:
        return
    soup: BeautifulSoup = BeautifulSoup(res.text, features="lxml")
    token = soup.find('input', attrs={'name': '_token'})['value']
    data = {
        'link-url': link,
        'options': options,
        'custom-ending': custom_ending,
        '_token': token
    }
    res = S.post('https://sl.ut.ac.id/shorten', data=data)
    if res.ok:
        soup = BeautifulSoup(res.text, features="lxml")
        return soup.find('input', {'id':'short_url'})['value']
    return
