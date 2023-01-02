import datetime
from pprint import pprint

import pytz


class Table():
    def __init__(self, number_of_seats:int, id:int, time_limit:datetime.timedelta):
        self._number_of_seats: int = number_of_seats
        self._table_id: int = id
        self._time_limit = time_limit
        self._is_occupied: bool = False
        self._reservation_start_time = {} # {datetime: occupied_seats}
        self._table_location = {'Bar':False,
                                'Terrace': False,
                                'Indoors': False,
                                'Floor number': 0, #0- is default,Floor number = 0 is ground
                                'VIP_Room':False,
                                'Less_preferred_location': {
                                                            'Near_toilet': False,
                                                            'Near_exit': False,
                                                            'Near_kitchen': False
                                                            }
                                }
        self.__tz_israel = pytz.timezone('Asia/Jerusalem')

    def __str__(self):
        reserv_str = ''
        for res_time in self._reservation_start_time.keys():
            reserv_str+=f'Time: {res_time.strftime("%Y-%m-%d %H:%M")} | Guests: {self._reservation_start_time[res_time]}\n'

        return f"{reserv_str}"

    def is_avaliable_now(self)-> bool:
        return not self._is_occupied

    # def _is_positive_int_number(self, number:int) -> bool:
    #     '''
    #     Checks if number is greater than zero
    #     :param number: integer number
    #     :return: True if number is greater than zero. False otherwise.
    #     '''
    #     if number>0:
    #         return True
    #     return False



    def _has_enough_seats(self,number_of_guests : int) ->bool:
        '''
        Checks if the table has enough seats
        :param number_of_guests: number of guests
        :return: True if table has required number of seats. False otherwise
        '''
        if number_of_guests>self._number_of_seats:
            return False
        return True

    # def _is_time_reservation_correct(self,time_of_reservation:datetime)-> bool:
    #     '''
    #     Checks if desired time reservation is greater than time is now
    #     :param time_of_reservation:
    #     :return:
    #     '''
    #
    #     #Table Management class should check the list of reservation dates/times
    #     if time_of_reservation<datetime.datetime.now():
    #         return False
    #     return True
    #

    def reserve_a_table(self, number_of_guests : int, time_of_reservation:datetime) -> bool:
        '''
        Reserves a table for a number_of_guests
        :param number_of_guests: Number of guests
        :param time_of_reservation: Desired time to reserve the table
        :return: True if success False otherwise
        '''


        # Management sys will check if there is enough time to reserve the table according to max time occupation
        self._reservation_start_time[time_of_reservation] = number_of_guests

        #checking if reservation is for now and changing the occupation status
        # if abs(datetime.datetime.utcnow() - time_of_reservation)  < datetime.timedelta(minutes=1):
        #     self._is_occupied = True
        self._is_occupied = True

        return True

    def release_a_table_now(self, time_of_reservation:datetime)->bool:
        '''
        Releases the table for other guests
        :return:
        '''
        if self._reservation_start_time.get(time_of_reservation):
            self._is_occupied = False
            self._reservation_start_time.pop(time_of_reservation)
            return True

        return False

    def cancel_reservation(self,time_of_reservation:datetime)->bool:
        '''
        Cancel the reservation
        :param time_of_reservation: Start time for the reservation
        :return:
        '''
        if self._reservation_start_time.get(time_of_reservation):
            self._reservation_start_time.pop(time_of_reservation)
            return True

        return False

    def update_reservation(self, current_time_of_reservation:datetime,
                                new_number_of_guests : int, new_time_of_reservation:datetime):

        #Management level
            # Check if new reservation is possible
            # Check if old reservation exists

        self.cancel_reservation(current_time_of_reservation)
        self.reserve_a_table(number_of_guests=new_number_of_guests, time_of_reservation=new_time_of_reservation)

    def time_left(self):
        '''
        Getting minimal datetime element from dictionary. Calculating the remaining
        :return: t_left in
        '''

        if self._is_occupied:
            # print(f"{datetime.datetime.utcnow()}")
            t_left = self._time_limit- (datetime.datetime.utcnow()-min(self._reservation_start_time))
            return t_left
        return None

    def _find_closest_slot(self)->datetime:
        if len(self._reservation_start_time)==0:
            return datetime.datetime.utcnow()

        time_try = datetime.datetime.utcnow()
        for reservation in self._reservation_start_time.keys():
            if time_try<reservation and time_try+self._time_limit <=reservation:
                return time_try
            else:
                time_try = reservation+self._time_limit

        return time_try


class TableReservationSystem():
    def __init__(self,restaurant_name:'str', tables: [Table]):
        self.restaurant_name = restaurant_name
        self._time_limit_occupation:datetime.timedelta = datetime.timedelta(minutes=30, hours=1)
        self._tables = tables

        self._tables_ids = []
        for table in self._tables:
            self._tables_ids.append(table._table_id)


    def __str__(self):
        table_status = ''
        for table in self._tables:
            table_status += f'Table ID: {table._table_id}  | # of Seats : {table._number_of_seats}  |  is free : {not table._is_occupied}' \
                            f'| Reservations = {table._reservation_start_time}\n'
        return f"Restaurant < {self.restaurant_name} > has <{len(self._tables)}> tables: \n" \
               f"{table_status}"

    def _table_id_exist(self, table_num:int):
        if table_num in self._tables_ids:
            return True
        return False

    def _is_reservation_time_correct(self,reservation_time:datetime.datetime):
        '''
        Checking if reservation is in permited time range: NOW < reservation < NOW +100 days
        :param reservation_time:
        :return:
        '''
        if reservation_time< datetime.datetime.utcnow() or reservation_time> datetime.datetime.utcnow() + datetime.timedelta(days=100):
            return False
        return True

    @staticmethod
    def _is_time_inside_reserved(reserved_start:datetime.datetime, reserved_end:datetime.datetime , requested_time: datetime.datetime):
        '''
        Checks if requested datetime falls between reserved_start and reserved_end
        :param reserved_start:
        :param reserved_end:
        :param requested_time:
        :return: True if reserved_start<= requested <= reserved_end
        '''
        if reserved_start< requested_time and requested_time< reserved_end:
            return True
        return False

    def _is_reservation_of_table_possible(self, table:Table, reservation_time:datetime.datetime):
        # Check if possible to reserve
        #  There is no reservation from now+table_time_limit -> get minimum time
        if len(table._reservation_start_time) > 0:
            for reserved in table._reservation_start_time.keys():

                #Check if new reservation starts inside of previous reservation's time
                #   If there is reservation between 15:00 - 16:00 (with l_time_limit = 1 hr)
                #   The new reservation on 15:30 is impossible
                if self._is_time_inside_reserved(reserved_start=reserved,
                                                 reserved_end=reserved+table._time_limit,
                                                 requested_time=reservation_time):
                    return False

                #Check if new reservation ends inside of next
                #   If there is reservation between 15:00 - 16:00 (with l_time_limit = 1 hr)
                #   The new reservation on 14:30 is impossible
                if self._is_time_inside_reserved(reserved_start=reservation_time,
                                                 reserved_end=reservation_time+table._time_limit,
                                                 requested_time=reserved):
                    return False

        return True

    def _is_positive_int_number(self, number:int) -> bool:
        '''
        Checks if number is greater than zero
        :param number: integer number
        :return: True if number is greater than zero. False otherwise.
        '''
        if number>0:
            return True
        return False

    def get_soonest_available_tables(self, guests:int):

        soonest = [] #{table_id : soonest_datetime}
        for table in self._tables:
            if table._number_of_seats>=guests:
                soonest_datetime = table._find_closest_slot()
                soonest.append({table._table_id:soonest_datetime})

        val_list = []
        soonest_sort =[]
        for elem in soonest:
            val_list.append(list(elem.values())[0])
        print(f"-> {min(val_list)}")
        count = len(soonest)
        while count > 0:
            count -= 1
            min_index = val_list.index(min(val_list))
            soonest_sort.append(soonest[min_index])
            soonest.remove(soonest[min_index])
            val_list.remove(val_list[min_index])

        return soonest_sort

    def reserve_a_table(self, table_id:int, guests: int, reservation_time :datetime.datetime):

        #Check if table exist in the restaurant
        if not self._table_id_exist(table_num=table_id):
            print(f"Table with id # {table_id} does not exist")
            return False

        #Check if reservation time is correct
        # if not self._is_reservation_time_correct(reservation_time=reservation_time):
        #     print(f"The reservation time should be between NOW (utc) and up until +100 days from now")
        #     return False

        #Check if guest number is correct
        if not self._is_positive_int_number(number=guests):
            print(f"Number of Guest should be greater than zero")
            return False

        for table in self._tables:
            if table._table_id == table_id:

                #Check if table has enough seats
                if not table._has_enough_seats(guests):
                    print(f"Table id: [{table._table_id}] has not enough seats [{table._number_of_seats}]\n")
                    return False

                #Check if possible to reserve
                #  There is no reservation from now+table_time_limit -> get minimum time
                if not self._is_reservation_of_table_possible(table=table, reservation_time=reservation_time):
                    print(f"Table id: [{table._table_id}] not possible to reserve for [{reservation_time}]\n"
                          f"There is another reservation conflict\n"
                          f"The Time difference should be at least [{table._time_limit}]\n")
                    return False


                table.reserve_a_table(number_of_guests=guests,time_of_reservation=reservation_time)
                return True

    def release_a_table(self, table_id:int) -> bool:
        '''
        Releases the table immediately if it was occupied
        :param table_id:
        :return:
        '''

        #Check if table exist in the restaurant
        if not self._table_id_exist(table_num=table_id):
            print(f"Table with id # {table_id} does not exist")
            return False

        for table in self._tables:
            closest_reservation = min(table._reservation_start_time) #get closest reservation

            #Check if NOW is inside the closest_reservation
            if table._table_id == table_id and \
                    self._is_time_inside_reserved(reserved_start=closest_reservation ,
                    reserved_end=closest_reservation +table._time_limit,
                    requested_time=datetime.datetime.utcnow()):

                table.release_a_table_now(closest_reservation ) # releases the closest_reservation
                return True

        return False

    def get_tables_with_less_than_x_minutes_left(self, min_left:datetime.timedelta, guests:int):
        '''
        Returns list of table's ids that is possible to reserve in min_left time
        :param min_left: datetime.timedelta - time span to check reservation vacancy
        :param guests: Number of guests
        :return: List of table's ids (tables_less_than_x_minutes)
        '''
        tables_less_than_x_minutes = []
        for table in self._tables:
            if table._has_enough_seats(number_of_guests=guests):
                last_resrvation_ends_in = table.time_left()
                #checking if there are no additional reservation that clashes with desired one
                if self._is_reservation_of_table_possible(table,datetime.datetime.utcnow()+min_left):
                    if last_resrvation_ends_in==None or last_resrvation_ends_in<min_left:
                        tables_less_than_x_minutes.append(table._table_id)
        return tables_less_than_x_minutes

    def get_tables_time_limit(self):
        '''
        Returnt dictionary where key = table_id, value = table_time_limit
        :return: time_limits dictionary
        '''
        time_limits = {} #{table_id : datetime.timedelta}
        for table in self._tables:
            time_limits[table._table_id]=(table._time_limit)
        return time_limits

    def update_tables_time_limit(self, time_limits:{int:datetime.timedelta}) ->bool:
        '''
        Updating time limits of tables per table ids
        :param time_limits: dictionary of time limit changes per each table {table_id : new_time_limit}
        :return: True if everything ok
        '''

        for tab_id,new_time_limit in time_limits.items():
            if not self._table_id_exist(table_num=tab_id):
                return False

        for table in self._tables:
            if time_limits.get(table._table_id):
                table._time_limit=time_limits[table._table_id]
        return True

if __name__ == '__main__':
    # my_table = Table(4,12,datetime.timedelta(days=0,hours=1,minutes=0))
    # my_table.reserve_a_table(2,datetime.datetime.utcnow())
    # my_table.reserve_a_table(2, datetime.datetime.utcnow()+datetime.timedelta(minutes=20,hours=2))
    # my_table.reserve_a_table(2, datetime.datetime.utcnow())
    # my_table.reserve_a_table(2, datetime.datetime.utcnow())


    # print(my_table)

    #
    # t1= datetime.time(hour=2,minute=30)
    # t2 = datetime.time(hour=1,minute=15)
    #
    # print(f"Date -now utc = {datetime.datetime.utcnow()}")
    # print(my_table.reserve_a_table(2, datetime.datetime(2022, 12, 15, 13, 10)))
    # print(my_table.time_left())
    # print(my_table)



    t_limit_1 = datetime.timedelta(hours=1,minutes=0)
    tables = [Table(2,100,t_limit_1), Table(4,101,t_limit_1), Table(4,102,t_limit_1), Table(6,103,t_limit_1)]
    japanika_res = TableReservationSystem(restaurant_name='Japanika',tables=tables)


    japanika_res.reserve_a_table(table_id=100, guests=2, reservation_time=datetime.datetime(2022, 12, 17, 14, 33))
    japanika_res.reserve_a_table(table_id=101, guests=2, reservation_time=datetime.datetime(2022, 12, 17, 14, 40))
    japanika_res.reserve_a_table(table_id=102, guests=2, reservation_time=datetime.datetime(2022, 12, 17, 14, 50))

    t = japanika_res.get_tables_with_less_than_x_minutes_left(min_left=datetime.timedelta(minutes=40),guests=2)
    print(t)

    japanika_res.update_tables_time_limit(time_limits={131:datetime.timedelta(hours=2)})
    # print(japanika_res.get_soonest_available_tables(2))

    # print(japanika_res.get_soonest_available_tables(4))
    #
    # dic_l = [{'a': datetime.datetime(2022,12,17,10,50)},
    #          {'b': datetime.datetime(2022,12,17,8,50)},
    #          {'c': datetime.datetime(2022,12,17,11,50)}]
    #
    # di ={'a': datetime.datetime(2022,12,17,10,50),
    #      'b': datetime.datetime(2022,12,17,10,50),
    #      'c': datetime.datetime(2022,12,17,10,50)}
















