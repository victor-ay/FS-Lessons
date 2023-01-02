import datetime
import os
import pickle
from nis import match
from pprint import pprint

import bus_exception


class ScheduledRide:
    def __init__(self, ride_id:int, origin_time: datetime.time, destination_time: datetime.time, driver_name:str):
        self._origin_time = origin_time
        self._destination_time = destination_time
        self._driver_name = driver_name
        self._delays = 0
        self._ride_id = ride_id


    def __str__(self):
        return f"ID: {self._ride_id} | Times: {self._origin_time}-{self._destination_time} | Driver: {self._driver_name} | Delays : {self._delays}"

    def report_delay(self):
        self._delays+=1

    def get_ride_id(self):
        return self._ride_id

    def get_ride_generic_info(self):
        general_ride_info = {
            'Time at origin':self._origin_time,
            'Time at destination':self._destination_time,
            'Ride ID':self._ride_id,
            'Delays': self._delays
        }
        return general_ride_info


###########################
class BusRout:
    def __init__(self, line_num:str, origin:str,destination:str, stops:[str]):
        self._line_num = line_num
        self._origin = origin
        self._destination = destination
        self._stops = stops
        self._rides :[ScheduledRide] = []


    def __str__(self):
        return f"Route: {self._line_num} |  {self._origin} -> {self._destination} | Stops: {self._stops}"

    def add_route(self,line_num:str, origin:str,destination:str,stops:[str]):
        self._line_num = line_num
        self._origin = origin
        self._destination = destination
        self._stops = stops

    def update_route(self,line_num:str, origin:str=None,destination:str=None,stops:[str]=None):
        if origin:
            self._origin = origin
        if destination:
            self._destination = destination
        if stops:
            self._stops = stops

    def get_scheduled_rides(self):
        return self._rides

    def add_scheduled_ride(self, new_ride:ScheduledRide):
        self._rides.append(new_ride)

    def report_delay(self,ride_id:int):
        for ride in self._rides:
            if ride.get_ride_id() == ride_id:
                ride.report_delay()

    def get_route_info_without_rides(self):
        rides_info = []
        searched_rides = self.get_scheduled_rides()
        for ride in searched_rides:
            rides_info.append(ride.get_ride_generic_info())
        route_info = {
            'Line number' : self._line_num,
            'Origin': self._origin,
            'Destination': self._destination,
            'Stops': self._stops,
            'Rides':rides_info
        }
        return route_info



###########################
class BestBusCompany:
    def __init__(self):
        self._bus_routs: dict[str, BusRout] = {} #{line_num : BusRout}
        self._name = 'BestBusCompany inc.'
        self._last_ride_id = 0
        self._rides_lines :dict [int,str]={} # {ride_id : line_num}

    def __str__(self):
        ex_str = ''
        for i, rout in enumerate(self._bus_routs):
            ex_str += f"[{i}] {self._bus_routs[rout]}\n"
        return ex_str

    def generate_next_ride_id(self):
        self._last_ride_id+=1

    def ad_rout(self,line_num:str, origin:str,destination:str,stops:[str]):
        self._bus_routs[line_num] = BusRout(line_num=line_num,origin=origin,destination=destination,stops=stops)

    def delete_route(self,line_num:str):
        self._bus_routs.pop(line_num)

    def update_route(self,line_num:str, origin:str=None,destination:str=None,stops:[str]=None):
        self._bus_routs[line_num].update_route(line_num, origin,destination,stops)

    def add_scheduled_ride(self, line_num:str,origin_time: datetime.time, destination_time: datetime.time, driver_name:str):
        current_bus_rout = self._bus_routs[line_num]
        self.generate_next_ride_id()
        new_ride = ScheduledRide(ride_id=self._last_ride_id,origin_time=origin_time,destination_time=destination_time,driver_name=driver_name)
        self._rides_lines[self._last_ride_id]=line_num
        current_bus_rout.add_scheduled_ride(new_ride)

    def get_rides_vs_bus_lines(self):
        return self._rides_lines

    def validate_line_num_exist(self,line_num:str):
        if not line_num in self._bus_routs:
            raise bus_exception.WrongInput(msg=f'Line [{line_num}] does not exist')

    def validate_line_num_not_exist(self,line_num:str):
        if line_num in self._bus_routs:
            raise bus_exception.WrongInput(msg=f'Line [{line_num}] exist')

    def get_route_info_for_passenger(self, line_num:str):
        self.validate_line_num_exist(line_num=line_num)
        line_info = self._bus_routs[line_num].get_route_info_without_rides()
        return line_info

    def get_bus_lines_going_through_place(self, searched_place:str, key:str):
        '''
        Returns set of bus line numbers that are mentioned (searched_place) in the (key) of rout dictionary
        :param searched_place:
        :param key:
        :return:
        '''
        line_num_set = set()
        for line_num, route in self._bus_routs.items():
            if (searched_place in route.get_route_info_without_rides()[key]):
                line_num_set.add(line_num)
        return line_num_set

    def search_route(self, line_num:str = None, origin: str = None, destination: str =None, bus_stop: str = None):
        '''
        Searches information according to the one of the parameters. If more than one provided - will return
        result according the order.
        :param line_num:
        :param origin:
        :param destination:
        :param bus_stop:
        :return: searched_routes - > list of results that matches search params
        '''

        #Searching for relevant bus line numbers to return list of relevant info
        line_num_set =()
        searched_routes = []

        if line_num:
            searched_routes.append(self.get_route_info_for_passenger(line_num=line_num))
            return searched_routes

        elif origin:
            line_num_set = self.get_bus_lines_going_through_place(searched_place=origin,key='Origin')
        elif destination:
            line_num_set = self.get_bus_lines_going_through_place(searched_place=destination,key='Destination')
        elif bus_stop:
            line_num_set = self.get_bus_lines_going_through_place(searched_place=bus_stop,key='Stops')


        for line in line_num_set:
            searched_routes.append(self.get_route_info_for_passenger(line_num=line))

        return searched_routes

    def get_list_of_all_bus_lines(self) -> [str]:
        '''
        Returns list of bus numbers
        :return:
        '''
        return list(self._bus_routs.keys())

###########################
class BBCmenu:
    def __init__(self):
        self._user_type = None

    def get_user_type(self):
        return self._user_type

class MainMenu(BBCmenu):
    def __init__(self):
        super().__init__()
        # self._user_type = self.get_user_type()
        self.__manager_password = 'RideWithUs!'
        self.__is_logedin = False
        self._first_level_menu_choice = None


    def __str__(self):
        return f"**********************************\n" \
               f"Welcome to Best-Bus-Company\n" \
               f"**********************************\n"

    def get_user_type(self):
        return self._user_type

    def is_user_manager(self):
        if self._user_type == 'manager':
            return True
        else:
            return False

    def verify_is_manager_or_passenger(self, user_input:str):
        if user_input.lower() != 'm' and user_input.lower() != 'p':
            raise bus_exception.WrongInput(f"You should input 'm' or 'p'. Your input was [{user_input}]")
        elif user_input.lower() == 'm':
            self._user_type = 'manager'
        else:
            self._user_type = 'passenger'

    def verify_managers_password(self,inputed_pass:str):
        if self.__manager_password != inputed_pass:
            raise bus_exception.WrongPassword(f"Ooops, wrong pasword.")

    def verify_manager_is_logged_in(self):
        if not self.__is_logedin:
            raise bus_exception.NotLogedInAsManager

    def password_ask_menu(self):
        if self._user_type == 'manager':
            for i in range(3, 0, -1):
                try:
                    pass_input = input(f"Please input password:\n"
                                       f"\t\t>> ")
                    main_menu.verify_managers_password(inputed_pass=pass_input)

                    print(f"Password accepted")
                    self.__is_logedin = True
                    break
                except bus_exception.WrongPassword as e:
                    print(e)
                    if i > 1:
                        print(f"[{i - 1}] tries left.\n")
                    else:
                        print(f"Bad day... You reached your maximum number of tries.\n"
                              f"The program will exit here. See you!")
                        exit(1)

    def verify_input_first_level(self,user_input:str):
        if user_input not in self._first_level_menu_choice:
            raise bus_exception.WrongInput(f"!!! Wrong input [{user_input}]\n"
                                           f"    Your input should be one of these {self._first_level_menu_choice}.")

class ManagerMenu(MainMenu):
    def __init__(self):
        super().__init__()
        self._first_level_menu_choice = ['1','2','3','4']
        self._update_level_menu_choice = ['1', '2', '3']

    def __str__(self):
        menu_msg = f"\n\n" \
                   f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n" \
                   f"You are inside MANAGER'S menu\n" \
                   f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n" \
                   f"Following actions avaliable for you:\n" \
                   f"\t[1] Add new route\n" \
                   f"\t[2] Delete route\n" \
                   f"\t[3] Update route\n" \
                   f"\t[4] Add scheduled ride\n" \
                   f"-----------------------\n" \
                   f"\t[0] To finish"
        return menu_msg

    def second_menu_level(self,user_input:str, bbc:BestBusCompany):
        match user_input:
            case '1':
                new_route = self.add_route(bbc=bbc)
                print(f"New line [{new_route}] was added:\n")
            case '2':
                self.delete_route(bbc=bbc)
            case '3':
                self.update_route(bbc=bbc)
            case '4':
                self.add_scheduled_ride(bbc=bbc)

    def add_route(self, bbc:BestBusCompany):
        all_lines = bbc.get_list_of_all_bus_lines()

        #getting new line number
        while True:
            try:
                new_line = input(f"Insert new line number.\n"
                                 f"List of all current lines : {all_lines}\n"
                                 f"\t\t>>")

                #checking if line exists already
                bbc.validate_line_num_not_exist(line_num=new_line)
                break
            except bus_exception.WrongInput as e:
                print(e)


        #getting origin and destination
        while True:
            new_origin = input(f"Insert Origin.\n"
                                  f"\t\t>>")
            try:
                new_destination = input(f"Insert Destination.\n"
                                      f"\t\t>>")
                if new_origin == new_destination:
                    raise bus_exception.WrongInput(f"!!! Origin and Destination should be different")
                break
            except bus_exception.WrongInput as e:
                print(e)




        #getting new stops
        while True:
            new_stop =  input(f"Insert stops seperated by coma(,).\n"
                         f"\t\t>>")

            #Removing case sensetivity -> spliting -> removing spaces
            new_list_of_stops = list(map(str.strip,new_stop.lower().split(',')))

            #checking if there are duplicates in stops
            if len(new_list_of_stops)!=len(set(new_list_of_stops)):
                raise bus_exception.WrongInput(f"!!! Duplication of stops is not allowed.")

            #capitalizing stops
            new_list_of_stops = list(map(str.capitalize,new_list_of_stops))
            break



        #creating new route
        bbc.ad_rout(new_line,origin=new_origin,destination=new_destination,stops=new_list_of_stops)

        return new_line

    def delete_route(self, bbc:BestBusCompany):
        inputed_line_num = input(f"Insert the line you wish to delete:\n"
                                 f"List of all current lines : {bbc.get_list_of_all_bus_lines()}\n"
                                 f"\t\t>>")
        bbc.validate_line_num_exist(inputed_line_num)

        user_input = input(f"Are you sure you want to delete line [{inputed_line_num}]? (y/n)\n"
                           f"\t\t>>")
        if user_input.lower()!='y' and user_input.lower()!='n':
            raise bus_exception.WrongInput(msg = f"!!! Expected input (y/n)")
        elif user_input.lower()=='n':
            print(f"Deleting line [{inputed_line_num}] was aborted.")
        else:
            bbc.delete_route(inputed_line_num)
            print(f"Line [{inputed_line_num}] successfully deleted.")

    def verify_update_route_choice(self,user_input:str):
        if user_input not in self._update_level_menu_choice:
            raise bus_exception.WrongInput(f"!!! Wrong input [{user_input}]\n"
                                           f"    Your input should be one of thees {self._first_level_menu_choice}.")

    def update_route(self,bbc= BestBusCompany):
        inputed_line_num = input(f"Insert the line you wish to update:\n"
                                 f"List of all current lines : {bbc.get_list_of_all_bus_lines()}\n"
                                 f"\t\t>>")
        bbc.validate_line_num_exist(inputed_line_num)
        menu_update = f"\n\n" \
                   f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n" \
                   f"What would you like to update?\n" \
                   f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n" \
                   f"Following actions avaliable for you:\n" \
                   f"\t[1] Origin\n" \
                   f"\t[2] Destination\n" \
                   f"\t[3] Stops\n"
        user_input = input(f"{menu_update}\n"
                           f"\t\t>>")
        self.verify_update_route_choice(user_input=user_input)

        if user_input=='1':
            bbc.update_route(line_num=inputed_line_num,origin=user_input)
        elif user_input=='2':
            bbc.update_route(line_num=inputed_line_num,destination=user_input)
        else:
            stops_list = list(map(str.strip,user_input.lower().split()))
            stops_list = list(map(str.strip,stops_list))
            bbc.update_route(line_num=inputed_line_num,
                             stops=stops_list)#splitin



    def validate_correct_time(self,inserted_time:str):
        time_splited = inserted_time.split(':')
        if len(time_splited)==2 and time_splited[0].isnumeric() and time_splited[1].isnumeric() and\
            float(time_splited[0]) % int(time_splited[0]) == 0 and float(time_splited[1]) % int(time_splited[1]) == 0:
                t_splited_0 = int(time_splited[0])
                t_splited_1 = int(time_splited[1])
                if t_splited_0<24 and t_splited_0>0 and t_splited_1<60 and t_splited_1>0:
                    if not datetime.datetime.strptime(inserted_time,"%H:%M"):
                        pass #then everything is OK

        else:
            raise bus_exception.WrongInput(f"!!! Wrong time input [{inserted_time}] .\n"
                                           f"    Should be in format [HH:MM]\n")

    def validate_destination_origin_time_consistency(self,origin_time:str,destination_time:str):
        if datetime.datetime.strptime(origin_time,"%H:%M") > datetime.datetime.strptime(destination_time,"%H:%M"):
            raise bus_exception.WrongInput(f"!!! Destination and Origin times are not consistent")

    def add_scheduled_ride(self,bbc= BestBusCompany):
        while True:
            inputed_line_num = input(f"Insert the line you wish to update:\n"
                                     f"List of all current lines : {bbc.get_list_of_all_bus_lines()}\n"
                                     f"\t\t>>")
            bbc.validate_line_num_exist(inputed_line_num)


            while True:
                try:
                    inputed_origin_time = input(f"Origin time [HH:MM]:\n"
                                             f"\t\t>>")
                    self.validate_correct_time(inputed_origin_time)
                    break
                except bus_exception.WrongInput as e:
                    print(e)

            while True:
                try:
                    inputed_destination_time = input(f"Destination time [HH:MM]:\n"
                                             f"\t\t>>")
                    self.validate_correct_time(inputed_destination_time)
                    self.validate_destination_origin_time_consistency(origin_time=inputed_origin_time, destination_time=inputed_destination_time)
                    break
                except bus_exception.WrongInput as e:
                    print(e)

            inputed_driver_name = input(f"Driver Name:\n"
                                        f"\t\t>>")
            break

        bbc.add_scheduled_ride(line_num=inputed_line_num,origin_time=inputed_origin_time,
                               destination_time=inputed_destination_time,driver_name=inputed_driver_name)
        print(f"Added new ride for the line [{inputed_line_num}].")



    # def verify_manager_input_first_level(self,user_input:str):
    #     if user_input not in self._first_level_menu_choice:
    #         raise bus_exception.WrongInput(f"Wrong input [{user_input}]\n"
    #                                        f"Your input should be one of thees {self._first_level_menu_choice}.")

class PassengerMenu(MainMenu):
    def __init__(self):
        super().__init__()
        self._first_level_menu_choice = ['1', '2']
        self._search_level_menu_choice = ['1','2','3','4']

    def __str__(self):
        menu_msg = f"\n\n" \
                   f"^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n" \
                   f"You are inside PASSENGER'S menu\n" \
                   f"^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n" \
                   f"Following actions avaliable for you:\n" \
                   f"\t[1] Search route\n" \
                   f"\t[2] Report delay\n" \
                   f"-----------------------\n" \
                   f"\t[0] To finish"
        return menu_msg

    def second_menu_level(self,user_input:str,bbc:BestBusCompany):
        match user_input:
            case '1':
                search_results = self.search_route()
                if len(search_results)==0:
                    print(f"No results found according your search. Sorry.\n")
                for res in search_results:
                    self._print_searched_result(res)

            case '2':
                self.report_delay(bbc=bbc)

    def _print_searched_result(self,searched_result:dict):
        for key, value in searched_result.items():
            if isinstance(value,list):
                #Stops & Rides should be inside the For loop
                print(f"\t> {key}:")
                # print(f"{key}:", end='')
                for l_val in value:
                    if not isinstance(l_val,list) and not isinstance(l_val,dict): # it means stops
                        # Each stpop will be printed here
                        print(f"\t\t>> {l_val}")
                        # print(f"| {l_val}", end='')
                    else:
                        #it should be a list of dictionaries (rides)
                        for k_2, v_2 in l_val.items():
                            #inside each ride which is dictionary
                            if isinstance(v_2,datetime.time):
                                print(f"\t\t>> {k_2}: {v_2.strftime('%H:%M')}")
                                # print(f"| {v_2.strftime('%H:%M')}", end='')
                            else:
                                print(f"\t\t>> {k_2}: {v_2}")
                                # print(f"| {v_2}", end='')
                    if key == 'Rides':
                        print(f"\t\t  --------------------------")
            else:
                #Line number, Origin, Destination will be printed here
                print(f"\t> {key}: {value}")
                # print(f"| {value}", end='')

        print(f"")

    def _validate_inputed_as_menu(self,inputed_choice:str):
        if not inputed_choice in self._search_level_menu_choice:
            raise bus_exception.WrongInput(f"!!! The input should be according to menu numbers. Your input [{inputed_choice}]\n")

    def search_route(self):

        while True:
            try:
                search_by = input(f"How do you like to search the line rote?.\n"
                                 f"Search by:\n"
                                 f"\t[1] Line number\n"
                                 f"\t[2] Origin\n"
                                 f"\t[3] Destination\n"
                                 f"\t[4] Stop\n\n"
                                 f"\t>>")
                self._validate_inputed_as_menu(inputed_choice=search_by)
                break

            except bus_exception.WrongInput as e:
                print(e)

        search_text = input(f"\nWhat to search for?.\n"
                            f"\t>>")

        match search_by:
            case '1': #by line_num
                searched_results = bbc.search_route(line_num=search_text)
            case '2':
                searched_results = bbc.search_route(origin=search_text)
            case '3':
                searched_results = bbc.search_route(destination=search_text)
            case '4':
                searched_results = bbc.search_route(bus_stop=search_text)

        list_of_results =[]
        for result in searched_results:
            list_of_results.append(result)
            # self._print_searched_result(result)
        return list_of_results

    def _validate_ride_id_exist(self,check_id :int, bbc:BestBusCompany):
        if not (check_id in bbc.get_rides_vs_bus_lines()):
            raise bus_exception.WrongInput(f"!!! There is no such ride ID [{check_id}]")

    def _validate_input_is_int(self,inputed_text:str):
        if not (inputed_text.isnumeric() or float(inputed_text)%int(inputed_text)==0):
            raise bus_exception.WrongInput(f"Input should be integer, yours [{inputed_text}]")

    def report_delay(self, bbc:BestBusCompany):
        print(f"To report about the delay, you should insert the ride ID."
              f"Let's search for the right ride ID.")
        all_routs = self.search_route() #getting list of routs
        print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n" 
              f"Find the relevant Ride ID from the printed results\n" \
              f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n")
        for res in all_routs:
            self._print_searched_result(searched_result=res)
        inputed_id = input(f"\nTo report the delay , please insert ID:\n"
                           f"\t>> ")

        self._validate_input_is_int(inputed_id)
        self._validate_ride_id_exist(int(inputed_id),bbc=bbc)

        rides_vs_lines = bbc.get_rides_vs_bus_lines()

        current_bus_line = rides_vs_lines[int(inputed_id)]
        current_bus_rout = bbc._bus_routs[current_bus_line]

        current_bus_rout.report_delay(int(inputed_id))
        print(f"Delay reported.\n"
              f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")



###########################

if __name__ == '__main__':

    main_menu = MainMenu()
    print(main_menu)

    while True:
        try:
            user_type = input(f"Please input:\n"
                              f"\t\t[m] : for manager\n"
                              f"\t\t[p] : for passenger\n"
                              f"\t\t>>")
            main_menu.verify_is_manager_or_passenger(user_input=user_type)
            break
        except bus_exception.WrongInput as e:
            print(f"!!!!!!!!!!!!!!!!!!!\n"
                  f"{e}\n"
                  f"!!!!!!!!!!!!!!!!!!!\n")

    #Valid for managers only
    main_menu.password_ask_menu()

    if main_menu.is_user_manager():
        user_menu = ManagerMenu()
    else:
        user_menu = PassengerMenu()


    # check whether this is the first time you run the app
    # if this is the first time - create a new class
    if not os.path.exists('bus_company.pickle'):
        bbc = BestBusCompany()
    else:
        # this is not the first time - we already have a DB
        # with data from the previous runs
        with open('bus_company.pickle', 'rb') as fh:
            bbc = pickle.load(fh)

    # bbc = BestBusCompany()
    # bbc.ad_rout('605','Netanya','Tel-Aviv',['Shefaim','Herzelia'])
    # bbc.ad_rout('950', 'Netanya', 'Jerusalem', ['Sharon junction', 'Kfar Saba', 'Raanana'])
    # bbc.ad_rout('947', 'Netanya', 'Haifa', ['Havazelet junction', 'Olga juncton', 'Atlit'])
    #
    # bbc.add_scheduled_ride('605',datetime.time(hour=9,minute=30),datetime.time(hour=10,minute=30),driver_name='Moshe Kuku')
    # bbc.add_scheduled_ride('605',datetime.time(hour=10,minute=30),datetime.time(hour=11,minute=30),driver_name='Moshe Kuku')
    # bbc.add_scheduled_ride('605', datetime.time(hour=11, minute=30), datetime.time(hour=12, minute=30),
    #                        driver_name='Gever Gever')
    # bbc.add_scheduled_ride('605', datetime.time(hour=12, minute=30), datetime.time(hour=13, minute=30),
    #                        driver_name='Gever Gever')
    run_program = True
    while run_program:
        print(user_menu)

        try:
            user_input = input(f"\t>>")
            if user_input=='0':
                print(f"Program will exit here")
                run_program = False
            else:
                user_menu.verify_input_first_level(user_input)
                user_menu.second_menu_level(user_input, bbc=bbc)

        except bus_exception.WrongInput as e:
            print(e)

    # before exiting the program, persist the current state
    # of te system in the file, so next time it will be loaded
    with open('bus_company.pickle', 'wb') as fh:
        pickle.dump(bbc, fh)
