from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext
from core.utils import action
from config import CALLBACK_SEPARATOR


@action.typing
def close(update: Update, context: CallbackContext):
    callback_query: CallbackQuery = update.callback_query
    callback_query.answer()
    callback_query.edit_message_text('Terimakasih. :D')
    return -1