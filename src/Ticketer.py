import datetime
import requests
import json
import config
from Ticket import Ticket

# Basic values
headers = {'X-API-Key': config.key, 'X-API-Secret': config.secret}
basicurl = 'https://api.assembla.com/v1/'
spaceurl = basicurl + 'spaces.json'


# Returns the url of the document list for space {@code space}
def ticketsurl(space):
    return basicurl + 'spaces/' + space + '/tickets'


# Returns the url of the specific ticket with id {@code id} in space {@code space}
def wikiurl(space, number):
    return basicurl + ' spaces/' + space + '/tickets/' + number + '.json'


# First we fetch all spaces from this user
spaces_req = requests.get(spaceurl, headers = headers)
spaces_json = json.loads(spaces_req.text)

# Print each of the spaces and ask which to download from
for i in range(len(spaces_json)):
    print(str(i) + ": " + spaces_json[i]['name'])

picked = -1
while picked < 0 or picked >= len(spaces_json):
    picked = int(input("Which space to download tickets from?"))

space_id = picked

# set the empty collection of all tickets
tickets = []

# start with page 1 of the tickets API
j = 1
space = spaces_json[space_id]['id']

print("Start downloading tickets.")
tickets_req = requests.get(ticketsurl(space), headers = headers, params = {
    'per_page': 10,
    'page'    : j, 'report': 0
})
try:
    tickets_json = json.loads(tickets_req.text)
except json.decoder.JSONDecodeError as e:
    print("No tickets to download at all.")
    tickets_json = []

# Loop over all pages of the json and get the tickets
while len(tickets_json) is not 0:
    # Fetch all tickets on this page
    for i in range(len(tickets_json)):
        # print("Fetching: " + str(tickets_json[i]))
        # actually store relevant information
        # TODO
        ticket = Ticket(tickets_json[i]['number'])
        ticket.set_created(tickets_json[i]['created_on'])
        ticket.set_completed(tickets_json[i]['completed_date'])
        ticket.set_estimate(tickets_json[i]['estimate'])
        ticket.set_worked_hours(tickets_json[i]['total_invested_hours'])
        ticket.set_plan_level(tickets_json[i]['hierarchy_type'])
        ticket.set_status(tickets_json[i]['status'])
        ticket.set_due_date(tickets_json[i]['due_date'])
        # print(ticket.to_string())
        tickets.append(ticket)

    # go to next page if possible
    j += 1
    tickets_req = requests.get(ticketsurl(space), headers = headers,
                               params = {'per_page': 10, 'page': j, 'report': 0})
    try:
        tickets_json = json.loads(tickets_req.text)
    except json.decoder.JSONDecodeError as e:
        # If there is no more data, a JSON decode error will be thrown
        print("Done downloading tickets (" + str(len(tickets)) + ").")
        break

if len(tickets) > 0:
    print("Starting to compute metrics.")

    print("===========================")
    print("Start computing cycle time.")
    # get the list with only closed tickets
    closed_tickets = [t for t in tickets if t.get_status() == 4 and t.get_plan_level() < 2 and
                                            t.get_completed() is not None and t.get_created is
                                                                              not None]

    if len(closed_tickets) == 0:
        print("There are no closed tickets.")
    else:
        sum_completion_times = datetime.timedelta(0)
        for t in closed_tickets:
            sum_completion_times += (t.get_completed() - t.get_created())

        print("Average cycle time is: " + str(sum_completion_times / len(closed_tickets)) +
              ". With " + str(len(closed_tickets)) + " tickets")

    print("===========================")
    print("Start computing work done time.")
    # get the list with only closed tickets
    worked_tickets = [t for t in tickets if
        t.get_worked() is not None and t.get_worked() != 0 and t.get_plan_level() < 2]
    if len(worked_tickets) == 0:
        print("There are no tickets with worked hours.")
    else:
        sum_worked_hours = 0
        for t in worked_tickets:
            sum_worked_hours += t.get_worked()

        print("Average worked time is: " + str(sum_worked_hours / len(worked_tickets)) +
              ". With " + str(len(worked_tickets)) + " tickets")

    print("===========================")
    print("Start computing estimation.")
    # get the list with only closed tickets
    estimation_tickets = [t for t in tickets if t.get_estimate() is not None and
                                                t.get_estimate() != 0 and t.get_plan_level() < 2]
    if len(estimation_tickets) == 0:
        print("There are no tickets with an estimation.")
    else:
        sum_estimations = 0
        for t in estimation_tickets:
            sum_estimations += t.get_estimate()

        print("Average estimation is: " + str(sum_estimations / len(estimation_tickets)) +
              ". With " + str(len(estimation_tickets)) + " tickets")

    print("===========================")
    print("Start completed worked estimation.")
    # get the list with only closed tickets
    completed_worked_tickets = [t for t in tickets if
        t.get_estimate() is not None and t.get_estimate() != 0 and t.get_worked() is not None and
        t.get_worked() != 0 and t.get_status() == 4 and t.get_plan_level() < 2]
    if len(completed_worked_tickets) == 0:
        print("There are no tickets with an estimation.")
    else:
        sum_worked = 0
        sum_estimates = 0
        for t in completed_worked_tickets:
            sum_estimates += t.get_estimate()
            sum_worked += t.get_worked()

        print("Average estimation of completed tickets is: " + str(sum_estimates / len(
            completed_worked_tickets)))
        print("Average worked of completed tickets is: " + str(sum_worked / len(
            completed_worked_tickets)))
        print("Factor is: " + str(
            (sum_worked / len(completed_worked_tickets)) /
            (sum_estimates / len(completed_worked_tickets))) +
              ". With " + str(len(completed_worked_tickets)) + " tickets")

    print("===========================")
    print("Start counting status estimation.")
    # get the list with only closed tickets
    count_tickets = [t for t in tickets if t.get_status() is not None]
    if len(count_tickets) == 0:
        print("There are no tickets with an estimation.")
    else:
        count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        for t in count_tickets:
            count[t.get_status()] += 1

        print("Count of the tickets according to status: " + str(count) +
              ". With " + str(len(count_tickets)) + " tickets")

    print("===========================")
    print("Done computing metrics.")
else:
    print("No tickets to compute metrics on.")
