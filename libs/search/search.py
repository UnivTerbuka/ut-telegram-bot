import logging
from fuzzywuzzy import process
from typing import List
from telegram import InlineQueryResult
from .faq import QnA, get_qna


class Search:
    def __init__(self):
        self.qna: List[QnA] = get_qna()
        self.qna_q_dict = dict(enumerate([qna.question for qna in self.qna]))
        self.qna_a_dict = dict(enumerate([qna.answer for qna in self.qna]))
        self.logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, query: str, thres=3) -> List[InlineQueryResult]:
        try:
            if not query:
                return []
            self.logger.debug('Searching {}'.format(query))
            best_q = process.extractBests(query, self.qna_q_dict)
            best_a = process.extractBests(query, self.qna_a_dict)
            results: List[InlineQueryResult] = []
            results += [self.qna[z].result_article for (x, y, z) in best_q]
            results += [self.qna[z].result_article for (x, y, z) in best_a]
            return results
        except Exception as E:
            self.logger.exception(E)
            return []
