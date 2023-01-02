import string

letters = ['a','S','f']

class LettersException(Exception):
    def __init__(self,letter:str):
        self.message = f"LettersException -> [{letter}]"
        super().__init__(self.message)

def letters_index(letter):
    if not letter.isalpha() or len(letter)!=1:
        raise LettersException(letter=letter)
    return (string.ascii_letters.index(letter)%26)+1

def vowels_filtered(letter: str):
    vowels = ['a', 'e',  'i', 'o', 'u']
    if letter.lower() in vowels:
        return True





if __name__ == '__main__':
    # try:
    #     indexes = list(map(letters_index,letters))
    # except LettersException as e:
    #     print(e)
    # print(indexes)

    ll = ['as','q','qwert']
    l1 = sorted(ll,key=lambda x: len(x))
    print(l1)

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

    def map_status(status:str):
        if status=='great':
            return 2
        if status=='good':
            return 1
        else:
            return 0

    def convert_to_min(delays:[str]):
        minutes =0
        for delay in delays:
            splited_time = delay.split()
            for t in splited_time:
                if 'h' in t:
                    minutes+=60*int(t.split('h')[0])
                elif 'm' in t:
                    minutes+=int(t.split('m')[0])
        return minutes



    d1 = sorted(buses, key=lambda x: (map_status(x['status']), convert_to_min(x['delays']), x['name']))
    print(d1)

