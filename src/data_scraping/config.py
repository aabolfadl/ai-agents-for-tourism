"""Configuration settings for the web scraper."""

# Base configurations
BASE_URLS = {
    "museums": "https://egymonuments.gov.eg/en/museums",
    "archaeological-sites": "https://egymonuments.gov.eg/en/archaeological-sites", 
    "monuments": "https://egymonuments.gov.eg/en/monuments",
    "sunken-monuments": "https://egymonuments.gov.eg/en/sunken-monuments"
}

OUTPUT_FILES = {
    "museums": "museums.json",
    "archaeological-sites": "archaeological_sites.json",
    "monuments": "monuments.json",
    "sunken-monuments": "sunken_monuments.json"
}

CHECKPOINT_FILES = {
    "museums": "museums_checkpoint.json",
    "archaeological-sites": "archaeological_sites_checkpoint.json", 
    "monuments": "monuments_checkpoint.json",
    "sunken-monuments": "sunken_monuments_checkpoint.json"
}

# Scraping settings
SCROLL_ATTEMPTS = 3
SCROLL_DELAY = 1
REQUEST_DELAY = 1
DEFAULT_TIMEOUT = 20

# Time constants
WEEK_DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# CSS Selectors
SELECTORS = {
    "listing_container": "div.listing.treasureListing",
    "list_items": "a.listItem",
    "title": ".mainPageTitle h1",
    "location": ".itemInfo",
    "description_container": ".txtSection",
    "description_paragraphs": "p",
    "opening_hours": ".openingHoursSec .dayOff-fromTo.fromTo",
    "prices": ".ticketPriceItem span",
    "services_slider": ".servicesSlider",
    "services_slides": ".slick-slide",
    "services_details": ".servicesDetails",
    "services_headings": "h2, h3, strong",
    "services_content": "p, li"
}