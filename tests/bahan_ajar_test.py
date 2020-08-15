from telegram import InlineQueryResultArticle, InlineKeyboardMarkup
from libs.bahan_ajar import BahanAjar, Book

book_data = {
    'id': 1,
    'title': 'tes buku',
    'author': 'author 1',
    'modul': 'TEST1234',
    'epub_url': '',
    'bookimages_url': '',
    'bookdetail_url': '',
    'rbv_url': '',
}


class TestBahanAjar:
    def test_create_book(self):
        book = Book(**book_data)
        assert hasattr(book, 'id')
        assert hasattr(book, 'title')
        assert hasattr(book, 'author')
        assert hasattr(book, 'modul')
        assert hasattr(book, 'epub_url')
        assert hasattr(book, 'bookimages_url')
        assert hasattr(book, 'bookdetail_url')
        assert hasattr(book, 'rbv_url')
        assert hasattr(book, 'depp_link_url')
        assert ' ' not in book.modul
        assert ' ' not in book.epub_url
        assert ' ' not in book.bookimages_url
        assert ' ' not in book.bookdetail_url
        assert ' ' not in book.rbv_url
        assert ' ' not in book.depp_link_url
        assert type(book.text) == str
        assert isinstance(book.reply_markup, InlineKeyboardMarkup)
        assert isinstance(book.inline_query_article, InlineQueryResultArticle)
