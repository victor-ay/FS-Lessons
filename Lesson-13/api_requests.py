import requests

# starting from GET

# sending rewuest to URL

# BORED_URL = "https://www.boredapi.com/api/activity"
# response = requests.get(BORED_URL)
# print(response)
# #
# print(response.status_code)
# print(response.text)
# print(response.text['activity']) # not working

# print(response.json())

response = requests.get("https://bad_url")
response = requests.get("https://www.boredapi.com/api/act")
print(response.status_code)
print(response.text)


GENDERIZE_URL = "https://api.genderize.io/"
response = requests.get(GENDERIZE_URL, params={'name': 'valeria'})
print(response.status_code, response.text, sep="\n")

GENDERIZE_URL = "https://api.genderize.io/bla/"
response = requests.get(GENDERIZE_URL, params={'name': 'valeria'})
print(response.status_code, response.text, sep="\n")

{"country": [{"country_id": "GH", "probability": 0.224}, {"country_id": "PH", "probability": 0.084},
             {"country_id": "NG", "probability": 0.073}, {"country_id": "US", "probability": 0.061},
             {"country_id": "NE", "probability": 0.034}], "name": "nathaniel"}

