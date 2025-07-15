import os
import requests
import ics
from ics import Calendar

# Fetch the ICS feed from the provided URL
url = 'https://feeds.rotaready.com/calendar/brewdog?token=oGlI1BR1222XwBdmGXmCl8GTzgCpDofSSN0rSID5uMhnwfZTsH9gTj8dUzgLmOkkwoovKLYwWdEKxxTYafn35ys2q1GedIn0rAtZtbW7DFjW5AOTsXByKJPOzb5NWgIZ'
response = requests.get(url)

# Parse the ICS feed data
calendar = Calendar(response.text)

# Create the output directories
output_dir = 'output/Splits'
os.makedirs(output_dir, exist_ok=True)

# Create a TXT file with all event data
txt_file_path = os.path.join(output_dir, 'events_data.txt')
with open(txt_file_path, 'w') as txt_file:
    for event in calendar.events:
        event_data = f"Event Title: {event.name}\n"
        event_data += f"Start: {event.begin}\n"
        event_data += f"End: {event.end}\n"
        event_data += f"Location: {event.location}\n"
        event_data += f"Description: {event.description}\n"
        event_data += f"URL: {event.url if event.url else 'N/A'}\n\n"
        txt_file.write(event_data)

print(f"Event data saved to {txt_file_path}")

# Recreate ICS files from TXT data
with open(txt_file_path, 'r') as txt_file:
    event_lines = txt_file.read().split('\n\n')  # Split events by double newline

for idx, event in enumerate(event_lines):
    event_info = event.split('\n')
    event_name = event_info[0].split(": ")[1]
    event_start = event_info[1].split(": ")[1]
    event_end = event_info[2].split(": ")[1]
    event_location = event_info[3].split(": ")[1]
    event_description = event_info[4].split(": ")[1]
    event_url = event_info[5].split(": ")[1]

    new_event = ics.Event(name=event_name, begin=event_start, end=event_end, location=event_location, description=event_description, url=event_url)

    # Create a new ICS calendar and add this event
    new_calendar = ics.Calendar(events=[new_event])
    output_ics_path = os.path.join(output_dir, f"event_{idx+1}.ics")

    # Write the new ICS file
    with open(output_ics_path, 'w') as ics_file:
        ics_file.writelines(new_calendar)
    print(f"Generated ICS for event: {event_name} at {output_ics_path}")
