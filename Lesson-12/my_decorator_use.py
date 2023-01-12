import math
from time import sleep
from my_decorators import *

@performance_log(time_units='ns')
def calc_factorial():
    # num = input(f"Insert num: ")
    # print(math.factorial(int(num)))
    sleep(1)

@performance_log(time_units='s')
def run_loop():
    for i in range(10000):
        j = i**i

if __name__ == '__main__':
    calc_factorial()
    # run_loop()