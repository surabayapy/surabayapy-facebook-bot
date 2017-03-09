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

from config import config
from chat.service.bridge import MembershipService


class Factory():

    @attribute
    def chat(self):
        return MembershipService()

