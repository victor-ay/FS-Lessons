import math
from pprint import pprint


class EBook:
    book_by_page = {int:str} # page_num: page content

    def __init__(self, book_path:str):
        self._book_path = book_path

        with open(self._book_path, 'r') as fh:
            self.__book_text = fh.read()

        self._list_of_words = self.__book_text.split(' ')
        self._pages = {} # pg_number : {'pg_start':start_word_index, 'pg_end':end_word_index}

    def divide_to_pages(self, words_per_page:int) -> {int:{int, int}}:
        amnt_of_pgs = self.get_tot_amnt_pages(words_per_page=words_per_page)
        for i in range(0,amnt_of_pgs):
            start_word_index = i*words_per_page
            if i == amnt_of_pgs-1:
                end_word_index = self._get_tot_amnt_of_words()-1
            else:
                end_word_index = start_word_index + words_per_page-1
            self._pages[i+1] = {'pg_start':start_word_index, 'pg_end':end_word_index}
        return self._pages


    def get_tot_amnt_pages(self, words_per_page:int)->int:
        return math.ceil( self._get_tot_amnt_of_words()/words_per_page)

    def display_page(self, page_num:int):
        page = ''
        # page = self.__book_text[self._pages[page_num]['pg_start']:self._pages[page_num]['pg_end']]
        print(f"Start word num-> {self._pages[page_num]['pg_start']} ; End word -> {self._pages[page_num]['pg_end']} ;")
        print(f"Start word -> [{self._list_of_words[self._pages[page_num]['pg_start']]}]")
        for i in range(self._pages[page_num]['pg_start'],self._pages[page_num]['pg_end']):
            page=' '.join(self._list_of_words[i])
        return page

    def _get_tot_amnt_of_words(self) -> int:
        return len(self._list_of_words)

my_book = EBook("data/alice.txt")
words_per_page=10000

print(my_book._get_tot_amnt_of_words())
print(my_book.get_tot_amnt_pages(words_per_page))
my_book.divide_to_pages(words_per_page=words_per_page)
print(my_book.display_page(3))



# ms ="It was high time to go, for the pool was getting quite crowded\
# with the birds and animals that had fallen into it:  there were a\
# Duck and a Dodo, a Lory and an Eaglet, and several other curious\
# creatures.  Alice led the way, and the whole party swam to the\
# shore."
#
# print(len(ms))
# words= ms.split()
# print(len(words))


