from typing import List
from logging import Logger
from telegram.ext import Dispatcher, CommandHandler
# Commands
from .registrasi import registrasi
from .link import link
from .formulir import formulir
from .donasi import donasi
from .about import about
from .cancel import cancel
from .start import start


class CommandMixin(object):
    logger: Logger = None
    COMMANDS_GROUP: int = 0
    COMMANDS: List[CommandHandler] = [
        CommandHandler('link', link),
        CommandHandler('formulir', formulir),
        CommandHandler('registrasi', registrasi),
        CommandHandler('about', about),
        CommandHandler('donasi', donasi),
        CommandHandler('cancel', cancel),
        CommandHandler('start', start),
    ]

    def register_commands(self, dispatcher: Dispatcher):
        try:
            if self.COMMANDS:
                for conversation in self.COMMANDS:
                    dispatcher.add_handler(
                        conversation, group=self.COMMANDS_GROUP
                    )
                self.logger.info('Commands added!')
            return True
        except Exception as e:
            self.logger.exception(e)
            return False
