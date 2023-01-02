import _io
import csv
import json
import os
from abc import ABC, abstractmethod


class TextFile(ABC):
    def __init__(self,f_path:str):
        #check if file exists
        #Check file type
        #save file to path
        self._type = os.path.splitext(self._path)[-1][1:]

        if self._type not in self._get_extension():
            raise Exception()

        if not os.path.exists(self._path):
            raise FileNotFoundError

        self._path = f_path

        self._size = os.path.getsize(self._path)
        self._data= self.get_content()


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


class CsvFile(TextFile):
    def _get_extension(self):
        return ['csv']

    def __init__(self,file_path:str, delimiter=','):
        super().__init__(f_path=file_path)
        self._delimiter = delimiter

    def _read_data_from_file(self, fh:_io.TextIOWrapper):
        ret_val = []
        for row in csv.DictReader(f=fh,delimeter=self._delimiter):
            ret_val.append(row)
        return ret_val


class JsonFile(TextFile):
    def _get_extension(self):
        return ['json']

    def _read_data_from_file(self, fh):
        return json.load(fh)


class TxtFile(TextFile):
    def _get_extension(self):
        return ['txt']

    def _read_data_from_file(self, fh):
        return fh.read()


if __name__ == '__main__':
    # my_file = TxtFile('E3.txt')
    # my_file = TxtFile('j.json')
    # my_file = TxtFile('j2.json')
    my_file = TxtFile('biostats.csv')

    print(my_file.get_file_type())
    print(my_file.get_file_size())
    print(my_file.get_content())

    # with open('biostats.csv', newline='') as fh:
    #     t_data = csv.DictReader()
        # for row in t_data:
        #     print(row['id'], row['name'])
    # print(t_data)
