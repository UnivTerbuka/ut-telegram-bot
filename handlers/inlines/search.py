from telegram import Update, InlineQuery, InlineQueryResult
from telegram.ext import CallbackContext
from typing import List
from core.utils.inline_query import article
from libs.rss.rss import Rss
from libs.search.search import Search

RSS = Rss()
SEARCH = Search()
EMPTY = article(
    title="❌ Tidak ada hasil",
    description="",
    message_text="Pm @UniversitasTerbukaBot untuk mengakses layanan UT. 😁",
)


def search(update: Update, context: CallbackContext):
    inline_query: InlineQuery = update.inline_query
    query = inline_query.query
    results_list: List[InlineQueryResult] = []
    if len(query) > 0:
        results_list.extend(SEARCH(query))
        results_list.extend(RSS(query))
    if not results_list:
        if RSS.inline_results:
            results_list.extend(RSS.inline_results)
        else:
            results_list.append(EMPTY)
        inline_query.answer(
            results_list, switch_pm_text="Bantuan", switch_pm_parameter="inline-help"
        )
        return -1
    inline_query.answer(
        results_list, switch_pm_text="Bantuan", switch_pm_parameter="inline-help"
    )
    return -1
