from telegram import Update, InlineQuery
from telegram.ext import CallbackContext
from typing import List
from libs.bahan_ajar import BahanAjar, Book


def bahan_ajar(update: Update, context: CallbackContext):
    query: InlineQuery = update.inline_query
    bahan_ajars: List[Book] = BahanAjar.search(query.query)
    results = []
    if bahan_ajars:
        buku: Book = bahan_ajars[0]
        results.append(buku.inline_query_article)
    query.answer(results=results)
    return -1
