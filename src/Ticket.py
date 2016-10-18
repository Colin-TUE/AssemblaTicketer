from datetime import datetime

plan_levels = {0: "None", 1: "Subtask", 2: "Story", 3: "Epic"}
plan_levels_str = {v: k for k, v in plan_levels.items()}
statuses_str = {"New": 0, "In Progress": 1, "Test": 2, "Review": 3, "Done": 4}
statuses = {v: k for k, v in statuses_str.items()}


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
        self.__estimate = None
        self.__worked = None
        self.__completed = None
        self.__created = None
        self.__plan_level = None
        self.__status = None
        self.__due_date = None

    def to_string(self):
        """
        Function to convert this ticket to string
        :return: string representation of this ticket
        """
        return str(
            {
                'number'       : self.__number, 'estimate': self.__estimate,
                'worked'       : self.__worked, 'completed': self.__completed,
                'created'      : self.__created, 'plan_level_number': self.__plan_level,
                'status_number': self.__status, 'due_date': self.__due_date
            })

    # Getters

    def get_created(self):
        """
        Returns the creation date
        :return: datetime or None
        """
        return self.__created

    def get_completed(self):
        """
        Returns the completion date
        :return: datetime or None
        """
        return self.__completed

    def get_estimate(self):
        """
        Returns the estimation
        :return: floar ot None
        """
        return self.__estimate

    def get_due_date(self):
        """
        Returns the due date
        :return: date or None
        """
        return self.__due_date

    def get_number(self):
        """
        Returns the number of the ticket
        :return: number (integer)
        """
        return self.__number

    def get_worked(self):
        """
        Returns the amount of time reported as worked
        :return: float or None
        """
        return self.__worked

    def get_plan_level(self):
        """
        Returns the plan level identifier (see self.plan_levels for resoltion)
        :return: number (integer) or None
        """
        return self.__plan_level

    def get_status(self):
        """
        Returns the status (see self.statuses for resolution)
        :return: number (integer) or None
        """
        return self.__status

    # Setters

    def set_created(self, param):
        """
        Set the creation datetime of this object. If not valid format then set the creation time
        to None
        :param param: the value to set
        :return: none
        """
        try:
            time = datetime.strptime(param, "%Y-%m-%dT%H:%M:%S.000Z")
        except ValueError as e:
            time = None

        self.__created = time

    def set_completed(self, param):
        """
        Set the completion datetime of this object. If not valid format then set the
        completion time to None
        :param param: the value to set
        :return: none
        """
        if param is not None:
            try:
                time = datetime.strptime(param, "%Y-%m-%dT%H:%M:%S.000Z")
            except ValueError as e:
                time = None
        else:
            time = None

        self.__completed = time

    def set_estimate(self, param):
        """
        Sets the estimate for this ticket. If the the param is not a float then set the estimate
        to None
        :param param: The value to set
        :return: none
        """
        try:
            number = float(param)
        except ValueError as e:
            number = None

        self.__estimate = number

    def set_worked_hours(self, param):
        """
        Sets the worked hours for this ticket. If the the param is not a float then set the
        worked hours to None
        :param param: The value to set
        :return: none
        """
        try:
            number = float(param)
        except ValueError as e:
            number = None

        self.__worked = number

    def set_plan_level(self, param):
        """
        Sets the plan level of this ticket. If not a valid plan level then set it to None
        :param param: The value to set
        :return: none
        """
        if param in plan_levels.keys():
            planlvl = param
        else:
            planlvl = None

        self.__plan_level = planlvl

    def set_status(self, param):
        """
        Sets the status of this ticket. If not a valid status then set ti to None
        :param param: The value to set
        :return: none
        """
        if param in statuses_str.keys():
            status = statuses_str[param]
        else:
            status = None

        self.__status = status

    def set_due_date(self, param):
        """
        Set the due date of this ticket. If not valid format then set the completion
        time to None
        :param param: the value to set
        :return: none
        """
        if param is not None:
            try:
                time = datetime.strptime(param, "%Y-%m-%d").date()
            except ValueError as e:
                time = None
        else:
            time = None

        self.__due_date = time
