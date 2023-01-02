import time
from concurrent.futures import ThreadPoolExecutor, Future

import requests as requests

def just_print(f:Future):
    if f.exception():
        print(f"API responded with exception")
    else:
        print(f" -->  {f.result()}")

def print_seconds():
    time_input = input(f"Insert time in sec: ")
    t_now = time.strptime(time_input,"%S").tm_sec
    t_delta = 0.1
    t_count =0
    with ThreadPoolExecutor() as executor:
        while t_now>0:
            t_count+=1
            futures = []
            if t_count==10:
                t_count=0

                future = executor.submit(send_req)
                futures.append(future)

                for f in futures:
                    f.add_done_callback(just_print)

        print(f"{t_now} seconds left")
        time.sleep(t_delta)
        t_now=round(t_now- t_delta,1)


    print("DONE!")

def send_req():
    response = requests.get('https://api.kanye.rest/')
    return response.json()['quote']


if __name__ == '__main__':
    print_seconds()
    # print(f"Response = {send_req()}")
    # print(39.2%10)