import requests
import json
import os

URL = 'https://api.telegram.org/bot{token}/{method}'


class TelegramChannel(object):
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def _get_url(self, method):
        return URL.format(
            token=self.token,
            method=method
        )

    def _notify(self, method, data, files=None):
        data.update(chat_id=self.chat_id)
        return json.loads(requests.post(
            self._get_url(method),
            data=data,
            files=files
        ).content)

    def notify_text(self, text='', link=None):
        if link is not None:
            text += u'\n' + link
        text = text.strip()
        return self._notify(
            'sendMessage',
            data=dict(text=text)
        )

    def notify_image(self, photo, caption):
        return self._notify(
            'sendPhoto',
            dict(caption=caption),
            files={'photo': (
                os.path.basename(photo.name), photo.read()
            )}
        )
