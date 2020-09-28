from typing import List
from logging import Logger
from telegram.ext import Dispatcher, CallbackQueryHandler
# Callbacks
from .buku import buku, buku_pattern
from .close import close, close_pattern
from .completion import completion, completion_pattern
from .content import content, content_pattern
from .course import course, course_pattern
from .discussion import discussion, discussion_pattern
from .discussions import discussions, discussions_pattern
from .folder import folder, folder_pattern
from .forum import forum, forum_pattern
from .forums import forums, forums_pattern
from .modul import modul, modul_pattern
from .module import module, module_pattern
from .page import page, page_pattern
from .resource import resource, resource_pattern
from .short import short, short_pattern
from .ticket import ticket, ticket_pattern


class CallbackMixin(object):
    logger: Logger = None
    CALLBACKS_GROUP: int = 0
    CALLBACKS: List[CallbackQueryHandler] = [
        CallbackQueryHandler(close, pattern=close_pattern),
        CallbackQueryHandler(course, pattern=course_pattern),
        CallbackQueryHandler(forum, pattern=forum_pattern),
        CallbackQueryHandler(forums, pattern=forums_pattern),
        CallbackQueryHandler(content, pattern=content_pattern),
        CallbackQueryHandler(module, pattern=module_pattern),
        CallbackQueryHandler(resource, pattern=resource_pattern),
        CallbackQueryHandler(completion, pattern=completion_pattern),
        CallbackQueryHandler(discussion, pattern=discussion_pattern),
        CallbackQueryHandler(discussions, pattern=discussions_pattern),
        CallbackQueryHandler(folder, pattern=folder_pattern),
        CallbackQueryHandler(buku, pattern=buku_pattern),
        CallbackQueryHandler(modul, pattern=modul_pattern),
        CallbackQueryHandler(page, pattern=page_pattern),
        CallbackQueryHandler(short, pattern=short_pattern),
        CallbackQueryHandler(ticket, pattern=ticket_pattern),
        CallbackQueryHandler(close),
    ]

    def register_callbacks(self, dispatcher: Dispatcher):
        try:
            if self.CALLBACKS:
                for callback in self.CALLBACKS:
                    dispatcher.add_handler(callback,
                                           group=self.CALLBACKS_GROUP)
                self.logger.info('Callbacks added!')
            return True
        except Exception as e:
            self.logger.exception(e)
            return False
