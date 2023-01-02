class USDConverter:
    def __init__(self):
        self.currencies_usd_to = {} #consist 1 USD  = XX Currency
        self.currencies_usd_to['USD'] = 1

    def __str__(self):
        return f"USDConverter contains {len(self.currencies_usd_to)} currencies"


    def _is_currency_exist(self, currency_name:str) -> bool:
        if self.currencies_usd_to.get(currency_name):
            return True

        print(f"No such currency [{currency_name}] in the converter")
        return False

    def is_valid_amnt(self,amnt:float) -> bool:
        if amnt<0:
            print(f"The amount should be positive number. Your input: {amnt}")
            return False
        return True

    def show_all_rates(self, from_usd:bool):
        for curr in self.currencies_usd_to.keys():
            if from_usd:
                self.display_exch_rate('USD', curr)
            else:
                self.display_exch_rate(curr, 'USD')

    def add_exch_rate(self, cur:float, currency_name:str, usd:float = 1):
        self.currencies_usd_to[currency_name] = cur / usd

    def display_exch_rate(self,from_curr: str, to_curr:str):
        if not self._is_currency_exist(from_curr) or not self._is_currency_exist(to_curr):
            pass #printing in the is_currency_exist() method
        elif from_curr.upper()=='USD':
            print(f"1 USD = {self.currencies_usd_to.get(to_curr)} {to_curr}")
        else:
            print(f"1 {from_curr.upper()} = {1/self.currencies_usd_to.get(from_curr)} {to_curr.upper()}")

    def update_exch_rate(self,cur:float, currency_name:str, usd:float = 1) -> bool:
        if self._is_currency_exist(currency_name):
            self.add_exch_rate(cur,currency_name,usd)
            return True

        return False

    def delete_exch_rate(self,currency_name:str) -> bool:
        if self._is_currency_exist(currency_name):
            del self.currencies_usd_to[currency_name]
            print(f"Currency [{currency_name}] was successfully removed from the converter")
            return True

        return False

    def sell_usd(self,amnt:float ,currency_name:str) -> float:
        if not self.is_valid_amnt(amnt):
            return None

        if self._is_currency_exist(currency_name):
            return self.currencies_usd_to[currency_name]*amnt
        return None

    def buy_usd(self,amnt:float ,currency_name:str) -> float:
        if not self.is_valid_amnt(amnt):
            return None

        if self._is_currency_exist(currency_name):
            return amnt/self.currencies_usd_to[currency_name]
        return None

if __name__ == '__main__':
    my_converter = USDConverter()


    my_converter.add_exch_rate(3.16,'NIS')
    my_converter.add_exch_rate(113.73, 'JPY')
    my_converter.add_exch_rate(0.89, 'EUR')

    my_converter.display_exch_rate('JPY','USD')
    my_converter.display_exch_rate('USD','JPY')

    print(my_converter.buy_usd(30000,'JPY'))
    print(my_converter.sell_usd(134, 'EUR'))

    my_converter.delete_exch_rate('JPY')
    print(my_converter.buy_usd(3000,'EUR'))

    my_converter.show_all_rates(from_usd=False)


