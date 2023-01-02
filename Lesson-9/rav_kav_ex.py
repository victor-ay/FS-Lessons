import datetime


class Ride:
    def __init__(self):
        self.short_ride = {ra}
        self.short_ride_range


class RavKav:
    def __init__(self, holder_id: int, holder_name: str):
        self.holder_id = holder_id
        self.holder_name = holder_name
        self.__balance: float = 0
        self.__ride_type = {
            'short': {'range_km': 15,
                      'cost': 5.5},
            'medium': {'range_km': 12,
                       'cost': 5.5},
            'long': {'range_km': 10000,
                     'cost': 23},
        }
        self.rides_log = {datetime: str}

    def __str__(self):
        return f"<RavKav> status:\n" \
               f"\t>Balance: {self.__balance}\n"

    def topup(self, amnt: float) -> bool:
        if amnt > 0:
            self.__balance += amnt
            return True

        print(f"The amount should be positive number")
        return False

    def is_enough_money(self, amnt: float) -> bool:
        if amnt > self.__balance:
            return True

        return False

    def get_price_of_ride_accor_km(self, km: float):
        pass

    def ride(self, km: float, ride_date: datetime) -> bool:

        pass