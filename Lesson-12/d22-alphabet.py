import string


class NotLetterException(Exception):
    def __init__(self, letter:str):
        self.message = f'Expected to get a letter. Got [{letter}]'
        super().__init__(self.message)

class NotASingleLetterError(Exception):
    def __init__(self,letter = str):
        self.message =f"Expected to get a single letter.\n" \
                      f"Got more than one letters: [{letter}]"
        super().__init__(self.message)


class AlphabetIterator:
    def __init__(self, letter:str):
        if not letter.isalpha():
            raise NotLetterException(letter=letter)

        if len(letter)!=1:
            raise NotASingleLetterError(letter=letter)

        self._letter = letter
        self._index = (string.ascii_lowercase).index(self._letter) + 1


    def __str__(self):
        return f"Start letter -> {self._letter} | index -> {self._index}"

    def __iter__(self):
        return self

    def __next__(self):
        if self._index<27:
            self._index+=1
            self._letter = string.ascii_lowercase[self._index]
            return self
        else:
            raise StopIteration


if __name__ == '__main__':

    try:
        my_letter = AlphabetIterator(letter = 'av')
        print(my_letter)

        print(next(my_letter))
        print(next(my_letter))
        print(next(my_letter))
        print(next(my_letter))
    except NotLetterException as e:
        print(f"Exception occured: NotLetterException\n"
              f"{e}")
    except NotASingleLetterError as e:
        print(f"Exception occured: NotASingleLetterError\n"
              f"{e}")

    # for i in my_letter:
    #     print(i)


