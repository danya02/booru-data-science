import json
import common
import random
import time

session = common.get_session()
conn = common.get_post_metadata_db()
kvconn = common.get_valkey_conn()

def peek_queue():
    # get an arbitrary post ID from the queue
    post_id = kvconn.srandmember('post_queue')
    return int(post_id)

def dequeue(post_ids):
    print('dequeueing', post_ids)
    kvconn.srem('post_queue', *post_ids)
    

def download_posts_metadata(post_id):
    response = session.get(f'https://danbooru.donmai.us/posts.json', params={'page': f'a{post_id-1}', 'limit': 200})
    response.raise_for_status()
    entries = response.json()
    print('Downloaded', len(entries), 'starting from', post_id)
    entry_params = [(entry['id'], json.dumps(entry), int(time.time()), json.dumps(entry), int(time.time())) for entry in entries]
    conn.executemany('INSERT INTO posts_json (id, json, fetched_at_unix) VALUES (?, ?, ?) ON CONFLICT DO UPDATE SET json = ?, fetched_at_unix = ?', entry_params)
    
    dequeue([entry['id'] for entry in entries])
    conn.commit()

while 1:
    post_id = peek_queue()
    download_posts_metadata(post_id)
    print("Remaining queued posts:", kvconn.scard('post_queue'))
    time.sleep(0.5)
