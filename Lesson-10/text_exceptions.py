class TextException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class CsvColumnsDontMatch(TextException):
    def __init__(self, msg=''):
        if len(msg) > 1:
            self._msg = msg
        else:
            self._msg = f"Columns in provided csv files does not match"
        super().__init__(msg)

