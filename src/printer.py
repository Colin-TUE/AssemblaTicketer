import Meter
import sprint_dates


def general_stats(meter):
    """
    Prints the general stats of the project
    """
    print("===========================")
    print("Start computing cycle time.")
    res = meter.closed_tickets_cycle_time()
    print("Average ticket cycle time is: " + str(res[Meter.result_key]) +
          ". With " + str(res[Meter.count_key]) + " tickets")
    res = meter.closed_epic_cycle_time()
    print("Average cycle time is: " + str(res[Meter.result_key]) +
          ". With " + str(res[Meter.count_key]) + " epics")
    res = meter.epic_cycle_time()
    print("Average running cycle time is: " + str(res[Meter.result_key]) +
          ". With " + str(res[Meter.count_key]) + " epics")

    print("===========================")
    print("Start computing work done time.")
    res = meter.closed_worked_tickets()
    print("Average closed worked time is: " + str(res[Meter.result_key]) +
          ". With " + str(res[Meter.count_key]) + " tickets")
    print("Start computing worked time.")
    res = meter.worked_tickets()
    print("Average worked time is: " + str(res[Meter.result_key]) +
          ". With " + str(res[Meter.count_key]) + " tickets")

    print("===========================")
    print("Start computing estimation.")
    res = meter.estimation_tickets()
    print("Average estimation is: " + str(res[Meter.result_key]) +
          ". With " + str(res[Meter.count_key]) + " tickets")

    print("===========================")
    print("Start worked estimation.")
    res = meter.estimation_worked_factor()
    print("Factor between estimation and worked is: " + str(res[Meter.result_key]) +
          ". With " + str(res[Meter.count_key]) + " tickets")
    res = meter.estimation_worked_closed_factor()
    print("Factor between estimation and worked closed is: " + str(res[Meter.result_key]) +
          ". With " + str(res[Meter.count_key]) + " tickets")

    print("===========================")
    print("Start counting status estimation.")
    res = meter.count_statuses()
    print("Count of the tickets according to status: " + str(res[Meter.result_key]) +
          ". With " + str(res[Meter.count_key]) + " tickets")

    print("===========================")
    print("Done computing metrics.")


def sprint_stats(meter, workspace):
    """
    Prints the sprint specific stats of the project
    """
    sprints = sprint_dates.sprint_dates(workspace)

    print("===========================")
    print("Start computing sprint specific estimation time.")
    for i in range(len(sprints)):
        print("Sprint " + str(i) + ":")
        res = meter.estimation_sprint(sprints[i][sprint_dates.start_key],
                                      sprints[i][sprint_dates.end_key])
        print("Estimation: " + str(res[Meter.result_key]) +
              ". With " + str(res[Meter.count_key]) + " tickets")
        res = meter.worked_sprint(sprints[i][sprint_dates.start_key],
                                  sprints[i][sprint_dates.end_key])
        print("Worked:     " + str(res[Meter.result_key]) +
              ". With " + str(res[Meter.count_key]) + " tickets")
