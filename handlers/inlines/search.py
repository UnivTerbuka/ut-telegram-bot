from telegram import Update, InlineQuery, InlineQueryResult
from telegram.ext import CallbackContext
from typing import List
from core.utils.inline_query import article
from libs.search.search import Search

SEARCH = Search()


def search(update: Update, context: CallbackContext):
    inline_query: InlineQuery = update.inline_query
    query = inline_query.query
    results_list: List[InlineQueryResult] = []
    if len(query) > 0:
        results_list.extend(SEARCH(query))
    if not results_list:
        results_list.append(
            article(
                title='❌ Tidak ada hasil',
                description='',
                message_text='Silahkan kunjungi @UniversitasTerbukaBot untuk mengakses layanan UT dari Telegram. 😁'  # NOQA
            ))
        inline_query.answer(results_list,
                            switch_pm_text='Bantuan',
                            switch_pm_parameter='inline-help')
        return -1
    inline_query.answer(results_list,
                        switch_pm_text='Bantuan',
                        switch_pm_parameter='inline-help')
    return -1
