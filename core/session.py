from functools import wraps
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from telegram import Message, Update
from telegram import User as TgUser
from telegram.error import BadRequest, RetryAfter, TimedOut, Unauthorized, NetworkError
from telegram.ext import CallbackContext
from typing import Any, Callable, Optional
from moodle import MoodleException
from moodle.exception import BaseException

from . import CoreContext
from core.db import get_session
from core.exceptions import RollbackException
from core.models import User
from handlers.errors import allert_devs

# Inspired from
# https://github.com/Nukesor/ultimate-poll-bot/blob/master/pollbot/telegram/session.py


def job_wrapper(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(context: CallbackContext) -> Any:
        result = None
        try:
            session = get_session()
            result = func(context, session)
        except Exception as e:
            if not ignore_exception(e):
                raise e
        finally:
            if "session" in locals():
                session.close()
            return result

    return wrapper


def message_wrapper(
    func: Callable[[Update, CoreContext], Any]
) -> Callable[[Update, CallbackContext], Any]:
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext) -> Any:
        result = None
        try:
            session = get_session()
            message: Message = update.effective_message
            user = get_user(session, update.effective_user)
            if user.banned:
                message.chat.send_message("Anda dibanned!")
                return result
            core_context = CoreContext.from_data(update, context, session, user)
            result = func(update, core_context)
        except BaseException:
            msg = "Gagal menghubungi elearning! Coba beberapa saat lagi."
            if update.callback_query:
                update.callback_query.answer(msg, show_alert=True)
            else:
                update.effective_message.reply_text(msg)
        except RollbackException as e:
            session.rollback()
            if update.callback_query:
                update.callback_query.answer(e.message)
            else:
                update.effective_message.reply_text(e.message)
        except Exception as e:
            if not ignore_exception(e):
                allert_devs(update, context)
        finally:
            if "session" in locals():
                session.close()
            return result

    return wrapper


def get_user(session: Session, tg_user: TgUser) -> User:
    user: Optional[User] = session.query(User).get(tg_user.id)
    if user is not None and user.banned:
        return user, None

    if user is None:
        user = User(tg_user.id, tg_user.username)
        session.add(user)
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            user = session.query(User).get(tg_user.id)
            if user is None:
                raise e
    if tg_user.username is not None:
        user.username = tg_user.username.lower()

    name = tg_user.full_name
    user.name = name
    return user


def ignore_exception(exception):
    """Check whether we can safely ignore this exception."""
    if type(exception) is BadRequest:
        if (
            exception.message.startswith("Query is too old")
            or exception.message.startswith("Have no rights to send a message")
            or exception.message.startswith("Message_id_invalid")
            or exception.message.startswith("Message identifier not specified")
            or exception.message.startswith("Schedule_date_invalid")
            or exception.message.startswith("Message to edit not found")
            or exception.message.startswith("Chat_write_forbidden")
            or exception.message.startswith("Chat not found")
            or exception.message.startswith(
                "Message is not modified: specified new message content"
            )
        ):
            return True

    if type(exception) is Unauthorized:
        if exception.message.lower() == "forbidden: bot was blocked by the user":
            return True
        if exception.message.lower() == "forbidden: message_author_required":
            return True
        if (
            exception.message.lower()
            == "forbidden: bot is not a member of the supergroup chat"
        ):
            return True
        if exception.message.lower() == "forbidden: user is deactivated":
            return True
        if exception.message.lower() == "forbidden: bot was kicked from the group chat":
            return True
        if (
            exception.message.lower()
            == "forbidden: bot was kicked from the supergroup chat"
        ):
            return True
        if exception.message.lower() == "forbidden: chat_write_forbidden":
            return True

    if type(exception) is TimedOut:
        return True

    if type(exception) is RetryAfter:
        return True

    # Super low level http error
    if type(exception) is NetworkError:
        return True

    if type(exception) is MoodleException:
        return False
    return False
