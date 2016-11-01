import datetime
import requests
import json
import sys
import time
import Meter
import config
import Ticket
import printer

# Basic values
headers = {'X-API-Key': config.key, 'X-API-Secret': config.secret}
basic_url = 'https://api.assembla.com/v1/'
space_url = basic_url + 'spaces.json'


# Returns the url of the document list for space {@code space}
def tickets_url(workspace):
    """
    The url to fetch the tickets from for a particular workspace
    :param workspace: The workspace
    :return: The url to fetch the tickets from
    """
    return basic_url + 'spaces/' + workspace + '/tickets'


# Returns the url of the specific ticket with id {@code id} in space {@code space}
def ticket_id_url(workspace, number):
    """
    The url for a specific ticket in a specific workspace
    :param workspace: The workspace
    :param number: The number of the ticket
    :return: The url to fetch that specific ticket
    """
    return basic_url + ' spaces/' + workspace + '/tickets/' + number + '.json'


# First we fetch all spaces from this user
spaces_req = requests.get(space_url, headers = headers)
spaces_json = json.loads(spaces_req.text)

# Print each of the spaces and ask which to download from
for i in range(len(spaces_json)):
    print(str(i) + ": " + spaces_json[i]['name']  # + " (id:" + str(spaces_json[i]['id']) + ")"
          )

picked = -1
while picked < 0 or picked >= len(spaces_json):
    try:
        picked = int(input("Which space to download tickets from?"))
    except ValueError:
        picked = -1

space_id = picked

# set the empty collection of all tickets
tickets = []

# start with page 1 of the tickets API
j = 1
space = spaces_json[space_id]['id']

print("Start downloading tickets.")
tickets_req = requests.get(tickets_url(space), headers = headers, params = {
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
        ticket = Ticket.Ticket(tickets_json[i]['number'])
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
    time.sleep(1)
    j += 1
    tickets_req = requests.get(tickets_url(space), headers = headers,
                               params = {'per_page': 10, 'page': j, 'report': 0})
    try:
        tickets_json = json.loads(tickets_req.text)
    except json.decoder.JSONDecodeError as e:
        # If there is no more data, a JSON decode error will be thrown
        print("Done downloading tickets (" + str(len(tickets)) + ").")
        break

if len(tickets) > 0:
    meter = Meter.Meter(tickets)

    options_output = {0: "Console", 1: "File"}
    print(options_output)
    picked = -1
    while picked < 0 or picked >= len(options_output):
        try:
            picked = int(input("Where to write the output to?"))
        except ValueError:
            picked = -1

    output_selection = picked

    if output_selection == 0:
        # if written to console then ask what to print
        picked = picked
        options_stats = {0: "General Statistics", 1: "Sprint Related Statistics"}
        print(options_stats)
        picked = -1
        while picked < 0 or picked >= len(options_stats):
            try:
                picked = int(input("Which stats to compute on the tickets?"))
            except ValueError:
                picked = -1

        option_stats_selected = picked

        if option_stats_selected == 0:
            printer.general_stats(meter)
        elif option_stats_selected == 1:
            printer.sprint_stats(meter, space)
    elif output_selection == 1:
        # if output written  to file, compute everything
        print("Writing output to file.")
        sys.stdout = open(config.output_dir + "\\output_" + str(datetime.datetime.now()).
                          replace(" ", "_").replace(".", "_").replace(":", "_")
                          + ".txt", "w")
        print("Computing statistics for " + str(len(tickets)) + " tickets")
        printer.general_stats(meter)
        printer.sprint_stats(meter, space)

else:
    print("No tickets to compute metrics on.")
