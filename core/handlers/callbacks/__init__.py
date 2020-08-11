from typing import List
from logging import Logger
from telegram.ext import Dispatcher, CallbackQueryHandler
# Callbacks
from .rbv import CallbackRbv

class CallbackMixin(object):
    logger: Logger = None
    CALLBACKS_GROUP: int = 0
    CALLBACKS: List[CallbackQueryHandler] = [
    ]

    def register_callbacks(self, dispatcher: Dispatcher):
        try:
            if self.CALLBACKS:
                for callback in self.CALLBACKS:
                    dispatcher.add_handler(
                        callback, group=self.CALLBACKS_GROUP
                    )
                self.logger.info('Callbacks added!')
            return True
        except Exception as e:
            self.logger.exception(e)
            return False
