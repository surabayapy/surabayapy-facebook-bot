"""
    surabayapy-facebook-bot
    oleh Christoforus Surjoputro
    ~~~~~~~~~
    Modul yang berfungsi untuk menyimpan segala konfigurasi aplikasi ini.

    :license: MIT, see LICENSE for more details.
"""

import os

try:  # pragma: nocover
    from ConfigParser import ConfigParser
    config = ConfigParser()
except ImportError:  # pragma: nocover
    from configparser import ConfigParser
    config = ConfigParser(strict=False)


config.read(os.getenv('CONFIG', 'etc/development.ini'))

mode = config.get('runtime', 'cache')
if mode == 'memory':
    from wheezy.caching import MemoryCache
    cache = MemoryCache()
elif mode == 'memcached':
    from wheezy.core.pooling import EagerPool
    from wheezy.caching.pylibmc import MemcachedClient
    from wheezy.caching.pylibmc import client_factory
    pool = EagerPool(
        lambda: client_factory(config.get('memcached', 'servers').split(';')),
        size=config.getint('memcached', 'pool-size'))
    cache = MemcachedClient(pool)
else:
    raise NotImplementedError(mode)

options = {}

# HTTPCacheMiddleware
options.update({
    'http_cache': cache
})
