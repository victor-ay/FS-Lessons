import calendar
import datetime

#
# def my_generator(n):
#
#     # initialize counter
#     value = 0
#
#     # loop until counter is less than n
#     while value < n:
#
#         # produce the current value of the counter
#         yield value
#
#         # increment the counter
#         value += 1
#
# # iterate over the generator object produced by my_generator
# for value in my_generator(3):
#
#     # print each value produced by generator
#     print(value)
#
# ##################
#
# # create the generator object
# squares_generator = (i * i for i in range(5))
#
# # iterate over the generator and print the values
# for i in squares_generator:
#     print(i)
import time

from pip._internal.utils.misc import enum


def my_date_generator(my_date:datetime.date):
    days_in_month = calendar.monthrange(year=my_date.year, month=my_date.month)[1]
    last_day_in_month = datetime.date(year=my_date.year, month=my_date.month, day=days_in_month)

    while my_date <= last_day_in_month:
        yield my_date
        my_date+=datetime.timedelta(days=1)


def batches(n: int, my_list:list):
    batch_start= 0
    batch_ends = n
    list_len = len(my_list)

    if batch_ends>list_len-1:
        batch_ends=list_len

    while list_len-1>batch_start:
        yield my_list[batch_start:batch_ends]
        batch_start = batch_ends
        batch_ends+=n
        if batch_ends>list_len-1:
            batch_ends=list_len


def my_fib(num:int):
    n1=0
    n2=1
    tn=n1
    for i in range(num):
        yield n2
        tn=n1
        n1=n2
        n2+=tn

if __name__ == '__main__':
    # for day in my_date_generator(datetime.date.today()):
    #     print(day)
    #
    # for i in range(10):
    #     print(my_fib())

    l1 = [i for i in range(11)]
    print(l1)
    for i in batches(3,l1):
        print(i)
    count =0
    for i in my_fib(10):
        print(f"i={i} | Count = {count}")
        time.sleep(0.5)