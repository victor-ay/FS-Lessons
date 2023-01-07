import re
from datetime import datetime
from pprint import pprint

buses = [
    {
        "delays": ['1h 20m', '25m', '3h', '2h 1m'],
        "status": 'bad',
        "name": "Jacob",
        "route_num": 560
    },
    {
        "delays": ['20m', '5m', '3h'],
        "status": 'great',
        "name": "Moshe",
        "route_num": 769
    },
    {
        "delays": ['2h 3m'],
        "status": 'good',
        "name": "Jack",
        "route_num": 766
    },
    {
        "delays": ['6h'],
        "status": 'great',
        "name": "Mark",
        "route_num": 876
    },
    {
        "delays": ['2h 3m'],
        "status": 'good',
        "name": "Anna",
        "route_num": 456
    },
]


# D4-1
# Implement a function that receives a list of english letters and returns a list with alphabet
# indexes of the letters in the English Alphabet. Use map() to map a letter from the English
# alphabet to its alphabet index. Your code should support both lowercase and uppercase letters.
# The alphabet index for “a” and “A” is 1.
# The alphabet index for “b” and “B” is 2.
# The alphabet index for “z” and “Z” is 26.
# If one of the received elements of the list is not an English alphabet letter - raise an exception.
# For example, if you receive [‘a’, ‘Z’, ‘C’, ‘e’], your function should return [1, 26, 3, 5].
# If you receive [3, ‘bla’, ‘a’, ‘D’], you should raise an exception.
def letter_to_index(elem: str) -> int:
    """
    Receive string and returns its index in Alphabet: a=A=1
    :param alphabet_list:
    :return:
    """
    a_ascii = ord('A')
    z_ascii = ord('Z')
    ret_val = None

    if not elem.isalpha() or len(elem) != 1 \
            or ord(elem.upper()) < a_ascii or ord(elem.upper()) > z_ascii:
        raise ValueError(f"Expected to get a single english alphabetic charater. Got [{elem}]")

    ret_val = ord(elem.upper())-a_ascii+1

    return ret_val

# D4-2
# Implement a function that filters out vowels from the given string and returns the original
# string without the vowels. Vowels are the following letters (both lowercase and uppercase): a, e,  i, o, u
# Use filter() to filter vowels from a given word (string)

def filter_out_vowels(elem: str):
    vowels = ['a','e','i','o','u']
    if elem in vowels:
        return False
    return True

# D4-3
# Implement a function that gets a list of strings that represent dates in format dd-mm-yyyy.
# Use map() and filter() to filter from this list all the dates that are Fridays and Saturdays.
# Test with the following list: ['12-12-2021', '18-12-2021', '19-12-2021]
# Write 2 additional unit tests to test your implementation

def validate_date_input(elem: str):
    if not re.fullmatch('\d{2}-\d{2}-\d{4}', elem.strip()):
        raise ValueError(f"Expected to get string in following format : [dd-mm-yyyy]. Got [{elem}]")


def map_date_to_weekday(elem:str):
    validate_date_input(elem)
    return datetime.strptime(elem,'%d-%m-%Y').weekday()


def sat_fri_filter_func(elem: str):
    weekday = map_date_to_weekday(elem)
    if weekday == 4 or weekday == 5:
        return False
    return True


def filter_fri_sat(dates_list: list[str]) -> list[str]:
    """
    Receive list of dates in format of strings, where each string element in date format of "dd-mm-yyyy"
    Returns list of dates filtered out Saturdays and Fridays
    :param dates:
    :return:
    """
    # Validate input in format of dd-mm-yyyy
    # Map string to datetime -> weekday
    # Filter out Saturday and Friday

    filtered = list(filter(sat_fri_filter_func,dates_list))
    return filtered

# D4-4
# Implement a function that receives a list of strings, and returns a new list of strings
# with all the original strings sorted by the string length.

def sort_list_according_length(list_of_strings: list[str]):
    list_of_strings.sort(key=len)
    return list_of_strings

# D4-5
# Implement a function that gets a dictionary of the format below and returns
# it's elements sorted first by status (great - good - bad), then by total minutes late,
# then by name.


def map_status(elem:str) -> int:
    match elem:
        case 'great':
            return 1
        case 'good':
            return 2
        case 'bad':
            return 3


def map_single_dely_to_min(elem:str) -> float:
    ret_val = 0.0
    for time_elem in elem.split():
        if 'h' in time_elem:
            ret_val+=float(time_elem.split('h')[0])*60
        elif 'm' in time_elem:
            ret_val += float(time_elem.split('m')[0])
    return ret_val


def map_tot_min_late(late_list : list[str]) -> float:
    temp_list = list(map(map_single_dely_to_min,late_list))
    return sum(temp_list)


def sorting_bus_dict(buses_dict: list[dict]):
    buses_dict.sort(key=
                           lambda x: (map_status(x['status']),
                                      map_tot_min_late(x['delays']),
                                      x['name'])
                           )

    # buses_dict.sort(key=
    #                        lambda x: (
    #                                   x['name'])
    #                        )
    return buses_dict

# D4-6
# Use lambda and filter/map/sort. Given a list of strings, filter out those
# containing less than 2 "a" chars. For example, for ["apple", "ananas", "banana", "pear"],
# your code should return ["ananas", "banana"]

def non_double_a_filter(elem: str):
    if re.findall('.*a.*a',elem):
        return True
    return False


if __name__ == '__main__':

    pl = ["Python", "Swift","Java", "C++", "Go", "Rust"]
    pl.sort(key = lambda x: len(x))
    print(pl)

    print(map_tot_min_late(['1h 20m', '25m']))
    pprint(sorting_bus_dict(buses))

    l_fruits = ["apple", "ananas", "banana", "pear","anananan"]
    print(list(filter(non_double_a_filter,l_fruits)))
    # filter ( )


