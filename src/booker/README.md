# Booker Directory

This directory contains scripts for web crawling and automating bookings for Egyptian monuments using the EgyMonuments website.

## Contents

- **main_booking.py**: Main script for automating the booking workflow via web crawling.
- **web_utils.py**: Utility functions for web driver setup, element finding, and booking interactions.
- **booking_details.json**: Input data for booking requests.

## How to Use

1. Install required Python packages:
   - `selenium`, `webdriver_manager`, `json`, etc.
2. Edit `booking_details.json` to specify the bookings you want to automate.
3. Run the main booking script:
   ```powershell
   cd src/booker
   python main_booking.py
   ```
4. The script will use a web driver to navigate, fill forms, and automate bookings on the EgyMonuments website.

## Notes

- Update utility functions in `web_utils.py` as needed for new booking flows or website changes.
- Ensure you have Chrome installed and internet access for Selenium automation.
- Booking data should be valid and formatted correctly in `booking_details.json`.

---
