from telegram import InlineKeyboardMarkup
from libs.rbv import Modul, Buku

data = {
    'nama': 'Test modul',
    'url': '',
    'subfolder': 'TEST1234',
    'doc': 'M99',
    'end': 999,
}


class TestRbv:
    def test_create_modul(self):
        modul = Modul(**data)
        assert hasattr(modul, 'nama')
        assert hasattr(modul, 'url')
        assert hasattr(modul, 'subfolder')
        assert hasattr(modul, 'doc')
        assert hasattr(modul, 'end')
        assert type(modul.absurl(1)) == str
        assert type(modul.callback_data(1)) == str

    def test_create_buku(self):
        modul = Modul(**data)
        buku = Buku(id='TEST1234', modul=[modul], initial=False)
        assert hasattr(buku, 'id')
        assert hasattr(buku, 'modul')
        assert hasattr(buku, 'path')
        assert hasattr(buku, 'config_path')
        assert isinstance(buku.baca_reply_markup, InlineKeyboardMarkup)
        assert isinstance(buku.reply_markup, InlineKeyboardMarkup)
        assert type(buku.text) == str
        assert type(buku.url) == str
        assert len(buku) == 1
        assert bool(buku) is True
