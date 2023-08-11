import requests

base_url = 'http://cal-api:3000/api/'
session_key = 'next-auth.session-token'
session = requests.Session()
session.get(base_url + 'auth/session')
r1 = session.post(
    base_url + 'auth/callback/credentials?',
    data={
        'email': 'envy42125@gmail.com',
        'password': 'ab0baNice',
        'csrfToken': session.get(base_url + 'auth/csrf').json()['csrfToken'],
        'callbackUrl': 'https://cal.local.host/',
        'redirect': False,
        'json': True,
    },
    allow_redirects=False,
)
token = r1.cookies.get(session_key)
session = requests.Session()
session.cookies.set(session_key, token)
r2 = session.get(base_url + 'trpc/viewer/me?batch=1&input=%7B%7D')
