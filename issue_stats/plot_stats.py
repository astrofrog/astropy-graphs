import numpy as np
import dateutil.parser
from datetime import datetime as dt
import matplotlib.pyplot as plt

plt.rc('axes', titlesize='medium')
plt.rc('axes', labelsize='medium')
plt.rc('xtick', labelsize='small')
plt.rc('ytick', labelsize='small')
plt.rc('xtick.major', size=2)
plt.rc('ytick.major', size=2)
plt.rc('xtick.minor', size=1)
plt.rc('ytick.minor', size=1)
plt.rc('font', family='serif')
plt.rc('axes', linewidth=0.5)
plt.rc('patch', linewidth=0.5)

import requests
from bs4 import BeautifulSoup

changelog = requests.get('http://docs.astropy.org/en/stable/changelog.html')
soup = BeautifulSoup(changelog.text, 'html5lib')

releases = {}
for entry in soup.findAll('h2'):
    version, date = entry.text.split()
    date = date.split("(")[1].split(")")[0]
    if date == 'unreleased':
        releases[version] = dt.today()
    else:
        releases[version] = dt.strptime(date, "%Y-%m-%d")


def to_year_fraction(date):

    import time

    def sinceEpoch(date): # returns seconds since epoch
        return time.mktime(date.timetuple())
    s = sinceEpoch

    year = date.year
    startOfThisYear = dt(year=year, month=1, day=1)
    startOfNextYear = dt(year=year+1, month=1, day=1)

    yearElapsed = s(date) - s(startOfThisYear)
    yearDuration = s(startOfNextYear) - s(startOfThisYear)
    fraction = yearElapsed/yearDuration

    return date.year + fraction

created = []
for line in open('created.txt'):
    date = dateutil.parser.parse(line)
    day_of_year = to_year_fraction(date)
    created.append(day_of_year)
created = np.array(created)
created.sort()
created_n = np.arange(len(created)) + 1.

closed = []
for line in open('closed.txt'):
    date = dateutil.parser.parse(line)
    day_of_year = to_year_fraction(date)
    closed.append(day_of_year)
closed = np.array(closed)
closed.sort()
closed_n = np.arange(len(closed)) + 1.

dates = np.hstack([created, closed])
diffs = np.hstack([np.repeat(1, len(created)), np.repeat(-1, len(closed))])

order = np.argsort(dates)

dates = dates[order]
diffs = diffs[order]
total = np.cumsum(diffs)

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(created, created_n, color='red', lw=2, label='total')
ax.plot(closed, closed_n, color='green', lw=2, label='closed')
ax.plot(dates, total, color='blue', lw=2, label='open')
ax.xaxis.set_ticks([2011, 2012, 2013, 2014, 2015, 2016, 2017])
ax.legend(loc='center left', fontsize=11)
ax.xaxis.set_ticklabels(['2011', '2012', '2013', '2014', '2015', '2016', '2017'])

upper = np.max(created_n)

for release, date in releases.items():
    if release.count(".") == 1:
        ax.axvline(to_year_fraction(date), color='k', lw=1, alpha=0.8)
        ax.text(to_year_fraction(date) - 0.01, upper, release, rotation=90, ha='right', size=10)
    else:
        ax.axvline(to_year_fraction(date), color='k', lw=1, alpha=0.3)

ax.set_xlabel("Time")
ax.set_ylabel("Number of issues")
ax.set_title("Astropy issues")
ax.set_xlim(2011.75, 2017.35)
fig.savefig('issue_stats.png', dpi=150)
