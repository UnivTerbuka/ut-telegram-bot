from typing import List
from logging import Logger
from telegram.ext import Dispatcher, ConversationHandler
# Conversations
from .buku import BUKU
from .shortlink import SHORTLINK
from .ticket import TICKET


class ConversationMixin(object):
    logger: Logger = None
    CONVERSATIONS_GROUP: int = 0
    CONVERSATIONS: List[ConversationHandler] = [
        ConversationHandler(**BUKU),
        ConversationHandler(**SHORTLINK),
        ConversationHandler(**TICKET),
    ]

    def register_conversations(self, dispatcher: Dispatcher):
        try:
            if self.CONVERSATIONS:
                for conversation in self.CONVERSATIONS:
                    dispatcher.add_handler(
                        conversation, group=self.CONVERSATIONS_GROUP
                    )
                self.logger.info('Conversations added!')
            return True
        except Exception as e:
            self.logger.exception(e)
            return False
