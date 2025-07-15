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

# Define the output directory path
output_dir = 'output/Splits'

# Ensure the output directory exists (create it if not)
os.makedirs(output_dir, exist_ok=True)

# Initialize a dictionary to store events by location
location_shifts = defaultdict(list)

# Loop through each event and sort it by location (filtering for BrewDog locations)
for event in calendar.events:
    if event.location and "BrewDog" in event.location:
        location_shifts[event.location].append(event)

# Debugging: Check how many locations and events are found
print(f"Total BrewDog locations found: {len(location_shifts)}")

# Now, create separate ICS files for each BrewDog location
for location, events in location_shifts.items():
    # Debugging: Check how many events are in each location
    print(f"Processing {len(events)} events for {location}")
    
    # Create a new calendar for each location's events
    new_calendar = Calendar(events)
    
    # Define the output path based on the location
    location_cleaned = location.replace(" ", "_").replace("/", "_")  # Clean location name for filenames
    output_ics_path = os.path.join(output_dir, f"{location_cleaned}_shifts.ics")
    
    # Write the new ICS file
    with open(output_ics_path, 'w') as ics_file:
        ics_file.writelines(new_calendar)
    
    # Debugging: Confirm that the file is being created
    print(f"Generated ICS for {location} at {output_ics_path}")

# Check if any ICS files exist in the output folder after script runs
print(f"Checking generated ICS files in {output_dir}")
for root, dirs, files in os.walk(output_dir):
    for file in files:
        print(f"Found: {file}")
