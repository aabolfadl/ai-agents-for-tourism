# Scripts Directory

This directory contains utility scripts for travel planning and data gathering related to rentals and restaurants in Egypt.

## Files

- **rental.py**

  - Schedules car rentals using the Booking.com RapidAPI.
  - Searches for available rental cars, displays details, and saves the top result to a JSON file.
  - Usage: Edit the script to provide pickup/dropoff details, then run with Python.

- **restaurants.py**
  - Finds nearby restaurants using the Overpass API (OpenStreetMap data).
  - Configurable for location and search radius.
  - Usage: Edit coordinates and radius as needed, then run with Python to print nearby restaurants.

## How to Use

1. Make sure you have Python 3 installed.
2. Install required packages:
   - For `rental.py`: `http.client`, `urllib`, `json` (standard library)
   - For `restaurants.py`: `requests`
3. Edit the scripts to set your parameters (API keys, coordinates, dates, etc.).
4. Run the scripts:
   ```powershell
   python rental.py
   python restaurants.py
   ```

## Notes

- The scripts are intended as utilities and may require editing for your specific use case.
- API keys and internet access are required for external requests.

---
