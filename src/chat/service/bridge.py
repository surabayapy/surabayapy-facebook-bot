"""
    surabayapy-facebook-bot
    oleh Christoforus Surjoputro
    ~~~~~~~~~
    Modul ini berisi servis-servis yang tersedia untuk modul chat messenger.

    :license: MIT, see LICENSE for more details.
"""

from datetime import timedelta
from mimetypes import guess_type

from wheezy.caching.patterns import Cached
from wheezy.core.comp import json_dumps
from wheezy.core.comp import json_loads
from wheezy.core.httpclient import HTTPClient

from config import cache
from config import config

cached = Cached(cache, time=timedelta(minutes=15))


class ChatService():

    def callUserProfileAPI(self, userID):
        ''' Getting user's first name by user ID. '''
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
        ''' Handling sending text message to messenger. '''
        token = config.get('chatmodule', 'token')
        messenger_link = config.get('chatmodule', 'messenger_link')

        MESSENGER_PATH = '/v2.6/me/messages?access_token={}'.format(token)
        CONTENT_TYPE = 'application/json'

        client = HTTPClient(messenger_link)
        if 200 != client.post(MESSENGER_PATH, body=messageData, content_type=CONTENT_TYPE):
            print('Error callSendAPI: {}'.format(client.headers))
            return None
        return True

    def _encode_multipart_formdata(self, messageData):
        ''' Preparing the body of html to send attachment message as multipart
            form data. Convert mesasge data and atachment to binary.
        '''
        BOUNDARY = b'----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = b'\r\n'
        body = b''
        for key in messageData:
            body += b'--' + BOUNDARY + CRLF
            if not isinstance(messageData[key], bytes):
                body += b'Content-Disposition: form-data; name="%s"' % key.encode('utf-8')
                body += CRLF + CRLF
                if isinstance(messageData[key], str):
                    body += messageData[key].encode('utf-8')
                    body += CRLF
                else:
                    body += json_dumps(messageData[key]).encode('utf-8')
                    body += CRLF
            else:
                body += b'Content-Disposition: form-data; name="%s"; filename="%s"' % (key.encode('utf-8'), b'speech.mp3')
                body += CRLF
                body += b'Content-Type: %s' % b'audio/mp3'
                body += CRLF
                body += CRLF
                body += messageData[key]
                body += CRLF
        body += b'--' + BOUNDARY + b'--'
        body += CRLF
        body += CRLF
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY.decode('utf-8')
        return content_type, body

    def callSendFileAPI(self, messageData):
        ''' Handling sending attachment message to messenger. '''
        CONTENT_TYPE, body = self._encode_multipart_formdata(messageData)
        token = config.get('chatmodule', 'token')
        messenger_link = config.get('chatmodule', 'messenger_link')

        MESSENGER_PATH = '/v2.6/me/messages?access_token={}'.format(token)

        client = HTTPClient(messenger_link)
        if 200 != client.post(MESSENGER_PATH, body=body, content_type=CONTENT_TYPE):
            print('Error callSendAPI: {}'.format(client.headers))
            return None
        return True
