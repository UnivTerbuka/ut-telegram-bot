from telegram import (
    Update,
    CallbackQuery,
    Chat,
    ChosenInlineResult,
    Message,
    Poll,
    PollAnswer,
    PreCheckoutQuery,
    ShippingQuery,
    User,
    InlineQuery,
)
from typing import Optional


class CoreUpdate(Update):
    update_id: int = 0
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    inline_query: Optional[InlineQuery] = None
    chosen_inline_result: Optional[ChosenInlineResult] = None
    callback_query: Optional[CallbackQuery] = None
    shipping_query: Optional[ShippingQuery] = None
    pre_checkout_query: Optional[PreCheckoutQuery] = None
    poll: Optional[Poll] = None
    poll_answer: Optional[PollAnswer] = None
    effective_chat: Optional[Chat] = None
    effective_message: Optional[Message] = None
    effective_user: Optional[User] = None
