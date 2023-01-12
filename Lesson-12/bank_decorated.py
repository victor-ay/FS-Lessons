import datetime


class Bank():

    def __init__(self):
        self._some_param = 1
        # self.working_days = [6, 0, 1, 2, 3]  # Sun - Thu ; Sun = 6, Thu = 3
        # self.working_hours = {'start': '09:00', 'end': '17:00'}

    @staticmethod
    # def working_hours_only(some_method):
    #     """
    #         Working hours: Sun - Thu, 09:00 - 17:00
    #     """
    #
    #     def wrapped_callable(*args, **kwargs):
    #         # working_days = [6, 0, 1, 2, 3]  # Sun - Thu ; Sun = 6, Thu = 3
    #         # working_hours = {'start': '09:00', 'end': '17:00'}
    #         working_days = args[0].working_days
    #         working_hours = args[0].working_hours
    #
    #         # Do before the <callable>
    #         ts_now = datetime.datetime.now()
    #         ts_weekday = ts_now.weekday()
    #         ts_time = ts_now.time()
    #
    #         if ts_weekday in working_days:
    #             if datetime.datetime.strptime(working_hours['start'], '%H:%M').time() <= ts_time <= datetime.datetime.strptime(working_hours['end'], '%H:%M').time():
    #                 results = some_method(*args, **kwargs)
    #                 return results
    #         print(f"Bank is closed now")
    #
    #     return wrapped_callable

    @staticmethod
    def working_hours_only(working_days, start_hour, end_hour):
        def wrapper(some_method):
            def decorator(*args, **kwargs):

                # Do something before the <some_method>
                ts_now = datetime.datetime.now()
                ts_weekday = ts_now.weekday()
                ts_time = ts_now.time()

                input_start_time = datetime.datetime.strptime(start_hour,"%H:%M").time()
                input_end_time = datetime.datetime.strptime(end_hour,"%H:%M").time()


                if ts_weekday in working_days:
                    if ts_time>input_start_time and input_end_time>ts_time:
                        results = some_method(*args, **kwargs)
                        return results

                print(f"Sorry pal, not your time")

                # Do something after <some_method> finishes to run


            return decorator
        return wrapper


    @working_hours_only(working_days = (6, 0, 1, 2, 3,4), start_hour = '07:30', end_hour = '20:20')
    def withdraw(self):
        print(f"Inside WITHDRAW")

    @working_hours_only(working_days = (6, 0, 1, 2, 3,4), start_hour = '08:30', end_hour = '17:20')
    def deposit(self):
        print(f"Inside DEPOSIT")

    def feedback(self):
        pass


if __name__ == '__main__':
    my_bank = Bank()
    # my_bank.withdraw(amnt=13)
    my_bank.withdraw()