from __future__ import annotations
from moodle import Mdl
from sqlalchemy.orm import Session
from telegram import Bot, Chat, Message, Update, CallbackQuery
from telegram.ext import CallbackContext, Dispatcher
from telegram.utils.promise import Promise
from typing import Type, TypeVar

from core.models import User
from config import MOODLE_URL

TP = TypeVar("TP")


class CoreContext(CallbackContext):
    bot: Bot

    def __init__(self, dispatcher: Dispatcher):
        super(CoreContext, self).__init__(dispatcher)
        self._chat = None
        self._message = None
        self._session = None
        self._query = None
        self._user = None

    @property
    def chat(self) -> Chat:
        return self._chat

    @property
    def message(self) -> Message:
        return self._message

    @property
    def moodle(self) -> Mdl:
        if "moodle" in self.user_data:
            return self.user_data["moodle"]
        self.user_data["moodle"] = Mdl(MOODLE_URL, self.user.token)
        return self.user_data["moodle"]

    @property
    def query(self) -> CallbackQuery:
        return self._query

    @property
    def session(self) -> Session:
        return self._session

    @property
    def user(self) -> User:
        return self._user

    def save(self, data=None):
        data = data or self.user
        if data:
            self.session.add(data)
            self.session.commit()

    @classmethod
    def from_data(
        cls, update: Update, context: CallbackContext, session: Session, user: User
    ) -> CoreContext:
        self = cls(context.dispatcher)

        self._chat = update.effective_chat
        self._message = update.effective_message
        self._query = update.callback_query

        self._session = session
        self._user = user

        if update is not None and isinstance(update, Update):
            chat = update.effective_chat
            user = update.effective_user

            if chat:
                self._chat_data = context.dispatcher.chat_data[chat.id]
            if user:
                self._user_data = context.dispatcher.user_data[user.id]
        return self

    @staticmethod
    def result(promise: Promise, type: Type[TP]) -> TP:
        return promise.result()
