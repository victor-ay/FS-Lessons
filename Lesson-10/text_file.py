import _io
import csv
import json
import os
import re
from abc import ABC, abstractmethod
from pprint import pprint

from text_exceptions import *


class TextFile(ABC):
    def __init__(self,f_path:str):
        #check if file exists
        #Check file type
        #save file to path
        self._path = f_path
        self._type = os.path.splitext(self._path)[-1][1:]

        if self._type not in self._get_extension():
            raise TypeError(f"The file should be [txt] only. Your file is [{self._type}]")

        if not os.path.exists(self._path):
            raise FileNotFoundError()

        self._path = f_path

        self._size = os.path.getsize(self._path)
        # self._data= self.get_content()


    @abstractmethod
    def _get_extension(self):
        pass

    def get_file_size(self):
        return self._size

    def get_file_type(self):
        return self._type

    def get_path(self):
        return self._path

    @abstractmethod
    def _read_data_from_file(self, fh):
        pass

    def get_content(self):
        with open(self._path, 'r') as fh:
            return self._read_data_from_file(fh)



    @abstractmethod
    def __add__(self, other: 'TextFile'):
        '''
        Creates new file name from <self> and <other> and returns new name after
        a couple of different checks.
        Returning file name as follows: <self_parent_dir>/<self_base_name>_<other_base_name>.<self_extension>
        :param other:
        :return:
        '''



        #check if other file exists
        # if not os.path.exists(other):
        #     raise FileNotFoundError()

        #check if both file are from the same type
        other_type = os.path.splitext(other._path)[-1][1:]
        if not self._type == other_type:
            raise TypeError(f"Not possible to add [{self._type}] and [{other_type}]")

        #create name of potential future file
        self_base_name = os.path.basename(os.path.splitext(self._path)[0]) #get file name from file #1
        self_dir_name = os.path.dirname(self._path)  # get file path without name from file #1
        other_base_name = os.path.basename(os.path.splitext(other._path)[0]) #get file name from file #2

        #create new path, by joining all names
        new_file_name = os.path.join(self_dir_name,self_base_name+'_'+other_base_name+'.'+self._type)


        #check if path exists already
        if os.path.exists(new_file_name):
            raise FileExistsError(f"Trying to create a file that exists already: [{new_file_name}]\n"
                                  f"You can pass custom file name to argument <custom_name>")

        return new_file_name


class CsvFile(TextFile):

    def __init__(self,file_path:str, delimiter=','):
        super().__init__(f_path=file_path)
        self._delimiter = delimiter

    def _get_extension(self):
        return ['csv']

    def _read_data_from_file(self, fh: _io.TextIOWrapper):
        ret_val = []
        field_index = None
        if not self._validate_csv_has_header(self):
            col_num = len(fh.readline().split(sep=self._delimiter))
            field_index = list(map(str, list(range(0, col_num))))
            fh.seek(0)

        for row in csv.DictReader(f=fh, fieldnames=field_index, delimiter=self._delimiter):
            ret_val.append(row)

        return ret_val

    @staticmethod
    def _validate_csv_correct(csv_file: 'CsvFile'):
        '''
        Validates that all columns in the file exists
        :param csv_file: CsvFile type
        :return:
        '''
        csv_content = csv_file.get_content()
        csv_col_num = len(csv_content[0])

        for csv_line in csv_file.get_content():
            if len(csv_line) != csv_col_num:
                raise CsvColumnsDontMatch()

    @staticmethod
    def get_headers(csv_file: 'CsvFile') -> list:
        """
        Returns list of headers from csv file.
        The returned list has case-sensitive values.
        Excessive spaces are removed from beginning and end of the word.

        If csv has no headers -> method will return list of indexes according to
        number of columns in the first row

        :param csv_file:
        :return: list of headers (strings)
        """

        # Getting list of keys from first element of returned list of dictionaries.
        # The returned list of dictionaries represent CSV file, where keys are columns names

        headers = list(csv_file.get_content()[0].keys())

        # removing excessive
        headers = list(map(str.strip,headers))


        return headers

    def _validate_csvs_have_same_headers(self, other: 'CsvFile', case_sensitive=True):
        self_headers = self.get_headers(self)
        other_headers = self.get_headers(other)

        # If there is a need for a case-insensitive check
        if not case_sensitive:
            # Get all elements of list to be lowercase
            self_headers = list(map(str.lower,self_headers))
            other_headers = list(map(str.lower, other_headers))

        if len(set(self_headers).difference(other_headers)) > 0:
            raise CsvColumnsDontMatch(msg=f'Names of columns in provided csv files are different')

    def __add__(self, other: 'CsvFile'):
        new_file_name = super().__add__(other)


        # Check if csv files are not corrupted -> every line has the same number of arguments
        self._validate_csv_correct(self)
        self._validate_csv_correct(other)

        # Getting content from csv files
        self_content = self.get_content()
        other_content = other.get_content()

        # Check if <self> and <other> have the same number of columns
        if len(self_content[0]) != len(other_content[0]):
            raise CsvColumnsDontMatch(f"Number of columns in provided csv files does not match")

        # Check if <self> and <other> have same headers
        self._validate_csvs_have_same_headers(other=other)

        # Create new list that will include data from both csv files
        new_csv_list = []
        new_csv_list.extend(self_content)
        new_csv_list.extend(other_content)

        with open(new_file_name, 'w') as csvfile:
            fieldnames = self.get_headers(self)
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for line in new_csv_list:
                writer.writerow(line)

        return new_file_name

    @staticmethod
    def _validate_csv_has_header(csv_file: 'CsvFile') -> bool:
        """
        Returns TRUE if csv_file has header
        :param csv_file:
        :return:
        """
        with open(csv_file.get_path(), 'r') as fd :
            has_header = csv.Sniffer().has_header(fd.read(2048))
        return has_header

    def get_rows_num(self) -> int:
        """
        Returns amounts of rows in file, not including the line of headers
        :return: row_nums
        """
        rows_num = len(self.get_content())
        # if not self._validate_csv_has_header(self):
        #     rows_num+=1
        return rows_num

    def get_columns_num(self) -> int:
        """
        Returns number of columns in csv file
        :return:
        """
        return len(self.get_content()[0])

    @staticmethod
    def _validate_number_in_range(input_num: int, min_range: int, max_range: int) :
        if input_num < min_range or input_num > max_range:
            raise ValueError(f"Your input number [{input_num}] should be between [{min_range}] and [{max_range}]")

    def get_row(self, row_num: int) -> dict:
        self._validate_number_in_range(input_num=row_num, min_range=0,max_range=self.get_rows_num())
        return self.get_content()[row_num]

    def get_column(self,col_num: int) -> list[str]:
        self._validate_number_in_range(input_num=col_num, min_range=0,max_range=self.get_columns_num())
        ret_val = []
        all_content = self.get_content()
        k_name = list(all_content[0].keys())[col_num]
        for content_row in all_content:
            ret_val.append(content_row[k_name])
        return ret_val

    def get_cell(self, row_num: int, col_num: int):
        self._validate_number_in_range(input_num=row_num, min_range=0,max_range=self.get_rows_num())
        self._validate_number_in_range(input_num=col_num, min_range=0,max_range=self.get_columns_num())
        all_content = self.get_content()
        k_name = list(all_content[0].keys())[col_num]
        return self.get_content()[row_num][k_name]




class JsonFile(TextFile):

    def __init__(self,file_path:str):
        super().__init__(f_path=file_path)
        self._dict_1 = None # for comparison and validations
        self._dict_2 = None # for comparison and validations

    def _get_extension(self):
        return ['json']

    def _read_data_from_file(self, fh):
        return json.load(fh)

    def _read_and_store_content(self, dict_1: dict, dict_2: dict):
        pass

    @staticmethod
    def _validate_dict_dimenssions_are_equal(dict_1: dict, dict_2: dict):
        if len(dict_1)!=len(dict_2):
            raise TypeError(f"Dictionaries have different length: len(dict_1) != len(dict_2)")

    @staticmethod
    def _validate_dictionaries_keys_equals(dict_1: dict, dict_2: dict):
        if set(dict_1.keys()) != set(dict_2.keys()):
            raise ValueError(f"Dictionary's keys are different")

    @staticmethod
    def _validate_dictionaries_values_same_type(dict_1: dict, dict_2: dict):
        for key_1, value_1 in dict_1.items():
            value_2 = dict_2.get(key_1)
            if type(value_1) != type(value_2)\
                    and (value_1 != None or value_2 != None):
                raise ValueError(f"Dictionary type values mismatch. {type(value_1)} != {type(value_2)}")

    def _validate_dicts_has_same_structure(self,dict_1: dict, dict_2: dict):
        """
        Checks if 2 dictionaries has same structures
        :return:
        """
        # Possibilities: {key: object} , {key:list}, {key:tuple}, {key:class}, {key:dictionary}

        # Validate dimensions of <self> and <other> are equal

        # Validate lengths of dictionaries are same
        self._validate_dict_dimenssions_are_equal(dict_1=dict_1, dict_2=dict_2)

        # Validate if keys are same
        self._validate_dictionaries_keys_equals(dict_1=dict_1, dict_2=dict_2)

        # Validate if values are from the same type
        self._validate_dictionaries_values_same_type(dict_1=dict_1, dict_2=dict_2)





    def __add__(self, other):
        """
        Creates new json file by name returned from parent abstract class.
        Creates an empty list.
        Copy to newly created file jsons <self> (file #1)
         -> ads new line -> and then copies from <other> file text line by line.

        Returns the relative path to newly created file.

        :param other:
        :return:
        """

    def is_list(self) -> bool:
        return isinstance(self.get_content(),list)

    def is_object(self) -> bool:
        """
        Returns true if object is from dictionary type
        :return:
        """
        return isinstance(self.get_content(),dict)


class TxtFile(TextFile):
    def _get_extension(self):
        return ['txt']

    def _read_data_from_file(self, fh):
        return fh.read()

    def __add__(self, other):
        '''
        Inherits from abstract class method __add__.
        Creates new txt file by name returned from parent abstract class.
        Copy to newly created file text line by line from <self> (file #1)
         -> ads new line -> and then copies from <other> file text line by line.

        Returns the relative path to newly created file.

        :param **kwargs:
        :param other:
        :return: The relative path to newly created file.
        '''
        new_file_name = super().__add__(other)

        #creating and opening new file to write into
        new_file = open(new_file_name, 'w')

        #get line by line from file #1 to new file
        with open(self.get_path(), 'r') as fh:
            for line in fh:
                new_file.write(line)

        #go to new line before adding content from file #2
        new_file.write('\n')

        # get line by line from file #1 to new file
        with open(other.get_path(),'r') as fh:
            for line in fh:
                new_file.write(line)

        #releasing newly created file
        new_file.close()

        return new_file_name

    def get_words_num(self) -> int:
        word_num=0
        if len(self.get_content())>0:
            word_num =len(self.get_content().strip().split(' '))
        return word_num

    def get_avg_word_len(self) -> float:
        """
        Returns average word length. Word length takes into account alphabetic symbols and symbol(_)
        :return:
        """
        words_num = self.get_words_num()
        num_of_spaces = words_num-1
        initial_text = self.get_content().strip()
        cleared_text = re.sub('[^a-zA-Z _]', '', initial_text)
        num_of_symbols = len(cleared_text)-num_of_spaces
        avg_word_len = round(num_of_symbols/words_num,1)
        return avg_word_len



if __name__ == '__main__':
    # my_file = TxtFile('E3.txt')
    # my_file = JsonFile('j.json')
    # my_file_2 = JsonFile('j2.json')
    # my_file = CsvFile('b_1.csv')

    # print(my_file.get_file_type())
    # print(my_file.get_file_size())
    # print(my_file.get_content())

    # m_txt_1 = TxtFile('files_to_play/t1.txt')
    # m_txt_2 = TxtFile('files_to_play/t2.txt')
    # m_txt_3 = TxtFile('files_to_play/t3.txt')

    j_file = JsonFile('files_to_play/j.json')
    jj=j_file.get_content()
    print(set(jj.keys()))
    for value in jj.values():
        print(type(value))
    # pprint(jj)






