# Dell-AI-Hackathon

## Overview

This repository contains an AI-powered system for optimizing tourist itineraries, booking visits, and scraping data about Egyptian monuments. It leverages agents, automation scripts, clustering, retrieval-augmented generation (RAG), and web scraping to provide a comprehensive travel planning solution.

## Directory Structure

```
src/
  agents/         # AI agents for itinerary planning, rescheduling, price estimation, and more
  booker/         # Automation scripts for booking visits via EgyMonuments
  clustering/     # Location clustering notebooks
  data_scraping/  # Web scraping utilities and scripts for Egyptian monuments
  RAG/            # Retrieval-Augmented Generation notebook for recommendations
  scripts/        # Additional scripts (e.g., rental, restaurants)
Documentation.pdf # Project documentation
README.md         # This file
```

### Key Components

- **Agents**:

  - `DayDateAssigningAgent.ipynb`: Assigns days and dates to monument visits using optimization and LLMs.
  - `IntraDayPlanningAgent.ipynb`: Plans intra-day activities for tourists.
  - `ReasonablePrice.ipynb`: Estimates reasonable prices using search and LLMs.
  - `ReschedulingAgent.ipynb`: Reschedules activities to avoid crowds, bad weather, and optimize time.
  - `WeatherCrowdednessAggregator.ipynb`: Aggregates weather and crowdedness data.

- **Booker**:

  - `main_booking.py`: Main script for automating bookings.
  - `web_utils.py`: Web automation utilities for booking.
  - `booking_details.json`: Booking data.

- **Clustering**:

  - `ClusteringLocations.ipynb`: Clusters locations for itinerary optimization.

- **Data Scraping**:

  - `main.py`: CLI for scraping museums, archaeological sites, and sunken monuments.
  - `extractors.py`, `data_manager.py`, `driver_manager.py`, `scraper.py`: Scraping utilities.
  - `json_files/`: Output data files.

- **RAG**:

  - `RAG.ipynb`: Uses retrieval-augmented generation for personalized recommendations.

- **Scripts**:
  - `rental.py`, `restaurants.py`: Additional utilities.

## Setup

1. **Clone the repository**

   ```powershell
   git clone <repo-url>
   cd Dell-AI-Hackathon-main
   ```

2. **Install Python dependencies**  
   Most notebooks/scripts require:

   - `langchain`
   - `requests`
   - `numpy`
   - `pydantic`
   - `selenium`
   - `webdriver_manager`
   - `openai`
   - `tiktoken`
   - (see individual notebooks/scripts for full requirements)

   Install with:

   ```powershell
   pip install -r requirements.txt
   ```

   Or install manually as needed.

3. **Run Jupyter Notebooks**  
   Open notebooks in `src/agents/`, `src/clustering/`, or `src/RAG/` with Jupyter or VS Code.

4. **Run Booking Automation**

   ```powershell
   cd src/booker
   python main_booking.py
   ```

5. **Run Data Scraping**
   ```powershell
   cd src/data_scraping
   python main.py --all
   # Or see --help for options
   ```

## Usage

- **Itinerary Planning**:  
  Use the agents in `src/agents/` to generate, optimize, and reschedule travel plans.

- **Booking**:  
  Automate bookings using scripts in `src/booker/`.

- **Data Scraping**:  
  Scrape monument data using `src/data_scraping/main.py`.

- **Clustering & RAG**:  
  Use clustering and RAG notebooks for advanced recommendations.

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

MIT License

---
