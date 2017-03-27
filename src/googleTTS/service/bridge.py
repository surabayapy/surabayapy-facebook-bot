"""
    surabayapy-facebook-bot
    oleh Christoforus Surjoputro
    ~~~~~~~~~
    Modul ini berfungsi untuk menggunakan TTS dari google translate.

    :license: MIT, see LICENSE for more details.
"""

from tempfile import TemporaryFile
import re

from wheezy.core.httpclient import HTTPClient
from gtts_token.gtts_token import Token

from config import config


class GoogleTTSService():

    def _optimizingText(self, string, max_chars):
        ''' Optimizing text by spliting text to send by last spacebar before
            max character allowed.
        '''
        if len(string) > max_chars:
            idx = string.rfind(' ', 0, max_chars)
            return [string[:idx]] + self._optimizingText(string[idx:], max_chars)
        else:
            return [string]
    
    def _tokenizationAndOptimation(self, text, max_chars):
        ''' Tokenize the text by some punctuation and return the optimal text. '''
        punc = "¡!()[]¿?.,;:—«»\n"
        punc_list = [re.escape(c) for c in punc]
        pattern = '|'.join(punc_list)
        parts = re.split(pattern, text)

        optimal_text = []
        for string in parts:
            optimal_text += self._optimizingText(string, max_chars)
        return optimal_text
    
    def _getTheSpeech(self, language, google_translate_link, optimal_text, token):
        ''' Getting the speech from google translate machine. '''
        tempfile = TemporaryFile()
        client = HTTPClient(google_translate_link)
        path = '/translate_tts'
        headers = {
            "Referer" : "http://translate.google.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
        }

        for idx, part in enumerate(optimal_text):
            query = {
                'ie' : 'UTF-8',
                'q' : part,
                'tl' : language,
                'total' : len(optimal_text),
                'idx' : idx,
                'client' : 'tw-ob',
                'textlen' : len(part),
                'tk' : token.calculate_token(part)
            }

            if 200 != client.get(path, params=query, headers=headers):
                print('Error callUserProfileAPI: {}'.format(client.headers))
                tempfile.close()
                return None
            tempfile.write(client.body)
        return tempfile
    
    def convert(self, text):
        ''' Interface to convert from text to speech. '''
        google_translate_link = config.get('googleTTS', 'google_translate_link')
        max_chars = int(config.get('googleTTS', 'max_chars'))
        language = config.get('googleTTS', 'language')
        
        if len(text) > max_chars:
            optimal_text = self._tokenizationAndOptimation(text, max_chars)
        else:
            optimal_text = [text]
        
        optimal_text = [x.replace('\n', '').strip() for x in optimal_text]
        optimal_text = [x for x in optimal_text if len(x) > 0]

        token = Token()
        speech_file = self._getTheSpeech(language, google_translate_link, optimal_text, token)
        speech_file.seek(0)
        speech = speech_file.read()
        speech_file.close()

        if speech:
            return speech
        else:
            return 'Maaf, terjadi kesalahaan saat merubah text ke suara. Silahkan coba kembali.'
