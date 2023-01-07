class BusException(Exception):
    def __init__(self,msg):
        super().__init__(msg)


class BusLineError(BusException):
    def __init__(self,msg):
        super().__init__(msg)


class WrongInput(Exception):
    def __init__(self,msg):
        super().__init__(msg)


class WrongPassword(Exception):
    def __init__(self,msg):
        super().__init__(msg)


class NotLogedInAsManager(Exception):
    def __init__(self,msg):
        super().__init__(msg)
