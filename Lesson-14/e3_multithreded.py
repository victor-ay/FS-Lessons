import concurrent
import datetime
import time
from concurrent.futures import ThreadPoolExecutor, wait
from pprint import pprint

import pytz

import requests

# national_api = "https://api.nationalize.io/?name=nathaniel"
#valeria
national_api = "https://api.nationalize.io"
country_code_api = "https://restcountries.com/v3.1/alpha/"

# person_name = input(f"Input your name: ")


# tz = datetime.datetime.utcnow().astimezone(pytz.timezone('Israel'))
# print(tz)

# national_response = requests.get(url=national_api, params={'name':person_name})
# if national_response.status_code<400:
#     national_response_json = national_response.json()
#     country_list = national_response_json['country']
#     country_list_sorted = sorted(country_list, key=lambda x: x['probability'], reverse=True)
#     country_code = country_list_sorted[0]['country_id']
#
#     search_country = country_code_api+country_code
#     country_data_response= requests.get(url=search_country)
#
#     if country_data_response.status_code<400:
#         country_data_response_json = country_data_response.json()
#         country_name_common = country_data_response_json[0]["name"]["common"]
#         country_continent = country_data_response_json[0]["continents"]
#         c_languages = country_data_response_json[0]["languages"].values()
#         print(f"{person_name} is probably from : {country_name_common}\n"
#               f"Continent: {country_continent}\n"
#               f"Languages: {c_languages}")
#     else:
#         print(f"Probably api responded wrongly. Tried to find [{country_data_response}]")
# else:
#     print(f"Your input probably not a name: [{person_name}]")

def request_single_name(person_name:str) -> dict:
    requested_data_for_name = {}

    national_response = requests.get(url=national_api, params={'name': person_name})
    if national_response.status_code < 400:
        national_response_json = national_response.json()
        country_list = national_response_json['country']
        country_list_sorted = sorted(country_list, key=lambda x: x['probability'], reverse=True)
        country_code = country_list_sorted[0]['country_id']



        search_country = country_code_api + country_code
        country_data_response = requests.get(url=search_country)

        if country_data_response.status_code < 400:
            country_data_response_json = country_data_response.json()
            country_name_common = country_data_response_json[0]["name"]["common"]
            country_continent = country_data_response_json[0]["continents"]
            c_languages = country_data_response_json[0]["languages"].values()

            requested_data_for_name = {
                'person_name': person_name,
                'country_code':country_code,
                'country_name_common':country_name_common,
                'country_continent':country_continent,
                'c_languages':c_languages
            }


            return requested_data_for_name
    else:
        print(f"Your input probably not a name: [{person_name}]")

def request_list_of_names(names_str:str) -> [dict]:
    names_list = names_str.split(',')
    list_of_country_data = []

    executor = ThreadPoolExecutor(max_workers=16)
    futures = []

    for name in names_list:
        # list_of_country_data.append(request_single_name(person_name=name))
        future = executor.submit(list_of_country_data.append(request_single_name(person_name=name)))
        futures.append(future)

    done, not_done = wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
    return done


names_str=input(f"Input names, seperated by coma:\n >>")

t1 = time.time()
l_name_country = request_list_of_names(names_str)
t2 = time.time()


for country_info in l_name_country:
    pprint(country_info)
    print()


print(f"It took: {t2-t1} sec\n"
      f"#of names: {len(l_name_country)}")

# victor,valeria,eyal,niv,moshe,albert,yohan,agrval,muhamad,noa
