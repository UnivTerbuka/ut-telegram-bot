from typing import List
from logging import Logger
from telegram.ext import Dispatcher, CommandHandler
# Commands
from .formulir import formulir
from .link import link
from .registrasi import registrasi
from .start import start


class CommandMixin(object):
    logger: Logger = None
    COMMANDS_GROUP: int = 0
    COMMANDS: List[CommandHandler] = [
        CommandHandler('start', start),
        CommandHandler('link', link),
        CommandHandler('formulir', formulir),
        CommandHandler('registrasi', registrasi),
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
