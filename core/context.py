from __future__ import annotations
from moodle import Mdl
from sqlalchemy.orm import Session
from telegram import (Chat, Message, Update, CallbackQuery, ParseMode)
from telegram.ext import CallbackContext, Dispatcher
from core.models import User
from config import MOODLE_URL


class CoreDefault(object):
    def defaults(self, kwargs: dict) -> None:
        if 'parse_mode' not in kwargs:
            kwargs['parse_mode'] = ParseMode.HTML
        if 'disable_web_page_preview' not in kwargs:
            kwargs['disable_web_page_preview'] = True


class CoreChat(Chat, CoreDefault):
    def __init__(self, chat: Chat):
        super(CoreChat, self).__init__(**chat.to_dict())

    def send_message(self, *args, **kwargs):
        self.defaults(kwargs)
        return super().send_message(*args, **kwargs)


class CoreMessage(Message, CoreDefault):
    def __init__(self, message: Message):
        super(CoreMessage, self).__init__(**message.to_dict())

    def reply_text(self, *args, **kwargs):
        self.defaults(kwargs)
        return super().reply_text(*args, **kwargs)


class CoreQuery(CallbackQuery, CoreDefault):
    def __init__(self, query: CallbackQuery):
        super(CoreQuery, self).__init__(**query.to_dict())

    def edit_message_text(self, *args, **kwargs):
        self.defaults(kwargs)
        return super().edit_message_text(*args, **kwargs)


class CoreContext(CallbackContext):
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
        if 'moodle' in self.user_data:
            return self.user_data['moodle']
        self.user_data['moodle'] = Mdl(MOODLE_URL, self.user.token)
        return self.user_data['moodle']

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
    def from_data(cls, update: Update, context: CallbackContext,
                  session: Session, user: User) -> CoreContext:
        self = cls(context.dispatcher)

        self._chat = CoreChat(update.effective_chat)
        self._message = CoreMessage(update.effective_message)
        self._query = CoreQuery(update.callback_query)

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
