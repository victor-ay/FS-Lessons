import requests
import os

url = "https://www.virustotal.com/api/v3/urls/aHR0cHM6Ly9lZHVsYWJzLmNvLmls"

with open(os.environ["VT_KEY"], 'r') as fh:
    vt_api_key = fh.read()

headers = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "x-apikey": vt_api_key
    }



response = requests.get(url, headers=headers)

print(response.text)
#
# print(os.environ["VT_KEY"])
#
# print(vt_api_key)