from __future__ import annotations
import os
import ujson as json
from dacite import from_dict
from dataclasses import dataclass, field
from pathlib import Path
from typing import List
from config import IMG_PATH


@dataclass
class Font:
    fontspec: str
    size: str
    family: str
    color: str


@dataclass
class Page:
    number: int
    pages: int
    height: int
    width: int
    fonts: List[Font] = field(default_factory=list)
    text: List[list] = field(default_factory=list)

    @classmethod
    def from_jsonp(cls, jsonp: str) -> List[Page]:
        pages_data = json.loads(jsonp)
        return (
            [from_dict(cls, page_data) for page_data in pages_data]
            if pages_data
            else []
        )

    def save(self, subfolder: str, doc: str) -> None:
        filepath = self.get_filepath(subfolder, doc, self.number)
        if os.path.isfile(filepath):
            return
        with open(filepath, "w", encoding="utf-8") as txt:
            txt.write(self.txt)

    @property
    def txt(self) -> str:
        if hasattr(self, "texts"):
            return getattr(self, "texts", "")
        now = 0
        out = ""
        for (height, hLines, vline, fills, font, texts) in self.text:
            if height != now:
                out += "\n"
                now = height
            out += str(texts)
        setattr(self, "texts", out)
        return out

    @classmethod
    def exist(cls, subfolder: str, doc: str, page) -> bool:
        filepath = cls.get_filepath(subfolder, doc, page)
        return os.path.isfile(filepath)

    @staticmethod
    def get_filepath(subfolder: str, doc: str, page: int):
        # /BUKU/MODUL-HALAMAN.txt
        filepath = os.path.join(IMG_PATH, subfolder)
        filename = f"{doc}-{page}.txt"
        Path(filepath).mkdir(parents=True, exist_ok=True)
        return os.path.join(filepath, filename)
