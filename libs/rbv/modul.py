from __future__ import annotations
import os
from logging import getLogger
from cachetools import cached, TTLCache
from dacite import from_dict
from dataclasses import dataclass
from pathlib import Path
from telegram.utils.helpers import create_deep_linked_url
from threading import RLock
from typing import Optional, Tuple, Union
from urllib.parse import urlparse, parse_qsl
from config import IMG_PATH, IMG_URL, CALLBACK_SEPARATOR, BOT_USERNAME, PUSTAKA_URL
from .utils import download, fetch_page_txt, get_max_page
from ..utils import format_html

PUSTAKA_READER = PUSTAKA_URL + "reader/index.php"
# http://www.pustaka.ut.ac.id/reader/index.php
PUSTAKA_SERVICES = PUSTAKA_URL + "reader/services/view.php"
# http://www.pustaka.ut.ac.id/reader/services/view.php

LOCK = RLock()
CACHE = TTLCache(50, 10 * 60)
logger = getLogger(__name__)


@dataclass
class Modul:
    nama: Optional[str]
    url: Optional[str]
    subfolder: Optional[str]
    doc: Optional[str]
    end: Optional[int]
    form: Optional[str] = "img"

    def __post_init__(self):
        self.url = (
            self.url
            if self.url
            else PUSTAKA_READER + f"?subfolder={self.subfolder}/&doc={self.doc}.pdf"
        )
        query = urlparse(self.url).query
        data = dict(parse_qsl(query))
        if not self.subfolder:
            self.subfolder = data.get("subfolder", "DUMP")
        self.subfolder = self.subfolder.upper()
        if not self.doc:
            self.doc = data.get("doc", "DUMP")
        if self.doc.endswith(".pdf"):
            self.doc = self.doc.rstrip(".pdf")
        self.doc = self.doc.upper()
        self.filepath = os.path.join(IMG_PATH, self.subfolder)
        if not self.end:
            if self.fetch():
                logger.debug("Berhasil mendapatkan modul {}".format(repr(self)))
            else:
                logger.debug("Gagal mendapatkan modul {}".format(repr(self)))

    def fetch(self) -> bool:
        max_page = get_max_page(self.url, self.subfolder, self.doc)
        if max_page == -1:
            return False
        self.end = max_page
        return True

    def get_page(self, page: int) -> str:
        if page < 0 or page > self.end:
            return
        url = (
            PUSTAKA_SERVICES
            + f"?doc={self.doc}&format=jpg&subfolder={self.subfolder}/&page={page}"
        )
        if download(url, page, self.abspath(page), self.url, self.doc, self.subfolder):
            return self.absurl(page)
        return

    def get_page_text(self, page: int) -> str:
        header = "Buku {} Modul {} Halaman {}\n".format(self.subfolder, self.doc, page)
        header += "Klik kanan / tahan {}, untuk membagikan halaman\n".format(
            format_html.href("Share", self.deep_linked_page(page))
        )
        return header + fetch_page_txt(page, self.url, self.doc, self.subfolder)

    def abspath(self, page: int, ext: str = "jpg") -> str:
        # /BUKU/MODUL-HALAMAN.jpg
        filename = f"{self.doc}-{page}.{ext}"
        Path(self.filepath).mkdir(parents=True, exist_ok=True)
        return os.path.join(self.filepath, filename)

    def absurl(self, page: int) -> str:
        urls = [IMG_URL, self.subfolder, f"{self.doc}-{page}.jpg"]
        return "/".join(urls)

    def deep_linked_page(self, page: int) -> str:
        return create_deep_linked_url(
            BOT_USERNAME, payload=f"READ-{self.subfolder}-{self.doc}-{page}"
        )

    def message_page(self, page: int) -> str:
        nama = self.nama if self.nama else self.subfolder
        img = self.get_page(page)
        share = self.deep_linked_page(page)
        texts = [
            f"Buku : {format_html.code(nama)}",
            format_html.href("\u200c", img),
            f"Modul : {format_html.href(self.doc, self.url)}",
            f"Halaman {page} dari {self.end} halaman.",
            f"Klik kanan / tahan {format_html.href('Share', share)}, untuk membagikan halaman",  # NOQA
        ]
        return "\n".join(texts)

    def callback_data(
        self, page: int = 1, name: str = "MODUL", txt: bool = True
    ) -> str:
        datas = [
            name,
            self.subfolder,
            self.doc,
            str(self.end),
            str(page),
            "txt" if txt else "img",
        ]
        # Datas : MODUL|subfolder|doc|end|page|form
        return CALLBACK_SEPARATOR.join(datas)

    @classmethod
    def from_data(cls, data: Union[list, str]) -> Tuple[Modul, int]:
        if type(data) == list:
            datas = data
        else:
            datas = data.split(CALLBACK_SEPARATOR)
        # Datas : MODUL|subfolder|doc|end|page|form

        @cached(CACHE, lock=LOCK)
        def get(subfolder, doc, end):
            data = {
                "subfolder": subfolder,
                "doc": doc,
                "end": end,
            }
            return from_dict(cls, data)

        return (get(subfolder=datas[1], doc=datas[2], end=int(datas[3])), int(datas[4]))

    @staticmethod
    def is_valid(id: str) -> bool:
        if " " in id:
            return False
        if "\n" in id:
            return False
        if not id[0:4].isalpha():
            return False
        if not id[4:].isdigit():
            return False
        return True

    @classmethod
    def validate(cls, id: str) -> str:
        assert cls.is_valid(id)
        return id[0:8].upper()

    @property
    def is_text(self) -> bool:
        return self.form == "txt"
