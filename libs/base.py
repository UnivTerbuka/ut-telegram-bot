from requests import Session

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'
}


class BaseRequests(Session):
    def __init__(self):
        super(BaseRequests, self).__init__()
        self.headers.update(HEADERS)
