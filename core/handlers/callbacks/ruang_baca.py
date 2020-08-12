from telegram import Update
from telegram.ext import CallbackContext
from libs.rbv import Modul, Rbv


class RuangBaca:
    def __init__(self):
        self.rbv = Rbv()
