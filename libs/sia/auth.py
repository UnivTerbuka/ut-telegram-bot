from bs4 import BeautifulSoup
from .base import BaseSia


class AuthMixin(BaseSia):
    def login(self, email: str = None, password: str = None) -> bool:
        url = 'https://sia.ut.ac.id/login'
        res = self.session.get(url)
        if not res.ok:
            return False
        soup = BeautifulSoup(res.text)
        data = {
            '_token': '',
            'email': email or getattr(self, 'email'),
            'password': password or getattr(self, 'password'),
            'captcha_answer_srs': ''
        }
        res = self.session.post(url, data=data)
        return res.status_code == 302
