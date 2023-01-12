import time
from time import perf_counter, perf_counter_ns


def my_decorator(some_function):
    def wraper(*args, **kwargs):
        # Do something before calling function
        result = some_function(*args, **kwargs)

        # Do something after the function ends
        return result
    return wraper

# def performance_log(some_function):
#     def wraper(*args, **kwargs):
#
#         t1 = perf_counter()
#         result = some_function(*args, **kwargs)
#         t2 = perf_counter()
#         print(f"Function < {some_function.__name__} > time to run : {t2-t1} [sec]")
#
#         return result
#     return wraper


# @my_decorator_2(time_units = 'ms')
# => some_function = my_decorator_2(time_units = 'ms')(some_function)

def performance_log (time_units = 's'):
    def wraper(some_function):
        def decorator(*args, **kwargs):
            # Do something before running <some_function>
            time_func = perf_counter if time_units != 'ns' else perf_counter_ns
            t1 = time_func()
            results = some_function(*args,**kwargs)
            t2 = time_func()

            dt = t2-t1
            if time_units == 'ms':
                dt*=1000

            print(f"Time performance of <{some_function.__name__}> : {dt} [{time_units}] ")
            # Do something after the <some_function> ends to run
            return results

        return decorator

    return wraper