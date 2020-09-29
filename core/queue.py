import functools
import inspect
from telegram import Bot
from telegram.ext import MessageQueue, Updater
from telegram.ext.messagequeue import queuedmessage
from telegram.utils.helpers import DEFAULT_NONE


class CoreQueueBot(Bot):
    def __new__(cls, *args, **kwargs):
        # Get default values from kwargs
        defaults = kwargs.get('defaults')

        # Make an instance of the class
        instance = super().__new__(cls)

        if not defaults:
            return instance

        # For each method ...
        for method_name, method in inspect.getmembers(instance, predicate=inspect.ismethod):
            # ... get kwargs
            argspec = inspect.getfullargspec(inspect.unwrap(method))
            kwarg_names = argspec.args[-len(argspec.defaults or []):]
            # ... check if Defaults has a attribute that matches the kwarg name
            needs_default = [
                kwarg_name for kwarg_name in kwarg_names if hasattr(defaults, kwarg_name)
            ]
            # ... make a dict of kwarg name and the default value
            default_kwargs = {
                kwarg_name: getattr(defaults, kwarg_name) for kwarg_name in needs_default if (
                    getattr(defaults, kwarg_name) is not DEFAULT_NONE
                )
            }
            # ... apply the defaults using a partial
            if default_kwargs:
                setattr(instance, method_name, functools.partial(method, **default_kwargs))

        return instance

    def __init__(self, *args, **kwargs):
        super(CoreQueueBot, self).__init__(*args, **kwargs)
        self._is_messages_queued_default = True
        self._msg_queue = MessageQueue()

    def stop(self):
        try:
            self._msg_queue.stop()
        except Exception:
            pass

    @queuedmessage
    def send_message(self,
                     chat_id,
                     text,
                     parse_mode=None,
                     disable_web_page_preview=None,
                     disable_notification=False,
                     reply_to_message_id=None,
                     reply_markup=None,
                     timeout=None,
                     **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup` OPTIONAL arguments'''
        # self.add_defaults(kwargs)
        return super(CoreQueueBot, self).send_message(
            chat_id,
            text,
            parse_mode,
            disable_web_page_preview,
            disable_notification,
            reply_to_message_id,
            reply_markup,
            timeout,
            **kwargs
        )


class CoreUpdater(Updater):
    def __init__(self, bot: CoreQueueBot, *args, **kwargs):
        super(CoreUpdater, self).__init__(bot=bot, *args, **kwargs)

    def signal_handler(self, signum, frame):
        super().signal_handler(signum, frame)
        self.bot.stop()
