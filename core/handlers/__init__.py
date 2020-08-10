from logging import getLogger, Logger
from telegram.ext import Dispatcher
from .commands import CommandMixin
from .conversations import ConversationMixin


class Handlers(CommandMixin, ConversationMixin):
    logger: Logger = None

    def __init__(self, dispacther: Dispatcher = None):
        self.dispacther = dispacther
        self.logger = getLogger(self.__class__.__name__)

    def register(self, dispacther: Dispatcher = None):
        dispacther = dispacther if dispacther else self.dispacther
        self.register_commands(dispacther)
        self.register_conversations(dispacther)
