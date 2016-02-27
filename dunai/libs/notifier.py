import gevent
import telegram
from django.conf import settings
# import threading


class Notifier(object):
    def __init__(self):
        raise Exception('Cannot be instantiated.')

    @classmethod
    def notify(cls, *args, **kwargs):
        if settings.DEBUG:
            cls._notify(*args, **kwargs)
        else:
            gevent.spawn(cls._notify, *args, **kwargs)

    @classmethod
    def _notify(cls, message, parse_mode=None, tags='web'):
        if isinstance(message, unicode):
            message = message.encode('utf-8')

        # if tags:
        message = ' '.join(['#' + tag for tag in tags.split(' ')]) + ' ' + message

        if settings.DEBUG:
            print '[DEBUG] Notification: "{}"'.format(message)
        else:
            bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
            bot.sendMessage(str(settings.TELEGRAM_GROUP_ID), message, parse_mode=parse_mode)
        # for update in bot.getUpdates(offset=0, timeout=10):
        #     print update
