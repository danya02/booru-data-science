import requests

def get_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'requests+pythonbot (+https://github.com/danya02/booru-data-science)'
    })
