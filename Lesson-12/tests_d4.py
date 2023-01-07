import unittest
from d4_all_exercises import *


class D4Tests(unittest.TestCase):

    def setUp(self) -> None:
        # List of wrong date formats
        self._l1_wrong_formats = ['adsd','thd', '11-12-200e', '111', '00-00-00000', 11]
        self._date_list = ['12-12-2021', '18-12-2021', '19-12-2021']
        # self._should

    def test_wrong_formats(self):
        """
        Tests if immune to wrong date formats.
        :return:
        """
        with self.assertRaises(ValueError):
            for elem in self._l1_wrong_formats:
                validate_date_input(elem)

    def test_date_filter(self):
        self.assertTrue(sat_fri_filter_func('08-01-2023'), msg=f"Wrongly filters non Friday and Saturday")
        self.assertFalse(sat_fri_filter_func('07-01-2023'), msg=f"Not filters Friday and Saturday")

    def test_date_list_filter(self):
        self.assertTrue(filter_fri_sat(self._date_list) == ['12-12-2021', '19-12-2021'])

if __name__ == '__main__':
    unittest.main()
