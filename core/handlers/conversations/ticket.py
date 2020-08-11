from telegram import Update, MessageEntity
from telegram.ext import CallbackContext, ConversationHandler, Filters, CommandHandler, MessageHandler
from libs.ticket import Ticket

COMMAND = 'tiket'

GET_TICKET = range(1)


def valid_ticket(ticket: str = ''):
    return len(ticket) == 20 and not ' ' in ticket


def ticket(update: Update, context: CallbackContext):
    msg: str = update.effective_message.text
    noticket = msg.split(' ')[1] if len(msg) == 27 else ''
    if Ticket.is_nomor_valid(noticket):
        ticket_ = Ticket.from_nomor(noticket)
        update.effective_message.reply_text(str(ticket_))
        return -1
    update.effective_message.reply_text(
        'Kirimkan nomor tiket yang akan dicek...'
    )
    return GET_TICKET


def get_ticket(update: Update, context: CallbackContext):
    noticket: str = update.effective_message.text
    noticket = noticket.upper()
    ticket_ = Ticket.from_nomor(noticket)
    update.effective_message.reply_text(str(ticket_))
    return -1


def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(f'/{COMMAND} telah dibatalkan')


TICKET = {
    'entry_points': [CommandHandler(COMMAND, ticket)],
    'states': {
        GET_TICKET: [
            MessageHandler(Filters.text, get_ticket)
        ]
    },
    'fallbacks': [CommandHandler('cancel', cancel)]
}
