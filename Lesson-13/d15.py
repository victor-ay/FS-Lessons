# def uppercase_decorator(function):
#     def wrapper():
#         func = function()
#         make_uppercase = func.upper()
#         return make_uppercase
#
#     return wrapper
#
# @uppercase_decorator
# def say_hi():
#     return 'hello there'
#
# say_hi()

class InvalidArgument(Exception):
    def __init__(self):
        super().__init__()
    def __str__(self):
        return f"Your input is not a string or has multiple arguments"



def single_str_arg(function):
    def wrapper(*args, **kwargs):
        print(f"Len of args = [{len(args)}]")
        print(f"Type of function = [{type(function)}]")
        if len(args)>1 or type(function())!=str:
            raise InvalidArgument
    return wrapper

@single_str_arg
def should_get_string(argum):
    return argum

if __name__ == '__main__':
    try:
        should_get_string('abc')
    except InvalidArgument as e:
        print(e)