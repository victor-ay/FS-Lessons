import os
import unittest
from text_file import TxtFile, JsonFile, CsvFile

# class TestStringMethods(unittest.TestCase):
#
#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')
#
#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())
#
#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)

class TestTextFiles(unittest.TestCase):

    def setUp(self):
        self._t1_path = 'files_to_play/t1.txt'
        self._t2_path = 'files_to_play/t2.txt'
        self._t3_path = 'files_to_play/t3.txt'
#         self._txt_file_1 = TxtFile(self._t1_path)
#         # self._txt_file_2 = TxtFile(self._t2_path)
#         # self._txt_file_3 = TxtFile(self._t3_path)

    def test_not_text_file(self):
        with self.assertRaises(TypeError):
            txt_file_0 = TxtFile('files_to_play/j.json')

    def test_file_not_found(self):
        """
        Gets wrong path but with txt extension
        :return:
        """
        with self.assertRaises(FileNotFoundError):
            txt_file_0 = TxtFile('not_existing/not_existing_directory.txt')

    def test_file_type_and_extraction(self):
        tested_file_type = TxtFile(self._t1_path)
        self.assertEqual(tested_file_type.get_file_type(),'txt',f"Returns wrong extension")
        self.assertEqual(tested_file_type.get_path(), 'files_to_play/t1.txt', f"Returns wrong path")
        self.assertEqual(tested_file_type.get_file_size(), os.path.getsize(self._t1_path), f"Returns wrong file size")

class TestJsonFiles(unittest.TestCase):

    def setUp(self) -> None:
        self.not_json_file = 'files_to_play/t1.txt'
        self.path_not_exist = 'not_existing/not_existing_directory.json'
        self.json_object_path = 'files_to_play/j.json'
        self.json_list_of_objects_path = 'files_to_play/j2.json'

    def test_is_object(self):
        self.assertTrue(
            JsonFile(self.json_object_path).is_object())

    def test_is_list(self):
        self.assertTrue(
            JsonFile(self.json_list_of_objects_path).is_list())

    def test_dictionaries_has_diferent_size(self):
        dict_1 = {1: 'k11', 2: 'k12', 3: 'k13', 4: 'k14', 5: 'k15'}
        dict_2 = {1: 'v21', 2: 'v22', 3: 'v23', 4: 'v24', 5: 'v25'}
        dict_3 = {31: 'v31', 32: 'v32', 33: 'v33', 34: 'v34'} #dict_3 smaller then dict_1
        dict_4 = {'1': 'v21', 2: 'v22', 3: 'v23', 4: 'v24', 5: 'v25'}

        with self.assertRaises(TypeError):
            JsonFile(self.json_object_path)._validate_dict_dimenssions_are_equal(dict_1, dict_3)

        with self.assertRaises(TypeError):
            JsonFile(self.json_object_path)._validate_dict_dimenssions_are_equal(dict_1, dict_3)

    def test_dictionaries_has_same_keys(self):
        dict_1 = {1: 'k11', 2: 'k12', 3: 'k13', 4: 'k14', 5: 'k15'}
        dict_2 = {1: 'v21', 2: 'v22', 3: 'v23', 4: 'v24', 5: 'v25'}
        dict_3 = {31: 'v31', 32: 'v32', 33: 'v33', 34: 'v34', 35: 'v35'}
        dict_4 = {'1': 'v21', 2: 'v22', 3: 'v23', 4: 'v24', 5: 'v25'}

        with self.assertRaises(ValueError):
            JsonFile(self.json_object_path)._validate_dicts_has_same_structure(dict_1, dict_3)

        with self.assertRaises(ValueError):
            JsonFile(self.json_object_path)._validate_dicts_has_same_structure(dict_1, dict_4)

    def test_validate_dictionaries_values_same_type(self):
        # All dictionaries bellow are in the same length

        dict_c1 = {1: 'v11', 2: ['v121', 'v122'], 3: {'k11': 'some string', 'k12': [1, 2, 3, 4]}, 4: 'v14', 5: None}

        # Different from dict_c1 in key:2 : list -> tuple
        dict_c2 = {1: 'v11', 2: ('v121', 'v122'), 3: {'k11': 'some string', 'k12': [1, 2, 3, 4]}, 4: 'v14', 5: None}

        # Different from dict_c1 in key:2 : list -> dict
        dict_c3 = {1: 'v11', 2: {'d31':'v121', 'd32': 'v122'}, 3: {'k11': 'some string', 'k12': [1, 2, 3, 4]}, 4: 'v14', 5: None}

        # Different from dict_c1 in key:2 : list -> None ==> Should not raise EXCEPTION
        dict_c4 = {1: 'v11', 2: None, 3: {'k11': 'some string', 'k12': [1, 2, 3, 4]}, 4: 'v14', 5: None}

        with self.assertRaises(ValueError):
            JsonFile(self.json_object_path)._validate_dictionaries_values_same_type(dict_c1,dict_c2)

        with self.assertRaises(ValueError):
            JsonFile(self.json_object_path)._validate_dictionaries_values_same_type(dict_c1,dict_c3)

        with self.assertRaises(ValueError):
            JsonFile(self.json_object_path)._validate_dictionaries_values_same_type(dict_c1,dict_c4)



if __name__ == '__main__':
    unittest.main()