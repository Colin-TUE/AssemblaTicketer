import datetime
import Ticket

result_key = "res"
count_key = "count"


class Meter:
    def __init__(self, tickets):
        if len(tickets) == 0:
            raise ValueError("Tickets is empty")

        self.__current_time = datetime.datetime.now()
        self.__tickets = tickets

    def closed_tickets_cycle_time(self):
        # get the list with only closed tickets
        closed_tickets = [t for t in self.__tickets if
            t.get_status() == Ticket.statuses_str["Done"] and
            t.get_plan_level() <= Ticket.plan_levels_str["Story"] and
            t.get_completed() is not None and
            t.get_created is not None
        ]

        if len(closed_tickets) == 0:
            return {result_key: 0, count_key: 0}
        else:
            sum_completion_times = datetime.timedelta(0)
            for t in closed_tickets:
                sum_completion_times += (t.get_completed() - t.get_created())

            return {
                result_key: sum_completion_times / len(closed_tickets),
                count_key : len(closed_tickets)
            }

    def closed_epic_cycle_time(self):
        closed_epics = [t for t in self.__tickets if
            t.get_status() == Ticket.statuses_str["Done"] and
            t.get_plan_level() > Ticket.plan_levels_str["Epic"] and
            t.get_completed() is not None and
            t.get_created is not None
        ]
        if len(closed_epics) == 0:
            return {result_key: 0, count_key: 0}
        else:
            sum_completion_times = datetime.timedelta(0)
            for t in closed_epics:
                sum_completion_times += (t.get_completed() - t.get_created())

            return {
                result_key: sum_completion_times / len(closed_epics),
                count_key : len(closed_epics)
            }


    def epic_cycle_time(self):
        closed_epics = [t for t in self.__tickets if
            t.get_plan_level() > Ticket.plan_levels_str["Epic"] and
            t.get_created is not None
        ]
        if len(closed_epics) == 0:
            return {result_key: 0, count_key: 0}
        else:
            sum_completion_times = datetime.timedelta(0)
            for t in closed_epics:
                completion = t.get_completed() if t.get_completed() is not None else \
                    self.__current_time
                sum_completion_times += (completion - t.get_created())

            return {
                result_key: sum_completion_times / len(closed_epics),
                count_key : len(closed_epics)
            }