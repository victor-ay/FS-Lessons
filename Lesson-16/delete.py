import datetime
from functools import lru_cache
from pprint import pprint

import pytz as pytz
import requests as requests

headers = {}


url="https://edulabs.co.il/"
response = requests.get(url=url, headers=headers)
t_lm_date = response.headers["Last-Modified"]
t_lm = datetime.datetime.strptime(t_lm_date,'%a, %d %b %Y %H:%M:%S %Z')

# print(t_lm_date)
# print(t_lm)


e = 1673625268
ed = datetime.datetime.fromtimestamp(e).astimezone(pytz.UTC)
print(f" ed = {ed}")

if t_lm< ed:

    print(f"Need to scan")
    print(type((ed-t_lm).days))

print(f"\nLast modified: {t_lm}\n"
      f"in UTC : {t_lm.astimezone(pytz.UTC)}")

