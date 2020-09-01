import logging
from fuzzywuzzy import process
from typing import List, Type
from telegram import InlineQueryResult
from .faq import QnA, get_qna
from .pdf import Pdf, get_pdf


class Search:
    def __init__(self):
        self.qna: List[QnA] = get_qna()
        self.pdf: List[Pdf] = get_pdf()
        self.qna_q_dict = dict(enumerate([qna.question for qna in self.qna]))
        self.qna_a_dict = dict(enumerate([qna.answer for qna in self.qna]))
        self.pdf_t_dict = dict(enumerate([pdf.title for pdf in self.pdf]))
        self.logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, query: str, thres=3) -> List[Type[InlineQueryResult]]:
        try:
            if not query:
                return []
            self.logger.debug('Searching {}'.format(query))
            results: List[Type[InlineQueryResult]] = []
            results.extend(self.best_qna(query))
            results.extend(self.best_pdf(query))
            return results
        except Exception as E:
            self.logger.exception(E)
            return []

    def best_qna(self,
                 query: str,
                 score_cutoff: int = 55) -> List[Type[InlineQueryResult]]:
        best_q = process.extractBests(query,
                                      self.qna_q_dict,
                                      score_cutoff=score_cutoff,
                                      limit=10)
        best_a = process.extractBests(query,
                                      self.qna_a_dict,
                                      score_cutoff=score_cutoff + 10,
                                      limit=5)
        results: List[Type[InlineQueryResult]] = []
        results += [self.qna[z].result_article
                    for (x, y, z) in best_q] if best_q else []
        results += [self.qna[z].result_article
                    for (x, y, z) in best_a] if best_a else []
        return results

    def best_pdf(self,
                 query: str,
                 score_cutoff: int = 50) -> List[Type[InlineQueryResult]]:
        best_f = process.extractBests(query,
                                      self.pdf_t_dict,
                                      score_cutoff=score_cutoff,
                                      limit=5)
        return [self.pdf[z].result_document
                for (x, y, z) in best_f] if best_f else []
