"""
    surabayapy-facebook-bot
    oleh Christoforus Surjoputro
    ~~~~~~~~~
    Modul ini berfungsi sebagai pemroses balasan dari inputan pengguna.

    :license: MIT, see LICENSE for more details.
"""


class StupidReplyService():

    def __init__(self, chatService, googleTTSService):
        self.chatService = chatService
        self.googleTTSService = googleTTSService

    def stupidReply(self, recipientID, messageText):
        ''' Rule based reply. Reply generate by checking keyword in text. '''
        list_intro = ['hai', 'halo', 'hi', 'hei']
        list_event = ['event', 'kegiatan']
        list_TTS = ['ucapkan', 'katakan']
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
        for tts in list_TTS:
            if tts in messageText:
                replyText = self.googleTTSService.convert(messageText.replace(tts + ' ', ''))
                break
        if not replyText:
            name = self.chatService.callUserProfileAPI(recipientID)
            replyText = 'Maaf {}, saya belum memahami apa yang kamu bicarakan.'.format(name or 'teman')
        return replyText

