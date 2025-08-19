# Agents Directory

This directory contains AI agent notebooks for itinerary planning, optimization, rescheduling, price estimation, and data aggregation for Egyptian tourism.

## Contents

- **DayDateAssigningAgent.ipynb**: Assigns days and dates to monument visits using optimization and LLMs.
- **IntraDayPlanningAgent.ipynb**: Plans intra-day activities for tourists.
- **ReasonablePrice.ipynb**: Estimates reasonable prices using search and LLMs.
- **ReschedulingAgent.ipynb**: Reschedules activities to avoid crowds, bad weather, and optimize time.
- **WeatherCrowdednessAggregator.ipynb**: Aggregates weather and crowdedness data for planning.

## How to Use

1. Open any notebook in Jupyter or VS Code.
2. Install required Python packages (see notebook cells for details, e.g. `langchain`, `openai`, `numpy`, etc.).
3. Run the notebook cells to:
   - Generate and optimize travel plans
   - Reschedule activities based on weather/crowdedness
   - Estimate prices and aggregate data

## Notes

- These agents are designed to work together for comprehensive itinerary planning.
- Update data sources and parameters in the notebooks as needed for your use case.

---
