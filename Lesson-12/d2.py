# Iterators

import calendar
from datetime import datetime, timedelta
from time import sleep

# D2-1
# Implement a simple class DateIterator that should be initialized with a date and implements iterator protocol
# (__iter__ and __next__ method)  that on every iteration returns the next date up until the end of the month.


class DateIterator():
    """
    Iterates dates from the provided date until end of the provided month
    """
    def __init__(self,date: datetime.date):
        self._date = date
        self._last_date = self._calc_last_date()

    def _calc_last_date(self):
        """
        Returns the last day in the month. Uses Calendar package
        :return:
        """
        day, ndays = calendar.monthrange(self._date.year, self._date.month)
        last_date = datetime(year=self._date.year,
                                   month=self._date.month,
                                   day=ndays
                                   ).date()
        return last_date

    def __iter__(self):
        return self

    def __next__(self):
        self._date += timedelta(days=1)
        if self._date <= self._last_date:
            return self._date
        else:
            raise StopIteration

if __name__ == '__main__':
    dt = DateIterator(datetime.now().date())
    for d in dt:
        print(d)
        # sleep(0.2)