import logging
import os
from queue import Queue

import cherrypy
from telegram import Bot, Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher, Defaults

from .handlers import Handlers, error_callback

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class SimpleWebsite(object):
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect('https://t.me/UniversitasTerbukaBot')


class UniversitasTerbukaBot(object):
    exposed = True
    updater: Updater = None

    def __init__(self, TOKEN: str, NAME: str = None):
        super(UniversitasTerbukaBot, self).__init__()
        self._updater: Updater = None
        self.TOKEN = TOKEN
        self.NAME = NAME
        self.defaults = Defaults(
            parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )
        # Register handlers
        self.dp: Dispatcher = None
        self.handlers = Handlers()
        if NAME:
            self.bot = Bot(self.TOKEN, defaults=self.defaults)
            self.update_queue = Queue()
            self.dp = Dispatcher(self.bot, self.update_queue, use_context=True)
            try:
                self.bot.setWebhook(
                    "https://{}.herokuapp.com/{}".format(self.NAME, self.TOKEN))
            except:
                raise RuntimeError("Failed to set the webhook")
        else:
            self.updater = Updater(
                TOKEN, use_context=True, defaults=self.defaults
            )
            self.dp = self.updater.dispatcher
        self.dp.add_error_handler(error_callback)
        self.handlers.register(self.dp)

    @cherrypy.tools.json_in()
    def POST(self, *args, **kwargs):
        update = cherrypy.request.json
        update = Update.de_json(update, self.bot)
        self.dp.process_update(update)

    def polling(self):
        self.updater.start_polling()
