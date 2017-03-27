"""
    surabayapy-facebook-bot
    oleh Christoforus Surjoputro
    ~~~~~~~~~
    Modul ini berfungsi sebagai daftar dari service-service yang ada
    pada aplikasi surabayapy-facebook-bot. Setelah membuat fitur baru,
    jangan lupa menambahkan servisnya di sini, sehingga dapat diakses
    modul lainnya.

    :license: MIT, see LICENSE for more details.
"""

from wheezy.core.descriptors import attribute

from chat.service.bridge import ChatService
from clarifaiAPI.service.bridge import ClarifaiService
from googleTTS.service.bridge import GoogleTTSService
from stupidreply.service.bridge import StupidReplyService


class Factory():

    @attribute
    def chat(self):
        return ChatService()

    @attribute
    def clarifai(self):
        return ClarifaiService()

    @attribute
    def googletts(self):
        return GoogleTTSService()

    @attribute
    def stupidreply(self):
        return StupidReplyService(self.chat, self.googletts)

