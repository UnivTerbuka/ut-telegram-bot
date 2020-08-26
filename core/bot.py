import os
from flask import Blueprint, request
from telegram import Bot, Update, ParseMode
from telegram.ext import Updater, Dispatcher, Defaults, messagequeue
from telegram.utils.request import Request

NAME = os.environ.get('NAME')
TOKEN = os.environ.get('TOKEN')


class QueueBot(Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''
    def __init__(self, is_queued_def=True, mqueue=None, **kwargs):
        super(QueueBot, self).__init__(**kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or messagequeue.MessageQueue(
            all_burst_limit=3, all_time_limit_ms=3000)

    def stop(self):
        try:
            self._msg_queue.stop()
        except:  # NOQA
            pass

    @messagequeue.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(QueueBot, self).send_message(*args, **kwargs)


class QueueUpdater(Updater):
    def __init__(self, bot: QueueBot, *args, **kwargs):
        super().__init__(bot=bot, *args, **kwargs)

    def signal_handler(self, signum, frame):
        super().signal_handler(signum, frame)

        self.bot.stop()


class UniversitasTerbukaBot(object):
    def __init__(self, TOKEN: str = TOKEN, NAME: str = NAME):
        super(UniversitasTerbukaBot, self).__init__()
        self.TOKEN = TOKEN
        self.NAME = NAME
        self.defaults = Defaults(parse_mode=ParseMode.HTML,
                                 disable_web_page_preview=True)
        # Init bot
        q = messagequeue.MessageQueue(all_burst_limit=3,
                                      all_time_limit_ms=3000)
        request = Request(con_pool_size=8)
        self.bot = QueueBot(token=TOKEN,
                            request=request,
                            mqueue=q,
                            defaults=self.defaults)
        # Register handlers
        self.updater: QueueUpdater = QueueUpdater(self.bot,
                                                  use_context=True,
                                                  defaults=self.defaults)
        # self.updater: Updater = Updater(
        #     TOKEN, use_context=True, defaults=self.defaults
        # )
        self.dp: Dispatcher = self.updater.dispatcher
        from handlers import Handlers, error_callback
        self.dp.add_error_handler(error_callback)
        self.handlers = Handlers()
        self.handlers.register(self.dp)
        self.bot = self.updater.bot
        if NAME:
            self.bot.setWebhook("https://{}.herokuapp.com/{}".format(
                self.NAME, self.TOKEN))

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
