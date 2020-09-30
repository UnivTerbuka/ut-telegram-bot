import logging
from fuzzywuzzy import process
from typing import List, Type
from telegram import InlineQueryResult
from .faq import Faq, get_faq
from .pdf import Pdf, get_pdf
from .qna import QnA, get_qna


class Search:
    def __init__(self):
        self.faq: List[Faq] = get_faq()
        self.qna: List[QnA] = get_qna()
        self.pdf: List[Pdf] = get_pdf()
        self.faq_q_dict = dict(enumerate([faq.question for faq in self.faq]))
        self.qna_q_dict = dict(enumerate([qna.question for qna in self.qna]))
        self.pdf_t_dict = dict(enumerate([pdf.title for pdf in self.pdf]))
        self.logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, query: str, thres=3) -> List[Type[InlineQueryResult]]:
        try:
            if not query:
                return []
            self.logger.debug("Searching {}".format(query))
            results: List[Type[InlineQueryResult]] = []
            results.extend(self.best_faq(query))
            results.extend(self.best_qna(query))
            results.extend(self.best_pdf(query))
            return results
        except Exception as E:
            self.logger.exception(E)
            return []

    def best_faq(self, query: str, score_cutoff=55) -> List[Type[InlineQueryResult]]:
        best_faq = process.extractBests(
            query, self.faq_q_dict, score_cutoff=score_cutoff, limit=10
        )
        return (
            [self.faq[z].result_article for (x, y, z) in best_faq] if best_faq else []
        )

    def best_qna(
        self, query: str, score_cutoff: int = 55
    ) -> List[Type[InlineQueryResult]]:
        best_q = process.extractBests(
            query, self.qna_q_dict, score_cutoff=score_cutoff, limit=10
        )
        return [self.qna[z].result_article for (x, y, z) in best_q] if best_q else []

    def best_pdf(
        self, query: str, score_cutoff: int = 50
    ) -> List[Type[InlineQueryResult]]:
        best_f = process.extractBests(
            query, self.pdf_t_dict, score_cutoff=score_cutoff, limit=5
        )
        return [self.pdf[z].result_document for (x, y, z) in best_f] if best_f else []
