import requests

# === Configuration ===
# Coordinates for Cairo, Egypt
latitude = 30.0444
longitude = 31.2357
radius_meters = 1000  # Search radius in meters

# === Overpass API setup ===
overpass_url = "https://overpass-api.de/api/interpreter"

# Query to fetch nearby restaurants using Overpass QL
query = f"""
[out:json];
node(around:{radius_meters},{latitude},{longitude})["amenity"="restaurant"];
out center 10;
"""

# === API Request ===
response = requests.post(overpass_url, data=query)

# Raise an error if the request failed
response.raise_for_status()

# Parse JSON response
data = response.json()

# === Display Results ===
print(f"Restaurants within {radius_meters} meters of ({latitude}, {longitude}):\n")
for element in data.get("elements", []):
    tags = element.get("tags", {})
    name = tags.get("name", "<no name>")
    lat = element.get("lat")
    lon = element.get("lon")
    print(f"- {name} at ({lat}, {lon})")