import concurrent.futures
import os
import time
from concurrent.futures import ThreadPoolExecutor, wait
from pprint import pprint

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

def web_request(url:str,ping_num:int):
    request = requests.get(url=url,headers=headers)
    if request.status_code >=400:
        pprint(f"request num = [{ping_num}] = {request.status_code}")
    elif ping_num%100==0:
        print(".", end="",sep="")

def web_requests_alot():
    t1 = time.time()
    for i in range(100):
        print(f">> [{i}]",end='',sep='')
        web_request('https://www.coding-academy.org/')
    t2 = time.time()
    print(f"Time = {t2-t1}")

def web_requests_alot_threaded():
    link = 'https://www.coding-academy.org/'
    executor = ThreadPoolExecutor(max_workers=128)
    futures = []

    t1 = time.time()
    for i in range(10_000):
        future = executor.submit(web_request, link, i)
        futures.append(future)


    done, not_done = wait(futures,return_when=concurrent.futures.ALL_COMPLETED)
    print(f"done: {len(done)}")
    t2 = time.time()
    print(f"Time = {t2-t1}")

web_requests_alot_threaded()
