import requests
import sqlite3
import valkey

def get_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'requests+pythonbot (+https://github.com/danya02/booru-data-science)'
    })
    return session

def get_post_metadata_db():
    conn = sqlite3.connect('post-metadata.sqlite3')
    conn.execute('CREATE TABLE IF NOT EXISTS posts_json (id INTEGER PRIMARY KEY, json TEXT NOT NULL, fetched_at_unix INTEGER NOT NULL)')
    return conn

def get_valkey_conn():
    return valkey.Valkey(host='localhost', port=6379, db=0)