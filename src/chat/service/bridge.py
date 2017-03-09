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

cached = Cached(cache, time=timedelta(minutes=15))


class MembershipService():

    def persistenData(self):
        return {
            'token': 'EAAD89itXOakBANPpbOD2OnlhGURlDM3OtEExk2YrpbudYZBgD0hLsH6qaUDcXEZCB5WAMM6c3iBgBRoGUigXYyUROZAZC0XqPvEoAZAvBr1DES7IZBm8kZBG365YocxotgQDzcZCd2cjqahs89DTJtgC4ZCJ9huyOJKmPMsGOyHToDAZDZD',
            'messengerLink': 'https://graph.facebook.com'
        }

    def callUserProfileAPI(self, userID):
        persistenData = self.persistenData()
        MESSENGER_PATH = '/v2.6/{}?fields=first_name&access_token={}'.format(userID, persistenData['token'])
        CONTENT_TYPE = 'application/json'

        client = HTTPClient(persistenData['messengerLink'])
        if 200 != client.get(MESSENGER_PATH):
            return None
        return cached.get_or_set(userID, lambda: json_loads(client.content)['first_name'])

    def callSendAPI(self, messageData):
        persistenData = self.persistenData()
        MESSENGER_PATH = '/v2.6/me/messages?access_token={}'.format(persistenData['token'])
        CONTENT_TYPE = 'application/json'

        client = HTTPClient(persistenData['messengerLink'])
        if 200 != client.post(MESSENGER_PATH, body=messageData, content_type=CONTENT_TYPE):
            print('Gagal membalas')
            print('Pesan error: {}'.format(client.headers))
            return None
        print('Berhasil membalas')
        return True
