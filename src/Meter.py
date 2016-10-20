import datetime
import Ticket

result_key = "res"
count_key = "count"
empty_result = {result_key: 0, count_key: 0}


class Meter:
    def __init__(self, tickets):
        if len(tickets) == 0:
            raise ValueError("Tickets is empty")

        self.__current_time = datetime.datetime.now()
        self.__tickets = tickets

    def closed_tickets_cycle_time(self):
        """
        Compute the cycle time of closed tickets
        :return:
        """
        # get the list with only closed tickets
        closed_tickets = [t for t in self.__tickets if
            t.get_status() == Ticket.statuses_str["Done"] and
            t.get_plan_level() <= Ticket.plan_levels_str["Story"] and
            t.get_completed() is not None and
            t.get_created() is not None
        ]

        if len(closed_tickets) == 0:
            return empty_result
        else:
            sum_completion_times = datetime.timedelta(0)
            for t in closed_tickets:
                sum_completion_times += (t.get_completed() - t.get_created())

            return {
                result_key: sum_completion_times / len(closed_tickets),
                count_key : len(closed_tickets)
            }

    def closed_epic_cycle_time(self):
        """
        Compute the cycle time of closed epics
        :return:
        """
        closed_epics = [t for t in self.__tickets if
            t.get_status() == Ticket.statuses_str["Done"] and
            t.get_plan_level() >= Ticket.plan_levels_str["Epic"] and
            t.get_completed() is not None and
            t.get_created() is not None
        ]
        if len(closed_epics) == 0:
            return empty_result
        else:
            sum_completion_times = datetime.timedelta(0)
            for t in closed_epics:
                sum_completion_times += (t.get_completed() - t.get_created())

            return {
                result_key: sum_completion_times / len(closed_epics),
                count_key : len(closed_epics)
            }

    def epic_cycle_time(self):
        """
        Compute the cycle time of all epics (if not completed assume today as completed time)
        :return:
        """
        epics = [t for t in self.__tickets if
            t.get_plan_level() >= Ticket.plan_levels_str["Epic"] and
            t.get_created() is not None
        ]
        if len(epics) == 0:
            return empty_result
        else:
            sum_completion_times = datetime.timedelta(0)
            for t in epics:
                completion = t.get_completed() if t.get_completed() is not None else \
                    self.__current_time
                sum_completion_times += (completion - t.get_created())

            return {
                result_key: sum_completion_times / len(epics),
                count_key : len(epics)
            }

    def closed_worked_tickets(self):
        """
        Compute the average worked time of closed tickets
        :return:
        """
        worked_tickets = [t for t in self.__tickets if
            t.get_worked() is not None and t.get_worked() != 0 and
            t.get_plan_level() <= Ticket.plan_levels_str["Story"] and
            t.get_status() == Ticket.statuses_str["Done"]
        ]
        if len(worked_tickets) == 0:
            return empty_result
        else:
            sum_worked_hours = 0
            for t in worked_tickets:
                sum_worked_hours += t.get_worked()

            return {
                result_key: sum_worked_hours / len(worked_tickets),
                count_key : len(worked_tickets)
            }

    def worked_tickets(self):
        """
        Compute the average worked time of tickets
        :return:
        """
        worked_tickets = [t for t in self.__tickets if
            t.get_worked() is not None and t.get_worked() != 0 and
            t.get_plan_level() <= Ticket.plan_levels_str["Story"]
        ]
        if len(worked_tickets) == 0:
            return empty_result
        else:
            sum_worked_hours = 0
            for t in worked_tickets:
                sum_worked_hours += t.get_worked()

            return {
                result_key: sum_worked_hours / len(worked_tickets),
                count_key : len(worked_tickets)
            }

    def estimation_tickets(self):
        # get the list with only closed tickets
        """
        Compute teh average estimation of tickets
        :return:
        """
        estimation_tickets = [t for t in self.__tickets if
            t.get_estimate() is not None and t.get_estimate() != 0 and
            t.get_plan_level() <= Ticket.plan_levels_str["Story"]
        ]
        if len(estimation_tickets) == 0:
            return empty_result
        else:
            sum_estimations = 0
            for t in estimation_tickets:
                sum_estimations += t.get_estimate()

            return {
                result_key: sum_estimations / len(estimation_tickets),
                count_key : len(estimation_tickets)
            }

    def count_statuses(self):
        """
        Compute the count of the tickets for each status
        :return:
        """
        count_tickets = [t for t in self.__tickets if t.get_status() is not None]
        if len(count_tickets) == 0:
            return empty_result
        else:
            count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
            for t in count_tickets:
                count[t.get_status()] += 1

            count_str = {
                "New"   : count[0], "In Progress": count[1], "Testing": count[2],
                "Review": count[3], "Done": count[4]
            }

            return {
                result_key: count_str,
                count_key : len(count_tickets)
            }

    def estimation_worked_factor(self):
        """
        Computes the factor between the estimation and the worked
        :return:
        """
        estimation_worked_tickets = [t for t in self.__tickets if
            t.get_estimate() is not None and t.get_estimate() != 0 and
            t.get_worked() is not None and t.get_worked() != 0 and
            t.get_plan_level() <= Ticket.plan_levels_str["Story"]
        ]
        if len(estimation_worked_tickets) == 0:
            return empty_result
        else:
            sum_estimations = 0
            sum_worked = 0
            for t in estimation_worked_tickets:
                sum_estimations += t.get_estimate()
                sum_worked += t.get_worked()

            avg_estimation = sum_estimations / len(estimation_worked_tickets)
            avg_worked = sum_worked / len(estimation_worked_tickets)
            return {
                result_key: avg_worked / avg_estimation,
                count_key : len(estimation_worked_tickets)
            }

    def estimation_worked_closed_factor(self):
        """
        Computes the factor between the estimation and the worked for closed tickets
        :return:
        """
        estimation_worked_tickets = [t for t in self.__tickets if
            t.get_estimate() is not None and t.get_estimate() != 0 and
            t.get_worked() is not None and t.get_worked() != 0 and
            t.get_plan_level() <= Ticket.plan_levels_str["Story"] and
            t.get_status() == Ticket.statuses_str["Done"]
        ]
        if len(estimation_worked_tickets) == 0:
            return empty_result
        else:
            sum_estimations = 0
            sum_worked = 0
            for t in estimation_worked_tickets:
                sum_estimations += t.get_estimate()
                sum_worked += t.get_worked()

            avg_estimation = sum_estimations / len(estimation_worked_tickets)
            avg_worked = sum_worked / len(estimation_worked_tickets)
            return {
                result_key: avg_worked / avg_estimation,
                count_key : len(estimation_worked_tickets)
            }

    def estimation_sprint(self, start, end):
        """
        Compute the total estimation for the sprint determined by start and end
        :param start: The start day of the sprint
        :param end: THe end day of the sprint
        :return:
        """
        sprint_tickets = [t for t in self.__tickets if
            t.get_estimate() is not None and  # t.get_estimate() != 0 and
            t.get_plan_level() <= Ticket.plan_levels_str["Story"] and
            t.get_created() is not None and start <= t.get_created().date() <= end
        ]
        if len(sprint_tickets) == 0:
            return empty_result
        else:
            sum_estimations = 0
            for t in sprint_tickets:
                sum_estimations += t.get_estimate()

            return {
                result_key: sum_estimations,
                count_key : len(sprint_tickets)
            }

    def worked_sprint(self, start, end):
        """
        Compute the total worked for the sprint determined by start and end
        :param start: The start day of the sprint
        :param end: THe end day of the sprint
        :return:
        """
        sprint_tickets = [t for t in self.__tickets if
            t.get_worked() is not None and  # t.get_estimate() != 0 and
            t.get_plan_level() <= Ticket.plan_levels_str["Story"] and
            t.get_created() is not None and start <= t.get_created().date() <= end
        ]
        if len(sprint_tickets) == 0:
            return empty_result
        else:
            sum_worked = 0
            for t in sprint_tickets:
                sum_worked += t.get_worked()

            return {
                result_key: sum_worked,
                count_key : len(sprint_tickets)
            }
