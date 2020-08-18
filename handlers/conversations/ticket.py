from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, Filters, CommandHandler, MessageHandler
from libs.ticket import Ticket

COMMAND = 'tiket'

GET_TICKET = range(1)


def answer(update: Update, tiket: Ticket):
    update.effective_message.reply_text(
        str(tiket), reply_markup=tiket.reply_markup)


def ticket(update: Update, context: CallbackContext):
    msg: str = update.effective_message.text
    noticket = msg.split(' ')[1] if len(msg) == 27 else ''
    if len(msg) > 6 and Ticket.is_nomor_valid(noticket):
        ticket_ = Ticket.from_nomor(noticket)
        answer(update, ticket_)
        return -1
    update.effective_message.reply_text(
        'Kirimkan nomor tiket yang akan dicek...'
        '/cancel untuk membatalkan'
    )
    return GET_TICKET


def get_ticket(update: Update, context: CallbackContext):
    noticket: str = update.effective_message.text
    noticket = noticket.upper()
    ticket_ = Ticket.from_nomor(noticket)
    answer(update, ticket_)
    return -1


def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(f'/{COMMAND} telah dibatalkan')


TICKET = {
    'name': COMMAND,
    'entry_points': [CommandHandler(COMMAND, ticket)],
    'states': {
        GET_TICKET: [
            MessageHandler(Filters.text, get_ticket)
        ]
    },
    'fallbacks': [CommandHandler('cancel', cancel)],
    'conversation_timeout': 180,
}
