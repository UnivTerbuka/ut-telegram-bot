from __future__ import annotations
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from requests import Session
from typing import List

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/81.0",  # NOQA
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",  # NOQA
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "id,en;q=0.7,en-US;q=0.3",
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": "sia.ut.ac.id",
}


@dataclass
class Tracking:
    nim: str = ""
    penerima: str = ""
    kota_pengiriman: str = ""
    kota_tujuan: str = ""
    status_proses: str = ""
    status: str = ""

    def __str__(self):
        return "Dari {} Ke {} Status Proses {} - {}".format(
            self.kota_pengiriman, self.kota_tujuan, self.status_proses, self.status
        )

    @classmethod
    def from_tr(cls, tr: Tag) -> Tracking:
        tds = tr.findAll("td")
        return cls(
            nim=tds[0].value,
            penerima=tds[1].value,
            kota_pengiriman=tds[2].value,
            kota_tujuan=tds[3].value,
            status_proses=tds[4].value,
            status=tds[5].value,
        )

    @classmethod
    def from_tbody(cls, tbody: Tag) -> List[Tracking]:
        trs = tbody.findAll("tr")
        return [cls.from_tr(tr) for tr in trs if tr] if trs else []


def track(billing: str) -> List[Tracking]:
    if len(billing) != 20:
        return
    if not billing:
        return
    session = Session()
    session.headers.update(HEADERS)
    url = "https://sia.ut.ac.id/trackingba/"
    res = session.get(
        url=url,
    )
    if not res.ok or not res.text:
        return
    soup = BeautifulSoup(res.text, "lxml")
    token_tag = soup.find("input", {"name": "_token"})
    if not token_tag or "value" not in token_tag:
        return
    data = {"_token": token_tag["value"], "nim": billing, "simpan": ""}
    res = session.post(url + "pencarian", data=data)
    if not res.ok or not res.text:
        return
    soup = BeautifulSoup(res.text, "lxml")
    tbody = soup.find("tbody")
    if not tbody:
        return
    return Tracking.from_tbody(tbody)


if __name__ == "__main__":
    data = track("20202041711479020021")
    print(data)
