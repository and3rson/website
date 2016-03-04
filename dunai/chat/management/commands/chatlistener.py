# coding=utf-8
from dunai.chat import helpers
import gevent
from django.conf import settings
from django.core.management import BaseCommand
from telegram import Bot
import re
import json

CLIENT_INBOX = '{chat_id}:new'
ADMIN_INBOX = 'admin:new'


def green(fn):
    def wrapper(*args, **kwargs):
        return gevent.spawn(fn, *args, **kwargs)
    return wrapper


class Command(BaseCommand):
    bot = None
    initial = True
    id = 0
    terminated = False

    def handle(self, *args, **options):
        self.bot = Bot(token=settings.TELEGRAM_TOKEN)
        self.initial = True
        self.id = 0
        self.terminated = False

        gevent.joinall([self.listen_from_admin(), self.listen_from_client()])

    @green
    def listen_from_admin(self):
        while not self.terminated:
            for update in self.bot.getUpdates(timeout=0 if self.initial else 5, offset=self.id):
                if not self.initial:
                    self.handle_update(update)
                self.id = max(self.id, update.update_id + 1)
            self.initial = False

    def handle_update(self, update):
        if update.message.chat.id != settings.TELEGRAM_GROUP_ID:
            self.bot.sendMessage(chat_id=update.message.chat.id, text=u"Sorry, I dont know you :(")
            return

        if update.message.reply_to_message:
            original_message = update.message.reply_to_message.text

            tags = re.findall('#([a-z]+)([0-9]+)', original_message)

            if not tags:
                self.bot.sendMessage(chat_id=update.message.chat.id, text=u'В мене просто немає слів :)')
                return

            key, value = tags[0]
            value = int(value)
            # msg = re.sub('\s*#[a-z]+[0-9]+\s*', '', update.message.text).strip()
            # print 'Reply for', key, value, original_message
            # print update.message.text

            helpers.publish(CLIENT_INBOX.format(chat_id=value), update.message.text)

    @green
    def listen_from_client(self):
        while not self.terminated:
            data = helpers.expect(ADMIN_INBOX)
            if data:
                key, value = data
                value = json.loads(value)
                self.bot.sendMessage(chat_id=settings.TELEGRAM_GROUP_ID, text='{} #chat{}: {}'.format(
                    value['chat_data']['username'],
                    value['chat_data']['id'],
                    value['message']
                ))
        # for message in data:
