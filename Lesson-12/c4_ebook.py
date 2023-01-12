import os
from time import sleep


class Ebook():
    def __init__(self,file_path: str, words_per_page: int):
        self._path = file_path
        self._validate_path_exists()

        self._tot_amount_of_words = 0

        self._words_per_page = words_per_page
        self._tot_num_of_pages = 0

        self._pages = {} # {pg_num (int) : str}
        self._get_ebook_content()

        self._bookmarks_by_name = {}
        #{'bookmark_name': page_num (int)}

        self._bookmarks_by_page = {}
        # {page {id}: list('bookmark_name')

        self._current_page = 0

    def __iter__(self):
        return self

    def __next__(self):
        next_page = self._current_page+1
        if next_page <= self._tot_num_of_pages:
            self._current_page=next_page
            return self.get_content_by_page(self._current_page)
        else:
            raise StopIteration

    def _validate_path_exists(self):
        if not os.path.exists(self._path):
            raise FileNotFoundError()

    def _validate_page_num_exist(self, pg_num:int):
        if pg_num > self._tot_num_of_pages:
            raise ValueError(f"Page number error. Maximum pages [{self._tot_num_of_pages}] , you requested [{pg_num}]")

    def _validate_bokkmark_name_not_exist(self, bookmark_name: str):
        if bookmark_name in self._bookmarks_by_name.keys():
            raise ValueError(f"Bookmark name [{bookmark_name}] exists already.")

    def _validate_bookmark_name_exist(self, bookmark_name: str):
        if bookmark_name not in self._bookmarks_by_name.keys():
            raise ValueError(f"Bookmark name [{bookmark_name}] exists already.")

    def _validate_bookmarks_exists_per_page_num(self, pg_num: int):
        if not self._bookmarks_by_page.get(pg_num):
            raise ValueError(f"There are no bookmarks for this page, page num [{pg_num}]")

    def get_content_by_page(self,page_num:int):
        self._validate_page_num_exist(page_num)
        return self._pages.get(page_num)

    def get_last_page(self):
        return self._pages[len(self._pages)]

    def store_bookmark_by_name(self,page_num:int, bookmark_name: str):
        # Validate page_num exist
        # Validate 'bookmark_name' does not exist
        # store bookmark in self._bookmarks_by_name and self._bookmarks_by_page
        self._validate_page_num_exist(pg_num=page_num)
        self._validate_bokkmark_name_not_exist(bookmark_name=bookmark_name)

        # Add unique bookmark name
        self._bookmarks_by_name[bookmark_name] = page_num


        if not self._bookmarks_by_page.get(page_num):
            self._bookmarks_by_page[page_num] = [bookmark_name]
        else:
            self._bookmarks_by_page[page_num].append(bookmark_name)

    def delete_bookmark_by_name(self,bookmark_name: str):
        self._validate_bookmark_name_exist(bookmark_name=bookmark_name)

        # Getting the page number of the bookmark to remove it from the list
        # of bookmarks in self._bookmarks_by_page
        bm_page = self._bookmarks_by_name.get(bookmark_name)

        # Removing the bookmark from self._bookmarks_by_name
        self._bookmarks_by_name.pop(bookmark_name)

        # Removing the bookmark name from the list of self._bookmarks_by_page saved by page_num
        self._bookmarks_by_page.get(bm_page).remove(bookmark_name)

    def delete_all_bookmarks_by_page(self,pg_num : int):
        self._validate_page_num_exist(pg_num=pg_num)
        self._validate_bookmarks_exists_per_page_num(pg_num=pg_num)

        # Getting the list of bookmarks according page number
        # Deleting bookmarks in self._bookmarks_by_name
        for bookmark in self._bookmarks_by_page.get(pg_num):

            # Deleting bookmark both from
            #       self._bookmarks_by_name &
            #       self._bookmarks_by_page
            self.delete_bookmark_by_name(bookmark_name=bookmark)

    def display_all_bookmarks(self):
        print(self._bookmarks_by_name.keys())

    def display_bookmarks_page_by_name(self,bookmark_name: str):
        self._validate_bookmark_name_exist(bookmark_name=bookmark_name)
        print(f"Bookmark: {bookmark_name} | Page : {self._bookmarks_by_name.get(bookmark_name)}")

    def _get_ebook_content(self):
        pg=1
        words_in_cur_pg = 0
        pg_content = ''
        word_counter=0
        with open(self._path, 'r') as fh:
            for line in fh:
                splited_line = line.split()
                # Join whole lines if not exceeds # of words per page
                if len(splited_line)+ words_in_cur_pg < self._words_per_page and len(line)!=0:
                    pg_content= pg_content+''.join(line)
                    words_in_cur_pg+=len(splited_line)

                else:
                    # Go word by word
                    for word in splited_line:
                        pg_content = pg_content + word + ' '
                        words_in_cur_pg += 1
                        if words_in_cur_pg == self._words_per_page:
                            self._pages[pg]=pg_content
                            pg+=1
                            word_counter += words_in_cur_pg
                            pg_content=''
                            words_in_cur_pg=0


        # eof
        if words_in_cur_pg>0:
            word_counter += words_in_cur_pg
            self._pages[pg] = pg_content
            # print(word_counter)

        self._tot_num_of_pages=pg
        self._tot_amount_of_words= word_counter

    def _calculate_num_of_page(self):
        return len(self._pages.keys())

    def get_tot_amount_of_pages(self):
        return self._tot_num_of_pages

    def get_tot_amnt_of_words(self):
        return self._tot_amount_of_words


if __name__ == '__main__':
    my_book = Ebook('alice_in_wonderland/alice_book.txt',words_per_page=200)
    # my_book = Ebook('alice_in_wonderland/al_1.txt', words_per_page=50)

    # print(my_book.get_last_page())
    print(my_book.get_tot_amount_of_pages())
    # print(my_book.get_tot_amnt_of_words())
    #
    # print(my_book.get_content_by_page(page_num=3))

    for count, pg in enumerate(my_book):
        print(f"\n------------------------------------------------> pg # {count}\n")
        print(pg)

    print(my_book.get_tot_amount_of_pages())




