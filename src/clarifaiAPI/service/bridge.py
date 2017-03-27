"""
    surabayapy-facebook-bot
    oleh Christoforus Surjoputro
    ~~~~~~~~~
    Modul ini berfungsi sebagai komunikasi dengan API clarifai.

    :license: MIT, see LICENSE for more details.
"""

from clarifai.rest import ClarifaiApp

from config import config

class ClarifaiService():

    def predict(self, url):
        clientId = config.get('clarifai', 'client_id')
        clientSecret = config.get('clarifai', 'client_secret')
        app = ClarifaiApp(clientId, clientSecret)
        model = app.models.get("general-v1.3")
        response = model.predict_by_url(url=url)

        if response['status']['code'] == 10000:
            kata_kunci = ''
            for kata in response['outputs'][0]['data']['concepts']:
                if not kata_kunci:
                    kata_kunci += kata['name']
                else:
                    kata_kunci += ', ' + kata['name']
            replyText = 'Beberapa kata kunci yang kami temukan pada foto anda adalah: {}'.format(kata_kunci)
        else:
            replyText = 'Maaf, gambar yang anda berikan tidak dapat kami deteksi.'
        return replyText
