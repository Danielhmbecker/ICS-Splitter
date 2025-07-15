import os
import requests
import ics
from ics import Calendar
from collections import defaultdict

# Fetch the ICS feed from the provided URL
url = 'https://feeds.rotaready.com/calendar/brewdog?token=oGlI1BR1222XwBdmGXmCl8GTzgCpDofSSN0rSID5uMhnwfZTsH9gTj8dUzgLmOkkwoovKLYwWdEKxxTYafn35ys2q1GedIn0rAtZtbW7DFjW5AOTsXByKJPOzb5NWgIZ'
response = requests.get(url)

# Parse the ICS feed data
calendar = Calendar(response.text)

# Create the output directories
output_dir = 'output/Splits'
os.makedirs(output_dir, exist_ok=True)

# Initialize a dictionary to store events by location
location_shifts = defaultdict(list)

# Loop through each event and sort it by location (filtering for BrewDog locations)
for event in calendar.events:
    if event.location and "BrewDog" in event.location:
        location_shifts[event.location].append(event)

# Now, create separate ICS files for each BrewDog location
for location, events in location_shifts.items():
    # Create a new calendar for each location's events
    new_calendar = Calendar(events)
    
    # Define the output path based on the location
    location_cleaned = location.replace(" ", "_").replace("/", "_")  # Clean location name for filenames
    output_ics_path = os.path.join(output_dir, f"{location_cleaned}_shifts.ics")
    
    # Write the new ICS file
    with open(output_ics_path, 'w') as ics_file:
        ics_file.writelines(new_calendar)
    
    print(f"Generated ICS for {location} at {output_ics_path}")
