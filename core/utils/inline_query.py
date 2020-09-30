from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode
from uuid import uuid4


def article(title="", description="", message_text="", key=None, reply_markup=None):
    return InlineQueryResultArticle(
        id=key or uuid4(),
        title=title,
        description=description,
        input_message_content=InputTextMessageContent(
            message_text=message_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        ),
        reply_markup=reply_markup,
    )
