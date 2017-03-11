"""
    surabayapy-facebook-bot
    oleh Christoforus Surjoputro
    ~~~~~~~~~
    Modul ini berfungsi servis-servis yang tersedia untuk modul chat.

    :license: MIT, see LICENSE for more details.
"""

from datetime import timedelta

from wheezy.caching.patterns import Cached
from wheezy.core.comp import json_loads
from wheezy.core.httpclient import HTTPClient

from config import cache
from config import config

cached = Cached(cache, time=timedelta(minutes=15))


class ChatService():

    def callUserProfileAPI(self, userID):
        first_name = cached.get(userID)
        if not first_name:
            token = config.get('chatmodule', 'token')
            messenger_link = config.get('chatmodule', 'messenger_link')

            MESSENGER_PATH = '/v2.6/{}?fields=first_name&access_token={}'.format(userID, token)
            CONTENT_TYPE = 'application/json'

            client = HTTPClient(messenger_link)
            if 200 != client.get(MESSENGER_PATH):
                print('Error callUserProfileAPI: {}'.format(client.headers))
                return None
            first_name = json_loads(client.content)['first_name']
            cached.set(userID, first_name)
        return first_name

    def callSendAPI(self, messageData):
        token = config.get('chatmodule', 'token')
        messenger_link = config.get('chatmodule', 'messenger_link')

        MESSENGER_PATH = '/v2.6/me/messages?access_token={}'.format(token)
        CONTENT_TYPE = 'application/json'

        client = HTTPClient(messenger_link)
        if 200 != client.post(MESSENGER_PATH, body=messageData, content_type=CONTENT_TYPE):
            print('Error callSendAPI: {}'.format(client.headers))
            return None
        return True
