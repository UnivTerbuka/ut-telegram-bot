from __future__ import annotations
from moodle import Moodle
from sqlalchemy.orm import Session
from telegram import Message, Update
from telegram.ext import CallbackContext, Dispatcher
from typing import Optional
from core.models import User
from config import MOODLE_URL


class CoreContext(CallbackContext):
    def __init__(self, dispatcher: Dispatcher):
        super(CoreContext, self).__init__(dispatcher)
        self._message = None
        self._moodle = None
        self._session = None
        self._user = None

    @property
    def message(self) -> Message:
        return self._message

    @property
    def moodle(self) -> Optional[Moodle]:
        if not self.user or not self.user.token:
            return None
        self._moodle = Moodle(MOODLE_URL, self.user.token)
        return self._moodle

    @property
    def session(self) -> Session:
        return self._session

    @property
    def user(self) -> User:
        return self._user

    @classmethod
    def from_data(cls, update: Update, context: CallbackContext,
                  session: Session, user: User) -> CoreContext:
        self = cls(context.dispatcher)
        self._session = session
        self._user = user

        if update is not None and isinstance(update, Update):
            chat = update.effective_chat
            user = update.effective_user

            if chat:
                self._chat_data = context.dispatcher.chat_data[chat.id]
            if user:
                self._user_data = context.dispatcher.user_data[user.id]

        self._message = update.effective_message
        return self
