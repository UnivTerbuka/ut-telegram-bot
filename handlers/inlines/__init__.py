from typing import List
from logging import Logger
from telegram.ext import Dispatcher, InlineQueryHandler
# InlineQuery
from .bahan_ajar import bahan_ajar
from .ticket import ticket


class InlineMixin(object):
    logger: Logger = None
    INLINES_GROUP: int = 0
    INLINES: List[InlineQueryHandler] = [
        InlineQueryHandler(ticket, pattern=r'^[A-Z]\d{10}-\d{8}$'),
        InlineQueryHandler(bahan_ajar, pattern=r'^[A-Z]{4}\d+$'),
    ]

    def register_inline(self, dispatcher: Dispatcher):
        try:
            if self.INLINES:
                for callback in self.INLINES:
                    dispatcher.add_handler(
                        callback, group=self.INLINES_GROUP
                    )
                self.logger.info('Inlines added!')
            return True
        except Exception as e:
            self.logger.exception(e)
            return False
