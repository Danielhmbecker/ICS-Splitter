import requests
import ics
from ics import Calendar
from collections import defaultdict

# Fetch the ICS feed from the provided URL
url = 'https://feeds.rotaready.com/calendar/brewdog?token=oGlI1BR1222XwBdmGXmCl8GTzgCpDofSSN0rSID5uMhnwfZTsH9gTj8dUzgLmOkkwoovKLYwWdEKxxTYafn35ys2q1GedIn0rAtZtbW7DFjW5AOTsXByKJPOzb5NWgIZ'
response = requests.get(url)

# Parse the ICS feed data
calendar = Calendar(response.text)

# Create a dictionary to store events by building
building_shifts = defaultdict(list)

# Loop through each event and sort it by the building name (assuming building info is in the location field)
for event in calendar.events:
    building = event.location  # Adjust this line based on where the building info is in the ICS file
    building_shifts[building].append(event)

# Save the parsed data into separate ICS files based on building
for building, events in building_shifts.items():
    new_calendar = Calendar(events)
    with open(f'{building}_shifts.ics', 'w') as f:
        f.writelines(new_calendar)
    print(f'Generated ICS for {building}')
