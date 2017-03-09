"""
    surabayapy-facebook-bot
    oleh Christoforus Surjoputro
    ~~~~~~~~~
    Modul url utama, berfungsi menghubungkan seluruh url yang ada pada aplikasi.

    :license: MIT, see LICENSE for more details.
"""

from wheezy.routing import url

from chat.web.urls import chat_urls


locale_urls = chat_urls
all_urls = locale_urls
