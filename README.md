# AI Empower Hackathon 2025: Enhancing Egyptian Tourism

## Problem Definition
The Egyptian tourism sector, a cornerstone of the national economy and a vital source of foreign currency, is ripe for digital innovation. Our solution is designed to address critical inefficiencies and challenges that hinder a truly world-class tourist experience.  
The problems we are tackling are not just inconveniences for travelers; they represent significant barriers to sustainable growth for the industry as a whole.

Our project aims to solve the following core issues:

- **Overcrowding & Congestion:** Tourist hotspots in cities like Cairo and Luxor frequently suffer from high foot traffic during peak hours, leading to long queue times, a degraded visitor experience, and potential stress on historical sites.  
  *Solution:* Optimizes visiting schedules to reduce queue time and distribute visitors evenly throughout the day, preserving the integrity of archaeological treasures.

- **Lack of Personalization:** Generic, one-size-fits-all itineraries fail to capture the unique interests of modern travelers.  
  *Solution:* Enhances tourist experience by generating personalized plans that are more likely to be followed and enjoyed.

- **Underused Destinations ("Hidden Gems"):** Many culturally rich and historically significant sites are overshadowed by major attractions.  
  *Solution:* Promotes lesser-known sites to distribute economic benefits more equitably and reduce strain on popular sites.

- **Poor On-site Experience:** Tourists face hurdles like complex urban transport and unfair pricing for local goods.  
  *Solution:* Reduces overpaying and ensures a seamless, stress-free travel experience, improving satisfaction and encouraging positive recommendations.

---

## Motivation: The Importance for Egypt's Tourism
This solution aligns with Egypt's National AI Strategy 2025-2030 and Vision 2030 for sustainable tourism.

- **Economic Growth and Diversification:** Enhances tourist experience and promotes a wider range of sites, increasing length of stay and spending, benefiting both major hubs and local communities.  
- **Global Competitiveness:** AI-driven, personalized, and seamless experience strengthens Egypt’s position in the global travel market.  
- **Sustainability and Preservation:** Manages visitor flow to prevent overcrowding, preserving fragile historical sites for future generations.

---

## Our Solution: A Multi-Agent Architecture
A multi-agent system designed to create a dynamic, personalized, and efficient tourism experience. It consists of three interconnected modules, each powered by specialized AI agents working collaboratively and sharing data in real time.

### Module 1: Intelligent Itinerary Planner
**Workflow:**
1. **User Query:** Users provide a natural language query, e.g., "Schedule an itinerary in Cairo from 14/8/2025 to 16/8/2025, I am mostly interested in archaeological sites."
2. **Query Refinement:** Cleans input to extract relevant entities.
3. **Information Agent (RAG):**  
   - Retrieval-Augmented Generation system fine-tuned on Egyptian Ministry of Tourism and Antiquities data.  
   - Retrieves matching tourist sites and promotes "hidden gems" with fewer reviews.
4. **Data Fetching & Clustering:**  
   - Fetches real-time weather and crowdedness data (APIs like BestTime.app).  
   - Clusters sites into daily groups, balancing hours per day.
5. **Planning Agent:** Orchestrates schedule and logistics.  
   - **Scheduling Sub-Agent:** Assigns sites to dates, minimizes exposure to extreme heat, avoids peak hours.  
   - **Booking Sub-Agent:** Books Uber rides and suggests nearby restaurants.

### Module 2: Itinerary Maintenance Module
**Workflow:**
1. **Scheduled Monitoring:** Periodically checks crowdedness for upcoming sites.  
2. **Live Foot Traffic Tool:** Compares current crowdedness with historical data.  
3. **Dynamic Rescheduling:** Automatically adjusts itinerary and transportation to optimize for heat, crowds, and seamless experience.

### Module 3: Reasonable Pricing Module
**Workflow:**
1. **User Input:** User enters item name.  
2. **AI Agent & LangChain:** Performs live web search.  
3. **Price Fetching:** Retrieves top 5 search results.  
4. **Price Range Generation:** Produces:
   - **Reasonable Price Range:** Fair market price.
   - **Touristic Price Range:** Higher, realistic tourist area price for negotiation.

---

## Novelty Highlights
- **Holistic Optimization:** Balances multiple constraints like heat, crowd levels, and logical daily flow.  
- **Adaptive Maintenance Loop:** Real-time re-planning prevents itinerary disruptions.  
- **"Hidden Gems" Promotion:** Strategically recommends low-review sites for sustainable tourism.  
- **On-site Financial Protection:** Provides fair pricing guidance, enhancing traveler trust.

---

## Technical Overview

### Dataset
Scraped from the Egyptian Ministry of Tourism and Antiquities. Each row represents a site with fields:
- `url`, `name`, `location`, `Outdoors` (bool), `Latitude`, `Longitude`, `hours_needed`, `rating`, `reviews`, `description`, `opening_hours`, `prices`, `services`.

---

### Notebooks & Scripts

#### `RAG/RAG.ipynb`
- Implements Information Agent for itinerary generation using RAG workflow.  
- Components: Vector store (Chroma), embeddings (HuggingFace), intent refinement, document retrieval, hidden gems filtering.

#### `agents/WeatherCrowdednessAggregator.ipynb`
- Aggregates weather and foot traffic data for itinerary planning.  
- Input: List of sites with location and date range.  
- Output: Hourly forecasts and crowdedness data.

#### `clustering/ClusteringLocations.ipynb`
- Clusters sites into daily itineraries.  
- Tools: K-Means, Optuna (hyperparameter tuning), Haversine formula.  
- Output: Balanced daily schedule.

#### `agent/DayDateAssigningAgent.ipynb`
- Schedules clustered daily groups to specific dates.  
- Uses brute-force optimization considering heat exposure and crowd density.  
- Wrapped in LangChain agent for reasoning transparency.

#### `agents/IntraDayPlanningAgent.ipynb`
- Creates optimal hourly schedule for each day.  
- Criteria: crowd levels, temperature, time of day.  
- Greedy algorithm + LangChain agent for human-readable explanations.

#### `agents/ReschedulingAgent.ipynb`
- Dynamic rescheduling for unexpected events.  
- Penalty-based optimization for heat, crowds, and timing.  
- LangChain agent provides reasoning and comparison of original vs. new schedule.

#### `agents/ReasonablePrice.ipynb`
- Provides item price range using LangChain and web search (TavilySearch).  
- Aggregates top results for reasonable and tourist-specific price ranges.

#### `scripts/restaurants.py`
- Input: Latitude, longitude, radius.  
- Output: Nearby restaurants with names and coordinates.

#### `scripts/rental.py`
- Input: Pickup/drop-off coordinates, dates, times.  
- Output: Optimal rental car option with details (name, price, supplier, rating, pick-up/drop-off info).
