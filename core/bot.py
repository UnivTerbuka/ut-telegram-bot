import logging
import os
from queue import Queue

import cherrypy
from telegram import Bot, Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher, Defaults

from .handlers import Handlers


def error(error):
    cherrypy.log("Error occurred - {}".format(error))


class SimpleWebsite(object):
    @cherrypy.expose
    def index(self):
        return """<H1>Welcome!</H1>"""


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
        self.bot = Bot(self.TOKEN, defaults=self.defaults)
        self.update_queue = Queue()
        # Register handlers
        self.dp = Dispatcher(self.bot, self.update_queue, use_context=True)
        self.dp.add_error_handler(error)
        self.handlers = Handlers()
        self.handlers.register(self.dp)
        if NAME:
            try:
                self.bot.setWebhook(
                    "https://{}.herokuapp.com/{}".format(self.NAME, self.TOKEN))
            except:
                raise RuntimeError("Failed to set the webhook")
        else:
            self.updater = Updater(
                TOKEN, bot=self.bot, dispatcher=True, use_context=True, defaults=self.defaults
            )

    @cherrypy.tools.json_in()
    def POST(self, *args, **kwargs):
        update = cherrypy.request.json
        update = Update.de_json(update, self.bot)
        self.dp.process_update(update)

    def polling(self):
        self.updater.start_polling()
