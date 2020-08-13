from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext
from telegram.error import BadRequest
from libs.ticket import Ticket
from core.config import CALLBACK_SEPARATOR
from libs.rbv import Buku

# Data : BUKU|CODE


def rbv(update: Update, context: CallbackContext):
    callback_query: CallbackQuery = update.callback_query
    data: str = callback_query.data
