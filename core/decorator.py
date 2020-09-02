from functools import wraps
from telegram import Update
from telegram.ext import CallbackContext
from typing import Any, Callable, List


def session(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext) -> Any:
        if 'jobs' in context.user_data:
            pass
        else:
            context.user_data['jobs']: List[str] = []
        return func(update, context)

    return wrapper
