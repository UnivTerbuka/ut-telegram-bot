from telegram import Update, InlineQuery
from telegram.ext import CallbackContext
from libs.ticket import Ticket


def ticket(update: Update, context: CallbackContext):
    query: InlineQuery = update.inline_query
    tiket: Ticket = Ticket.from_nomor(query.query)
    query.answer(results=[tiket.inline_query_article])
    return -1
