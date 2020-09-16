from functools import wraps
from telegram import Update, User
from telegram.ext import CallbackContext
from typing import Any, Callable, List

from core.context import CoreContext
from config import DOMAIN


def only_users(users: List[int], msg: str = ''):
    def decorator(
        func: Callable[[Update, CallbackContext], Any]
    ) -> Callable[[Update, CallbackContext], Any]:
        @wraps(func)
        def wrapper(update: Update, context: CallbackContext) -> Any:
            user: User = update.effective_user
            if user.id not in users:
                if msg:
                    update.effective_message.reply_text(msg)
                return
            return func(update, context)

        return wrapper

    return decorator


def assert_token(
    func: Callable[[Update, CoreContext], Any]
) -> Callable[[Update, CoreContext], Any]:
    @wraps(func)
    def wrapper(update: Update, context: CoreContext) -> Any:
        if context.user.token is None:
            msg = 'Silahkan login di\n' + DOMAIN + 'elearning.html'
            if context.query:
                context.query.answer()
                context.query.edit_message_text(msg)
            else:
                context.message.reply_text(msg)
            return -1
        return func(update, context)

    return wrapper
