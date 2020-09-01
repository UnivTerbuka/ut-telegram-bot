import logging
from functools import wraps
from telegram import Update
from telegram import User as TgUser
from telegram.ext import CallbackContext
from typing import Callable
from core.db import db
from core.models import User


def user_session(func: Callable) -> Callable:
    logger = logging.getLogger(func.__name__)

    @wraps(func)
    def wrapper(update: Update, context: CallbackContext):
        result = None
        try:
            user = get_user(update.effective_user)
            result = func(update, context, user)
        except Exception as e:
            logger.exception(e)
        finally:
            return result

    return wrapper


def get_user(user: TgUser) -> User:
    user_ = User.query.filter_by(id=user.id)
    if user_:
        return user_.first()
    user_ = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
    )
    db.session.add(user_)
    db.session.commit()
    return user_
