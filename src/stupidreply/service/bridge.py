"""
    surabayapy-facebook-bot
    oleh Christoforus Surjoputro
    ~~~~~~~~~
    Modul ini berfungsi servis-servis yang tersedia untuk modul chat.

    :license: MIT, see LICENSE for more details.
"""


class StupidReplyService():

    def __init__(self, chatService):
        self.chatService = chatService

    def stupidReply(self, recipientID, messageText):
        list_intro = ['hai', 'halo', 'hi', 'hei']
        list_event = ['event', 'kegiatan']
        replyText = ''
        for intro in list_intro:
            if intro in messageText:
                name = self.chatService.callUserProfileAPI(recipientID)
                replyText = 'Halo {}'.format(name or 'teman')
                break
        for event in list_event:
            if event in messageText:
                replyText = 'surabaya.py sedang ada kegiatan di sub co bersama FacebookDev Circle Surabaya.'
                break
        if not replyText:
            name = self.chatService.callUserProfileAPI(recipientID)
            replyText = 'Maaf {}, saya belum memahami apa yang kamu bicarakan.'.format(name or 'teman')
        return replyText

