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

# Set the condition for looping to true
ticketsPresent = True

j = 1
space = spaces_json[space_id]['id']
tickets_req = requests.get(ticketsurl(space), headers = headers, params = {
    'per_page': 10,
    'page'    : j, 'report': 0
})
try:
    tickets_json = json.loads(tickets_req.text)
except json.decoder.JSONDecodeError as e:
    print("No tickets to download at all:")
    tickets_json = []

# Loop over all pages of the json and get the tickets
while len(tickets_json) is not 0:
    # Fetch all tickets on this page
    for i in range(len(tickets_json)):
        print("Fetching: " + str(tickets_json[i]))
        # actually store relevant information
        # TODO
        ticket = Ticket(tickets_json[i]['number'])
        ticket.setCreated(tickets_json[i]['created_on'])
        ticket.setCompelted(tickets_json[i]['completed_date'])
        ticket.setEstimate(tickets_json[i]['estimate'])
        ticket.setWorkedHours(tickets_json[i]['total_invested_hours'])
        ticket.setPlanLevel(tickets_json[i]['hierarchy_type'])
        ticket.setStatus(tickets_json[i]['status'])
        ticket.setDueDate(tickets_json[i]['due_date'])

    # go to next page if possible
    j += 1
    tickets_req = requests.get(ticketsurl(space), headers = headers,
                               params = {'per_page': 10, 'page': j, 'report': 0})
    try:
        tickets_json = json.loads(tickets_req.text)
    except json.decoder.JSONDecodeError as e:
        # If there is no more data, a JSON decode error will be thrown
        print("Done downloading tickets")
        break
print("Starting to compute metrics.")

