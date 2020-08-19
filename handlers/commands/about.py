from telegram import Update, Bot
from telegram.ext import CallbackContext
from core.utils import action

MESSAGE = '''
Developer : @hexatester - Habib Rohman
Source code : https://github.com/hexatester/ut-telegram-bot

Bot ini dikembangan dengan menggunakan <a href="https://www.python.org/">Bahasa Pemrograman Python </a>.

Dan menggunakan library :
* <a href="https://python-telegram-bot.org/">python-telegram-bot</a>
* <a href="https://www.crummy.com/software/BeautifulSoup/">beautifulsoup4</a>
* <a href="https://2.python-requests.org/en/master/">requests</a>
* <a href="https://github.com/hexatester/ut-telegram-bot/blob/master/requirements.txt">dll.</a>
'''


@action.typing
def about(update: Update, context: CallbackContext):
    update.effective_message.reply_text(MESSAGE)
