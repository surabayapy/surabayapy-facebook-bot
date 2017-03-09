"""
    surabayapy-facebook-bot-migrate.py
    oleh Christoforus Surjoputro
    ~~~~~~~~~
    migrate.py digunakan untuk membuat database pada postgresql.

    :license: MIT, see LICENSE for more details.
"""

import os
import psycopg2
import psycopg2.extras
#import urlparse
from urllib import parse as urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor()

cur.execute("CREATE TABLE main_data (name text PRIMARY KEY, data jsonb);")
cur.execute("INSERT INTO main_data (name, data) VALUES (%s, %s)", ("detail", psycopg2.extras.Json({})))

conn.commit()

cur.close()
conn.close()