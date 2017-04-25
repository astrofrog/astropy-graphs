import json
import time
from six.moves import input

import requests

session = requests.Session()

username = input('Username: ')

try:
    import getpass
    import keyring
    pw = keyring.get_password('api.github.com', username)
    if pw is None:
        pw = getpass.getpass(prompt='Password for api.github.com: ')
        keyring.set_password('api.github.com', username, pw)
except ImportError:
    password = input('Password (plaintext - if you want to hide it, install getpass & keyring): ')

authorization = (username, pw)
auth = session.get('https://api.github.com', auth=authorization)
auth.raise_for_status()

BASE_URL = "https://api.github.com/repos/astropy/astropy/issues"

created = []
closed = []

params = {}
params['per_page'] = 100

params['state'] = 'closed'
params['page'] = 1

while True:

    response = session.get(BASE_URL, params=params, auth=authorization)
    if response.status_code == 403:
        print('.', end='')
        time.sleep(1)
        continue
    response.raise_for_status()
    results = response.json()

    if len(results) == 0:
        break

    for issue in results:
        created.append(issue['created_at'])
        closed.append(issue['closed_at'])

    params['page'] += 1
    print("Retrieved page {0} of closed issues".format(params['page']))
    # slow it down so we don't exceed the rate limit imposed by the API
    time.sleep(1)

params['state'] = 'open'
params['page'] = 1

while True:

    response = session.get(BASE_URL, params=params, auth=authorization)
    if response.status_code == 403:
        print('.', end='')
        time.sleep(1)
        continue
    response.raise_for_status()
    results = response.json()

    if len(results) == 0:
        break

    for issue in results:
        created.append(issue['created_at'])

    params['page'] += 1

    print("Retrieved page {0} of open issues".format(params['page']))
    # slow it down so we don't exceed the rate limit imposed by the API
    time.sleep(1)

with open('created.txt', 'w') as f:
    for c in created:
        f.write(c + '\n')

with open('closed.txt', 'w') as f:
    for c in closed:
        f.write(c + '\n')
