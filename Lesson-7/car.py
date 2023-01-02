from pprint import pprint


class Car:
    def __init__(self, manufacturer: str, model :str, color: str,
                 fuel_consumption: float,
                 fuel_tank_capacity: float,
                 year: int = None):
        self.manufacturer: str = manufacturer
        self.model: str = model
        self.color: str = color
        self.km : int = 0
        self.fuel: float = 0
        self.fuel_consumption: float  = fuel_consumption
        self.fuel_tank_capacity: float = fuel_tank_capacity
        self.year: int = year
        self.maintenance = {}

    def __str__(self):
        return f"{self.manufacturer} | Model: {self.model} | Year: {self.year}"

    def display_dashboard(self):
        print(f"Dashboard for : {self.manufacturer} {self.model}")
        print(f"================================================\n"
              f"Fuel left: {self.fuel}\n"
              f"Km: {self.km}\n"
              f"================================================")

    def fill_tank(self,amnt: float) -> bool:
        if amnt<=0:
            print(f"Amount of fuel should be a positive number greater then zero")
            return False
        if self.fuel+amnt>self.fuel_tank_capacity:
            print(f"Cannot fill the requested amount of fuel: {amnt} liters\n"
                  f"The maximum possible amount to fill : {self.fuel_tank_capacity - self.fuel}")
            return False

        self.fuel+=amnt
        return True

    def drive(self, kms_driven:float) -> bool:
        if kms_driven<0:
            print(f"The driven kilometers should be a positive number. Your input is {kms_driven}")
            return False
        if kms_driven*(self.fuel_consumption/100)> self.fuel:
            print(f"The input of driven kilometers is incorrect: {kms_driven}\n"
                  f"The remaining fuel in the tank is enough for {self.fuel/(self.fuel_consumption/100)} km")
            return False

        self.km+=kms_driven
        self.fuel-=(self.fuel_consumption/100)*kms_driven
        return True

    def fill_to_full(self):
        self.fuel = self.fuel_tank_capacity

    def add_maintanance(self, date:str, description: str):
        m_list = self.maintenance.get(date,[])
        m_list.append(description)
        self.maintenance
        self.maintenance[date]=description

    def display_all_maintenance(self):
        pprint(self.maintenance)

    def get_all_maintanance(self):
        return self.maintenance