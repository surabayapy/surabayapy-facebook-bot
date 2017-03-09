"""
    surabayapy-facebook-bot
    oleh Christoforus Surjoputro
    ~~~~~~~~~
    Modul url untuk meyimpan handler apa saja yang terdapat pada modul chat

    :license: MIT, see LICENSE for more details.
"""

from wheezy.routing import url

from chat.web.api import Chat


chat_urls = [
    url('chat', Chat, name='chat')
]
