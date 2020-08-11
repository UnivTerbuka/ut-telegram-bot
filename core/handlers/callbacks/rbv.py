from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext
from core.config import CALLBACK_SEPARATOR
from libs.rbv import Modul, Rbv


def modul_decorator(func):
    def real_modul(self, update, modul, page):
        return func(self, update, modul, page)
    return real_modul


class RuangBaca:
    def __init__(self):
        self.rbv = Rbv()

    def __call__(self, update: Update, context: CallbackContext):
        if not update.callback_query:
            return
        callback_query: CallbackQuery = update.callback_query
        callback_query.answer()
        data: dict = self.parse_data(callback_query.data)
        modul: Modul = Modul.from_data(data)
        if modul:
            self.rbv(modul, data.get('page', 1))
        else:
            callback_query.edit_message_text(
                'Terjadi error / buku tidak ditemukan...'
            )

    @modul_decorator
    def answer(self, update: Update, modul: Modul, page: int, url: str):
        pass

    def create_button(self, page: int):
        return

    def create_data(self, modul: Modul, page: int = 1):
        # Data : modul|doc|start|end|page
        data = [modul.modul, modul.doc, modul.start, modul.end, page]
        return CALLBACK_SEPARATOR.join(data)

    @staticmethod
    def parse_data(data: str) -> dict:
        datas: list = data.split(CALLBACK_SEPARATOR)
        return {
            'modul': datas[0],
            'doc': datas[1],
            'start': datas[2],
            'end': datas[3]
        }


CallbackRbv = RuangBaca()
