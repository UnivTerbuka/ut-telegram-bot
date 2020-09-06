from dataclasses import dataclass, field
from dacite import from_dict
from requests import Session
from typing import Iterator, List, Optional, Union


@dataclass
class Arg:
    url: str
    is_secret: bool = False
    custom_ending: Optional[str] = None
    response_type: Optional[str] = None

    def __dict__(self) -> dict:
        params = {'url': self.url}
        params['is_secret'] = self.is_secret
        if self.custom_ending is not None:
            params['custom_ending'] = self.custom_ending
        return params


@dataclass
class ShortenedLink:
    long_url: str
    short_url: str


@dataclass
class ShortenedLinks:
    shortened_links: List[ShortenedLink] = field(default_factory=list)


@dataclass
class Response:
    action: str
    result: Union[str, ShortenedLinks]

    def __iter__(self) -> Iterator[ShortenedLink]:
        return iter(self.result)

    def __getitem__(self, index: int) -> ShortenedLink:
        return self.result[index]

    def __len__(self) -> int:
        return len(self.result) if isinstance(self.result, list) else 1


class Polr:
    def __init__(self, domain: str, token: str, response_type: str = 'json'):
        self.domain = domain
        self.token = token
        self.response_type = response_type
        self.params = {
            'key': self.token,
            'response_type': self.response_type,
        }
        self.session = Session()

    def shorten(self,
                url,
                is_secret: bool = False,
                custom_ending: Optional[str] = None,
                response_type: Optional[str] = None) -> str:
        arg = Arg(url, is_secret, custom_ending, response_type)
        params = dict(self.params)
        params.update(dict(arg))
        res = self.session.get(url=self.domain + '/api/v2/action/shorten',
                               params=params)
        return res.text

    def shorten_bulk(self, args: List[Arg]) -> Response:
        links = [dict(arg) for arg in args]
        data = {'links': links}

        res = self.session.post(url=self.domain +
                                '/api/v2/action/shorten_bulk',
                                params=self.params,
                                data=data)
        res_data = res.json()
        return from_dict(Response, res_data)

    def lookup(self,
               url_ending: str,
               url_key: Optional[str] = None) -> Optional[Response]:
        params = dict(self.params)
        params['url_ending'] = url_ending
        if url_key is not None:
            params['url_key'] = url_key
        res = self.session.get(url=self.domain + '/api/v2/action/lookup',
                               params=params)
        if res.status_code == 404:
            return
        res_data = res.json()
        return from_dict(Response, res_data)
