from . import COMMAND


def cancel(update, context):
    update.effective_message.reply_text(f'/{COMMAND} telah dibatalkan')
    return -1
