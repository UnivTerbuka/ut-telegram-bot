import os
from flask import Blueprint, request
from telegram import Bot, Update, ParseMode
from telegram.ext import Updater,  Dispatcher, Defaults, messagequeue
from telegram.utils.request import Request
from handlers import Handlers, error_callback


NAME = os.environ.get('NAME')
TOKEN = os.environ.get('TOKEN')


class MQBot(Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''

    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or messagequeue.MessageQueue(
            all_burst_limit=3, all_time_limit_ms=3000
        )

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @messagequeue.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_message(*args, **kwargs)


class UniversitasTerbukaBot(object):
    def __init__(self, TOKEN: str = TOKEN, NAME: str = NAME):
        super(UniversitasTerbukaBot, self).__init__()
        self.TOKEN = TOKEN
        self.NAME = NAME
        self.defaults = Defaults(
            parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )
        # Init bot
        # q = messagequeue.MessageQueue(
        #     all_burst_limit=3, all_time_limit_ms=3000
        # )
        # request = Request(con_pool_size=8)
        # self.bot = MQBot(TOKEN, defaults=self.defaults, request=request, mqueue=q)
        # Register handlers
        self.updater: Updater = Updater(
            TOKEN, use_context=True, defaults=self.defaults
        )
        self.dp: Dispatcher = self.updater.dispatcher
        self.dp.add_error_handler(error_callback)
        self.handlers = Handlers()
        self.handlers.register(self.dp)
        self.bot = self.updater.bot
        if NAME:
            try:
                self.bot.setWebhook(
                    "https://{}.herokuapp.com/{}".format(self.NAME, self.TOKEN))
            except:
                raise RuntimeError("Failed to set the webhook")

    def process_update(self, update):
        update = Update.de_json(update, self.bot)
        self.dp.process_update(update)

    def polling(self):
        self.updater.start_polling()


def get_blueprint(token, name):
    bp = Blueprint('bot', __name__)
    bot = UniversitasTerbukaBot(token, name)

    @bp.route(f"/{bot.TOKEN}", methods=['POST'])
    def webhook():
        update = request.get_json()
        bot.process_update(update)
        return ''
    return bp