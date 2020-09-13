from functools import wraps
from telegram import Update, User
from telegram.ext import CallbackContext
from typing import Any, Callable, List


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
