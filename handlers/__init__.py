from logging import getLogger, Logger
from telegram.ext import Dispatcher
from .callbacks import CallbackMixin
from .commands import CommandMixin
from .conversations import ConversationMixin
from .inlines import InlineMixin


class Handlers(CommandMixin, ConversationMixin, CallbackMixin, InlineMixin):
    logger: Logger = None

    def __init__(self, dispacther: Dispatcher = None):
        self.dispacther = dispacther
        self.logger = getLogger(self.__class__.__name__)

    def register(self, dispacther: Dispatcher = None):
        dispacther = dispacther if dispacther else self.dispacther
        self.register_conversations(dispacther)
        self.register_callbacks(dispacther)
        self.register_inline(dispacther)
        self.register_commands(dispacther)
