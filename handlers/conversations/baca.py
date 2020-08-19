from dacite import from_dict
from logging import getLogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatAction
from telegram.ext import CallbackContext, ConversationHandler, Filters, CommandHandler, MessageHandler
from core.utils import action
from libs.rbv import Buku
from libs.utils import format_html

COMMAND = 'baca'
GET_BOOK = range(1)
logger = getLogger(__name__)


def delete_data(data: dict):
    if data and COMMAND in data:
        del data[COMMAND]


def set_data(data: dict, value):
    if data:
        data[COMMAND] = value


def get_data(data: dict):
    return data.get(COMMAND) if data else None


def answer(update: Update, code: str, context: CallbackContext = None):
    user_data: dict = context.user_data if context else {}
    message: Message = get_data(user_data)
    if not message:
        message: Message = update.effective_message.reply_text(
            'Mencari buku...')
        set_data(user_data, message)
    data = {
        'id': code
    }
    try:
        buku: Buku = from_dict(Buku, data)
        if buku:
            context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_PHOTO
            )
            message: Message = message.edit_text(
                buku.text,
                reply_markup=buku.reply_markup
            )
        else:
            message.edit_text(
                f'Buku {code} tidak ditemukan di rbv\n'
            )
    except Exception as E:
        logger.exception(E)
        message: Message = message.edit_text(
            'Tidak dapat menghubungi rbv.'
        )
    finally:
        delete_data(user_data)
    return -1


@action.typing
def baca(update: Update, context: CallbackContext):
    msg: str = update.effective_message.text
    if len(msg) > 5:
        answer(update, msg.lstrip('/baca '), context)
        return -1
    update.effective_message.reply_text(
        'Kode buku yang aka dibaca?\n'
        '<i>Maaf jika lambat..</i>\n'
        '/cancel untuk membatalkan'
    )
    return GET_BOOK


@action.typing
def get_buku(update: Update, context: CallbackContext):
    code: str = update.effective_message.text
    answer(update, code, context)
    return -1


def start(update: Update, context: CallbackContext):
    text: str = update.effective_message.text
    # /start BACA-code
    code: str = text.split('-')[-1]
    answer(update, code, context)
    return -1


@action.typing
def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(f'/{COMMAND} telah dibatalkan')
    delete_data(context.user_data)
    return -1


BACA = {
    'name': COMMAND,
    'entry_points': [
        CommandHandler(COMMAND,
                       baca),
        CommandHandler('start',
                       start,
                       filters=Filters.regex(r'/start READ-[A-Z]{4}\d+$')),
    ],
    'states': {
        GET_BOOK: [
            MessageHandler(Filters.text & Filters.regex(
                r'^[A-Z]{4}\d+$'), get_buku)
        ]
    },
    'fallbacks': [CommandHandler('cancel', cancel)],
    'conversation_timeout': 180,
}
