import csv
import folium
from datetime import datetime
from collections import defaultdict

# Define the Bigfoot class
class Bigfoot:
    def __init__(self, number, title, classification, timestamp, latitude, longitude):
        self.number = number
        self.title = title
        self.classification = classification
        self.timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def to_dict(self):
        return {
            'number': self.number,
            'title': self.title,
            'classification': self.classification,
            'timestamp': self.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'latitude': self.latitude,
            'longitude': self.longitude
        }

# Function to read CSV and map to Bigfoot instances
def load_bigfoot_data(csv_file):
    bigfoot_sightings = []
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            sighting = Bigfoot(
                number=row['number'],
                title=row['title'],
                classification=row['classification'],
                timestamp=row['timestamp'],
                latitude=row['latitude'],
                longitude=row['longitude']
            )
            bigfoot_sightings.append(sighting)
    return bigfoot_sightings

# Function to aggregate sightings by year
def aggregate_sightings_by_year(sightings):
    sightings_by_year = defaultdict(list)
    
    for sighting in sightings:
        year = sighting.timestamp.year
        sightings_by_year[year].append(sighting)
    
    return sightings_by_year

# Function to plot all sightings on a single map
def plot_all_sightings_on_map(sightings_by_year):
    # Initialize a map centered at an approximate center point
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
    
    # Add a marker for each sighting
    for year, sightings in sightings_by_year.items():
        for sighting in sightings:
            folium.Marker(
                location=[sighting.latitude, sighting.longitude],
                popup=(
                    f"Year: {year}<br>"
                    f"Title: {sighting.title}<br>"
                    f"Classification: {sighting.classification}<br>"
                    f"Timestamp: {sighting.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')}"
                ),
                tooltip=f"{year}: {sighting.title}"
            ).add_to(m)
    
    # Save the map to a single HTML file
    m.save("all_bigfoot_sightings.html")

# Load Bigfoot sightings from a CSV file
csv_file = './data/bfro_locations.csv'
bigfoot_sightings = load_bigfoot_data(csv_file)

# Aggregate sightings by year
sightings_by_year = aggregate_sightings_by_year(bigfoot_sightings)

# Plot all sightings on a single map
plot_all_sightings_on_map(sightings_by_year)
