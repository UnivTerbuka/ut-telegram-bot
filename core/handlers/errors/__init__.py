from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)


def error_callback(update, context):
    try:
        raise context.error
    except Unauthorized:
        # remove update.message.chat_id from conversation list
        pass
    except BadRequest:
        # handle malformed requests - read more below!
        pass
    except TimedOut:
        # handle slow connection problems
        pass
    except NetworkError:
        # handle other connection problems
        pass
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        pass
    except TelegramError:
        # handle all other telegram related errors
        pass
