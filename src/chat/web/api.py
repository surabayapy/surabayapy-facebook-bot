"""
    surabayapy-facebook-bot
    oleh Christoforus Surjoputro
    ~~~~~~~~~
    Modul ini berfungsi sebagai penerima pesan dari facebook, mengolah pesan
    tersebut, dan mengirimkannya ke pengguna.

    :license: MIT, see LICENSE for more details.
"""

from datetime import timedelta

from wheezy.core.comp import json_dumps

from factory import Factory
from shared.apihandler import APIHandler


class ChatBaseHandler(APIHandler):

    def factory(self):
        return Factory()


class Chat(ChatBaseHandler):

    def persistenData(self):
        return {
            'token': 'EAAD89itXOakBANPpbOD2OnlhGURlDM3OtEExk2YrpbudYZBgD0hLsH6qaUDcXEZCB5WAMM6c3iBgBRoGUigXYyUROZAZC0XqPvEoAZAvBr1DES7IZBm8kZBG365YocxotgQDzcZCd2cjqahs89DTJtgC4ZCJ9huyOJKmPMsGOyHToDAZDZD',
            'messengerLink': 'https://graph.facebook.com'
        }

    def get(self):
        if (self.request.query['hub.mode'][0] == 'subscribe' and
            self.request.query['hub.verify_token'][0] == 'verifikasi-python-id-bot'):
            return self.json_response(int(self.request.query['hub.challenge'][0]))
        else:
            self.errors = 'Validasi gagal. Pastikan token untuk validasi sama.'
            print(self.errors)
            return self.error_response(403)

    def post(self):
        print(self.request.form)
        data = self.request.form
        if data['object'] == 'page':
            for entry in data['entry']:
                for messaging in entry['messaging']:
                    if 'message' in messaging:
                        self.receivedMessage(messaging)
                    else:
                        print("Pesan tidak diketahui")
        response = self.json_response({"status":"OK"})
        response.status_code = 200
        return response

    def receivedMessage(self, messaging):
        ''' Logika untuk membalas diletakkan di sini.

            Cache bisa digunakan dengan menggunakan senderID sebagai kombinasi
            key dengan servis sequential. Mis: '213123-seq': 'data'.
        '''
        senderID = messaging['sender']['id']
        recipientID = messaging['recipient']['id']
        message = messaging['message']

        if 'text' in message:
            replyText = self.stupidReply(senderID, message['text'].lower())
            self.sendTextMessage(senderID, replyText)

    def stupidReply(self, recipientID, messageText):
        list_intro = ['hai', 'halo', 'hi', 'hei']
        list_event = ['event', 'kegiatan']
        replyText = ''
        f = self.factory()
        for intro in list_intro:
            if intro in messageText:
                name = f.chat.callUserProfileAPI(recipientID)
                replyText = 'Halo {}'.format(name)
                break
        for event in list_event:
            if event in messageText:
                replyText = 'surabaya.py sedang ada kegiatan di sub co bersama FacebookDev Circle Surabaya.'
                break
        if not replyText:
            name = f.chat.callUserProfileAPI(recipientID)
            replyText = 'Maaf {}, saya belum memahami apa yang kamu bicarakan.'.format(name)
        return replyText

    def sendTextMessage(self, recipientID, replyText):
        messageData = {
            'recipient': {'id': recipientID},
            'message': {'text': replyText}
        }
        f = self.factory()
        f.chat.callSendAPI(json_dumps(messageData))

