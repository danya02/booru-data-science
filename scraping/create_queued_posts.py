import common
import requests

session = common.get_session()
kvconn = common.get_valkey_conn()

# find latest post on Danbooru
response = session.get('https://danbooru.donmai.us/posts.json?limit=1')

post_id = response.json()[0]['id']

print(post_id)

# Add to queue all posts in range from 1 to post_id
for i in range(1, post_id + 1, 1000):
    print(i)
    kvconn.sadd('post_queue', *range(i, min(i+1000, post_id+1)))