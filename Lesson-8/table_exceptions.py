class TableSystemException(Exception):
    pass

class PositiveIntNumber(TableSystemException):
    def __init__(self, num):
        super().__init__("")