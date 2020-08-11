from logging import getLogger, Logger
from telegram.ext import Dispatcher
from .callbacks import CallbackMixin
from .commands import CommandMixin
from .conversations import ConversationMixin
from .errors import error_callback


class Handlers(CommandMixin, ConversationMixin, CallbackMixin):
    logger: Logger = None

    def __init__(self, dispacther: Dispatcher = None):
        self.dispacther = dispacther
        self.logger = getLogger(self.__class__.__name__)

    def register(self, dispacther: Dispatcher = None):
        dispacther = dispacther if dispacther else self.dispacther
        self.register_commands(dispacther)
        self.register_conversations(dispacther)
        self.register_callbacks(dispacther)
