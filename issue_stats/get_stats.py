import json
import time

import requests

BASE_URL = "https://api.github.com/repos/astropy/astropy/issues"

created = []
closed = []

params = {}
params['per_page'] = 100

params['state'] = 'closed'
params['page'] = 1

while True:

    results = requests.get(BASE_URL, params=params).json()

    if len(results) == 0:
        break

    for issue in results:
        created.append(issue['created_at'])
        closed.append(issue['closed_at'])

    params['page'] += 1

params['state'] = 'open'
params['page'] = 1

while True:

    results = requests.get(BASE_URL, params=params).json()

    if len(results) == 0:
        break

    for issue in results:
        created.append(issue['created_at'])

    params['page'] += 1

with open('created.txt', 'w') as f:
    for c in created:
        f.write(c + '\n')

with open('closed.txt', 'w') as f:
    for c in closed:
        f.write(c + '\n')
