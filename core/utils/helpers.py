from telegram import Bot, Message, ReplyMarkup
from telegram.utils.promise import Promise
from typing import Callable, Optional, Type, TypeVar, Union

TP = TypeVar("TP")


def resolve(promise: Union[Promise, TP], t: Type[TP]) -> TP:
    if isinstance(promise, t):
        return t
    if isinstance(promise, Promise):
        return promise.result()
    return promise


def editor(
    bot: Bot, chat: int, message: Union[int, Message], inline_message: int = None
) -> Callable[
    [str, Optional[str], Optional[str], Optional[bool], Optional[ReplyMarkup]], Message
]:
    if isinstance(message, Promise):
        message = message.result()
    if isinstance(message, Message):
        message_id = message.message_id
    else:
        message_id = message

    def wrapper(
        text: str,
        parse_mode: str = None,
        disable_web_page_preview: bool = None,
        reply_markup: ReplyMarkup = None,
    ) -> Message:
        return bot.edit_message_text(
            text,
            chat,
            message_id,
            inline_message,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup,
        )

    return wrapper
