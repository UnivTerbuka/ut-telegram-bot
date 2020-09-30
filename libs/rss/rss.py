from fuzzywuzzy import process
from telegram import InlineQueryResult
from typing import List, Type
from .pengumuman import Pengumuman, get_pengumuman


class Rss:
    def __init__(self):
        self.pengumuman: List[Pengumuman] = get_pengumuman()
        self.pengumuman_title_dict = dict(enumerate([p.title for p in self.pengumuman]))
        inline_results: List[Type[InlineQueryResult]] = []
        inline_results += (
            [pengumuman.result_article for pengumuman in self.pengumuman]
            if self.pengumuman
            else []
        )
        self.inline_results = inline_results

    def __call__(self, query: str) -> List[Type[InlineQueryResult]]:
        return self.search(query)

    def search(self, query: str) -> List[Type[InlineQueryResult]]:
        best_p_t = process.extractBests(
            query, self.pengumuman_title_dict, score_cutoff=40, limit=3
        )
        results: List[Type[InlineQueryResult]] = []
        results += (
            [self.pengumuman[z].result_article for (x, y, z) in best_p_t]
            if best_p_t
            else []
        )
        return results
