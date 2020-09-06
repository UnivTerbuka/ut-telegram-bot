from telegram import Update
from telegram.ext import CallbackContext
from core.utils import action
from libs.utils import format_html

MESSAGE = '''
Developers :
Habib Rohman - @hexatester - {linkedin}

Source code : https://github.com/UnivTerbuka/ut-telegram-bot

Bot ini dikembangan dengan menggunakan {python}.

Dan menggunakan library :
* <a href="https://python-telegram-bot.org/">python-telegram-bot</a>
* <a href="https://www.crummy.com/software/BeautifulSoup/">beautifulsoup4</a>
* <a href="https://2.python-requests.org/en/master/">requests</a>
* {dll}
'''.format(linkedin=format_html.href(
    "LinkedIn", "https://sl.ut.ac.id/hexatester-linkedin"),
           python=format_html.href("Bahasa Pemrograman Python",
                                   "https://sl.ut.ac.id/python"),
           dll=format_html.href("dll", "https://sl.ut.ac.id/ut-bot-req"))


@action.typing
def about(update: Update, context: CallbackContext):
    update.effective_message.reply_text(MESSAGE)
