import time
from concurrent.futures import ProcessPoolExecutor, Future
from math import factorial

def simple_factorial(num):
    return factorial(num)

def just_print(f:Future):
    # print(f" --> ")
    f.result()
    # print(f" -->  {f.result()}")

def calc_factorial(int_list:[int]):
    with ProcessPoolExecutor() as executor:
        futures=[]
        for num in int_list:
            future = executor.submit(simple_factorial,num)
            futures.append(future)

        for f in futures:
            f.add_done_callback(just_print)


if __name__ == '__main__':
    # user_input = input(f"Input numbers separated coma:").split(',')
    # user_int = list(map(int,user_input))

    user_int = [1550]*100_000

    # t1 = time.time()
    # for i in user_int:
    #     simple_factorial(i)
    #     # print(simple_factorial(i))
    # t2 = time.time()


    t3 = time.time()
    calc_factorial(user_int)
    t4 = time.time()

    # print(f"One process Took : {t2-t1}")
    print(f"Multi process Took : {t4 - t3}")