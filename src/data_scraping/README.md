# Data Scraping Directory

This directory contains scripts and utilities for scraping data about Egyptian museums, monuments, archaeological sites, and sunken monuments from online sources.

## Contents

- **main.py**: Command-line interface for scraping different site types and showing statistics.
- **scraper.py**: Core scraper logic for extracting data from web pages.
- **extractors.py**: Utilities for extracting specific data fields.
- **data_manager.py**: Manages data storage and processing.
- **driver_manager.py**: Web driver setup and management for automated scraping.
- **config.py**: Configuration for URLs, selectors, and constants.
- **json_files/**: Output directory for scraped data in JSON format.

## How to Use

1. Install required Python packages (see scripts for details, e.g. `selenium`, `requests`).
2. Run the main scraper:
   ```powershell
   cd src/data_scraping
   python main.py --all
   # Or scrape a specific type:
   python main.py --type museums
   python main.py --type archaeological-sites
   python main.py --type sunken-monuments
   # Show statistics:
   python main.py --stats
   ```
3. Scraped data will be saved in the `json_files/` directory.

## Notes

- Update configuration in `config.py` as needed for new sites or selectors.
- Ensure you have internet access and the required permissions to scrape target sites.

---
