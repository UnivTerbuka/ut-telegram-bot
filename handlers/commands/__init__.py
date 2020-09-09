from typing import List
from logging import Logger
from telegram.ext import Dispatcher, CommandHandler, Filters
# Commands
from .registrasi import registrasi
from .link import link
from .formulir import formulir
from .donasi import donasi
from .about import about
from .cancel import cancel
from .inline_help import inline_help
from .start import start

private_filter = Filters.private


class CommandMixin(object):
    logger: Logger = None
    COMMANDS_GROUP: int = 0
    COMMANDS: List[CommandHandler] = [
        CommandHandler('link', link, private_filter),
        CommandHandler('formulir', formulir, private_filter),
        CommandHandler('registrasi', registrasi, private_filter),
        CommandHandler('about', about, private_filter),
        CommandHandler('donasi', donasi, private_filter),
        CommandHandler('cancel', cancel, private_filter),
        CommandHandler('start', inline_help,
                       Filters.regex(r'/start inline-help')),
        CommandHandler('start', start, private_filter),
    ]

    def register_commands(self, dispatcher: Dispatcher):
        try:
            if self.COMMANDS:
                for conversation in self.COMMANDS:
                    dispatcher.add_handler(conversation,
                                           group=self.COMMANDS_GROUP)
                self.logger.info('Commands added!')
            return True
        except Exception as e:
            self.logger.exception(e)
            return False
