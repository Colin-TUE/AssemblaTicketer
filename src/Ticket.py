from datetime import datetime

class Ticket:
    """
    Class that represents a ticket and its relevant information for the Meter
    """

    def __init__(self, number):
        """
        Creates a ticket with a associated number
        :param number: The unique number within the space
        """
        self.__number = number
        self.__estimate = -1
        self.__worked = -1
        self.__completed = datetime.now()
        self.__created = datetime.now()

    def setCreated(self, param):
        time = None
        try:
            time = datetime.strptime(param, "%Y-%m-%dT%H:%M:%S.000Z")
        except ValueError as e:
            time = None


    def setCompelted(self, param):
        pass

    def setEstimate(self, param):
        pass

    def setWorkedHours(self, param):
        pass

    def setPlanLevel(self, param):
        pass

    def setStatus(self, param):
        pass

    def setDueDate(self, param):
        pass
