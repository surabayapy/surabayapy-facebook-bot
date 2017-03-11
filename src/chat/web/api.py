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

    def get(self):
        if (self.request.query['hub.mode'][0] == 'subscribe' and
            self.request.query['hub.verify_token'][0] == 'verifikasi-python-id-bot'):
            return self.json_response(int(self.request.query['hub.challenge'][0]))
        else:
            self.errors = 'Validasi gagal. Pastikan token untuk validasi sama.'
            return self.error_response(403)

    def post(self):
        #print(self.request.form)
        data = self.request.form
        if data['object'] == 'page':
            for entry in data['entry']:
                for messaging in entry['messaging']:
                    if 'message' in messaging:
                        self.receivedMessage(messaging)
        response = self.json_response({"status":"OK"})
        response.status_code = 200
        return response

    def receivedMessage(self, messaging):
        senderID = messaging['sender']['id']
        recipientID = messaging['recipient']['id']
        message = messaging['message']

        if 'text' in message:
            f = self.factory()
            replyText = f.stupidreply.stupidReply(senderID, message['text'].lower())
            self.sendTextMessage(senderID, replyText)

    def sendTextMessage(self, recipientID, replyText):
        messageData = {
            'recipient': {'id': recipientID},
            'message': {'text': replyText}
        }
        f = self.factory()
        f.chat.callSendAPI(json_dumps(messageData))

