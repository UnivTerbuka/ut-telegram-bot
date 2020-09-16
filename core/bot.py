from telegram import Update, ParseMode
from telegram.ext import Updater, Dispatcher, Defaults
from threading import Thread
from config import NAME, TOKEN, PERSISTENCE


class UniversitasTerbukaBot(object):
    def __init__(self, TOKEN: str = TOKEN, NAME: str = NAME):
        super(UniversitasTerbukaBot, self).__init__()
        self.TOKEN = TOKEN
        self.NAME = NAME
        self.defaults = Defaults(parse_mode=ParseMode.HTML,
                                 disable_web_page_preview=True)
        self.updater: Updater = Updater(TOKEN,
                                        use_context=True,
                                        persistence=PERSISTENCE,
                                        defaults=self.defaults)
        self.dp: Dispatcher = self.updater.dispatcher
        from handlers import Handlers, error_callback
        self.dp.add_error_handler(error_callback)
        self.handlers = Handlers()
        self.handlers.register(self.dp)
        self.bot = self.updater.bot
        self.update_queue = self.updater.update_queue
        if NAME:
            self.bot.setWebhook("https://{}.herokuapp.com/{}".format(
                self.NAME, self.TOKEN))

    def start_dispatcher_thread(self):
        self.thread = Thread(target=self.dp.start, name='dispatcher')
        self.thread.start()

    def process_update(self, update):
        update = Update.de_json(update, self.bot)
        self.update_queue.put(update)

    def polling(self):
        self.updater.start_polling(clean=True)
