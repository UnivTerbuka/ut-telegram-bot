from telegram.ext import Filters, CommandHandler, MessageHandler
from .config import COMMAND, SET_TOKEN
from .start import start
from .elearning import elearning
from .set_token import set_token
from .fallbacks import cancel

ELEARNING = {
    'name':
    COMMAND,
    'entry_points': [
        CommandHandler(COMMAND, elearning),
        CommandHandler('start',
                       start,
                       filters=Filters.private
                       & Filters.regex(r'^\/start TOKEN-[a-z0-9]+$'))
    ],
    'states': {
        SET_TOKEN:
        [MessageHandler(Filters.text & ~Filters.regex(r'^/'), set_token)]
    },
    'fallbacks': [CommandHandler('cancel', cancel)]
}
