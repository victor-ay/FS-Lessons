import datetime
from pprint import pprint


class BankAccount():
    def __init__(self, bank_name:str, bank_branch:str, account_num: int,
                 account_holders:[{'id':int,
                                  'first_name': str,
                                   'last_name': str,
                                   'address': str}]):
        self.__bank_name = bank_name
        self.__bank_branch = bank_branch
        self.__account_number = account_num
        self.__account_holders = account_holders

        self.__isUSDallowed = True
        self.__balance = {'NIS':0, 'USD':0}
        self.__credit_limit = {'NIS':-1000, 'USD':0}
        self.__transactions = {}
        self.__usdTOnis = 3.52
            # {'date': [
            #           {
            #               'transaction' : 'deposit / withdraw / conversion',
            #               'amount' : float,
            #               'currency': 'NIS / USD'
            #            }
            #          ]}

    def __str__(self):
        return f"Bank Account: \n" \
               f"\t >> Bank name: {self.__bank_name}\n" \
               f"\t >> Bank branch: {self.__bank_branch}\n" \
               f"\t >> Account: {self.__account_number}\n" \
               f"\t >> Balans: \n" \
               f"\t\t\t{self.__balance['NIS']} [NIS]\n" \
               f"\t\t\t{self.__balance['USD']} [USD]\n" \
               f"\t >> Account holders:\n" \
               f"\t\t\t{self.__account_holders}"

    def _hasUSDaccount(self) -> bool:
        '''
        Checking if the account has USD account as well
        :return:
        '''
        if self.__isUSDallowed:
            return True
        return False

    @staticmethod
    #Not using self inside the method  -> it's static
    def _is_corect_amount_of_money(amnt:float) -> bool:
        '''
        Checking if inserted amount of money is positive number
        :param amnt:
        :return:
        '''
        if amnt<=0:
            print(f"The inserted amount should be positive number")
            return False
        return True

    def deposit(self,amnt:float, inShekel = True, date:datetime = datetime.datetime.now().date()) -> bool:
        #check if amnt is correct
        #check if has USD account, if inShekel = False
        if self._is_corect_amount_of_money(amnt) :
            if inShekel:

                # if not exist any data about transaction on this date -> create empty list
                self._initialize_transaction_date(date=date)

                # update transaction data
                self.__transactions[date].append(
                    {'transaction':'deposit',
                     'amount':amnt,
                     'currency': 'NIS'}
                )

                #update NIS balance
                self.__balance['NIS']+=amnt

                return True

            #if mony deposition is in USD
            elif self._hasUSDaccount():
                self._initialize_transaction_date(date=date)
                self.__transactions[date].append(
                    {'transaction':'deposit',
                     'amount':amnt,
                     'currency': 'USD'}
                )
                #update USD balance
                self.__balance['USD']+=amnt
                return True

        return False

    def _is_enough_to_withdraw(self,amnt:float, inShekel = True) -> bool:
        '''
        Returns True if success, False + message if not
        :param amnt: Requested amount of money to withdraw
        :param inShekel: Requested currency. NIS is default, option for USD
        :return: boolean
        '''
        if inShekel:
            balance_nis = self.get_current_balance()['NIS']
            if balance_nis>=amnt:
                return True

            #comes here if there is not enough money on the NIS balance
            print(f">>Your balance is low.\n"
                  f">>Sorry, your NIS [₪ {balance_nis}] balance is lower than requested amount [₪ {amnt}]\n")
            return False
        else: #no need it, but it fixes the mind
            # The section for the USD account
            balance_usd = self.get_current_balance()['USD']
            if balance_usd >= amnt:
                return True

            # comes here if there is not enough money on the USD balance
            print(f">>Your balance is low.\n"
                  f">>Sorry, your USD [$ {balance_usd}] balance is lower than requested amount [$ {amnt}]\n")
            return False

    def _initialize_transaction_date(self, date:datetime):
        if not self.__transactions.get(date):
            self.__transactions[date] = []

    def withdraw(self,amnt:float, inShekel = True, date:datetime = datetime.datetime.now().date()):
        #Check the fllowing:
        #   is enough money
        #   is correct number

        if self._is_corect_amount_of_money(amnt) and self._is_enough_to_withdraw(amnt=amnt,inShekel=inShekel):
            if inShekel:
                # if not exist any data about transaction on this date -> create empty list
                self._initialize_transaction_date(date=date)
                # update transaction data
                self.__transactions[date].append(
                    {'transaction':'withdraw',
                     'amount':amnt,
                     'currency': 'NIS'}
                )

                #update NIS balance
                self.__balance['NIS']-=amnt
                return True

            elif self._hasUSDaccount()  and self._is_enough_to_withdraw(amnt=amnt,inShekel=inShekel):
                self._initialize_transaction_date(date=date)
                self.__transactions[date].append(
                    {'transaction':'withdraw',
                     'amount':amnt,
                     'currency': 'USD'}
                )
                #update USD balance
                self.__balance['USD']-=amnt
                return True

        return False

    def convert(self,amnt:float,  buyUSD = True, date:datetime = datetime.datetime.now().date())-> bool:
        '''

        :param amnt: Amnt of money to be converted
        :param buyUSD: True   - if one wants to buy USD on the amnt of NIS
                       False  - if one wants to buy NIS on the amnt of USD
        :return:
        '''

        #if buy USD ->
        #              * check if enough NIS for amount of USD
        #              * check if enough there is an USD account
        #              * change balance
        #              * change add Convert transaction
        if self._is_corect_amount_of_money(amnt):
            if not self.__isUSDallowed:
                print(f">> You can't make conversions on your account since you dont have a USD account.\n"
                      f">> Please contact bank to open the USD account for a such operation.")
                return False

            if buyUSD and self._is_enough_to_withdraw(amnt=amnt,inShekel=True):

                self.__balance['NIS']-=amnt
                self.__balance['USD']+=amnt/self.__usdTOnis
                self._initialize_transaction_date(date=date)
                self.__transactions[date].append(
                    {'transaction':'conversion',
                     'amount':amnt,
                     'currency_bought': 'USD'}
                )
                return True

            elif buyUSD==False and self._is_enough_to_withdraw(amnt=amnt,inShekel=False):
                self.__balance['USD']-=amnt
                self.__balance['NIS']+=amnt*self.__usdTOnis
                self._initialize_transaction_date(date=date)
                self.__transactions[date].append(
                    {'transaction':'conversion',
                     'amount':amnt,
                     'currency_bought': 'NIS'}
                )
                return True

        return False


    def get_current_balance(self):
        '''

        :return: Dictionary of balance {'NIS':-1000, 'USD':0}
        '''
        return self.__balance

    def get_transactions_on_date(self,date:str):
        '''

        :param date: string in format 'YYYY-MM-DD'
        :return:
        '''
        if self.__transactions.get(date):
            return self.__transactions.get(date)
        else:
            print(f"No transaction on a day : {date}\n"
            f"Make sure you inserted date as a following format: [YYYY-MM-DD]\n")
            return None

    def get_cash_flow_month(self, month:int, last_requested_month=True):
        '''

        :param month: integer between 0 and 12
        :param month: if True -> will return only last month.
                         False -> will go over all years and will extract transaction data from all <month> that match
        :return: dictionary {'YYYY-<month>-DD' : <transactions data>} or empty dictionary if nothing found
        '''

        #check if input is correct ->
        if 0>month or month>12:
            print(">> The requested month is wrong.\n"
                  ">> You should choose positive number between 1 and 12 included\n")
            return None

        #creating temporary transaction dictionary
        months_transaction = {}

        #will return only the last month
        for key,value in self.__transactions.items():

            #isolating according the month number

            if key.month==month:
                # if month of the current year requested
                if last_requested_month & key.year==datetime.datetime.now().year:
                    months_transaction[key] = value
                    return months_transaction
                else:
                    #all months in any year
                    months_transaction[key] = value

        # if requested all transactions in all months that match
        return months_transaction

    def get_cash_flow_year(self, year:int):
        if 1910 > year or year> int(datetime.datetime.now().year):
            print(">> The requested year is wrong.\n"
                  f">> You should choose positive number between [1910] and current year [{datetime.datetime.now().year}]\n")
            return None

        #creating temporary transaction dictionary
        year_transaction = {}

        #will return only the last month
        for key,value in self.__transactions.items():
            #isolating according the month number
            if key.year==year:
                year_transaction[key] = value

        # if requested all transactions in all months that match
        return year_transaction


if __name__ == '__main__':
    my_account = BankAccount('Discount','320',123456,
                             [{'id': 111,
                               'first_name':'Viclor',
                               'last_name': 'Aynbinder',
                               'address': 'Netanya'}])
    my_account.deposit(amnt=300)
    my_account.deposit(amnt=100)
    my_account.withdraw(amnt=25)
    my_account.deposit(amnt=75, inShekel=False)
    my_account.withdraw(amnt=25, inShekel=False)
    my_account.convert(amnt=25,buyUSD=True,date = datetime.datetime.now().date())
    # my_account.deposit(amnt=100,inShekel=False,date=datetime.datetime.now().date())

    # print(my_account.get_current_balance())
    # print(my_account)
    #
    # d_date = '2022-12-11'
    # pprint(f"Getting transaction on date [{d_date}]:\n"
    #        f">> {my_account.get_transactions_on_date(d_date)}")

    pprint(my_account.get_cash_flow_month(12))
    pprint(my_account.get_cash_flow_year(2022))

    # a = {'1':11, '2':22}
    # for k,v in a.items():
    #     print(f"k = {k}")
