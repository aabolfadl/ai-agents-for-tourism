"""Data extraction utilities for different types of content."""

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from config import SELECTORS, WEEK_DAYS


class DataExtractor:
    """Handles extraction of different data types from web pages."""
    
    @staticmethod
    def extract_name(driver):
        """Extract the name/title of the site."""
        try:
            name_el = driver.find_element(By.CSS_SELECTOR, SELECTORS["title"])
            return name_el.text.strip()
        except NoSuchElementException:
            return ""
    
    @staticmethod
    def extract_location(driver):
        """Extract location information."""
        try:
            loc_el = driver.find_element(By.CSS_SELECTOR, SELECTORS["location"])
            return loc_el.text.strip()
        except NoSuchElementException:
            return ""
    
    @staticmethod
    def extract_description(driver):
        """Extract description from paragraphs."""
        try:
            desc_container = driver.find_element(By.CSS_SELECTOR, SELECTORS["description_container"])
            paragraphs = desc_container.find_elements(By.TAG_NAME, SELECTORS["description_paragraphs"])
            return "\n".join(p.text.strip() for p in paragraphs if p.text.strip())
        except NoSuchElementException:
            return ""
    
    @staticmethod
    def extract_opening_hours(driver):
        """Extract opening hours information."""
        opening_hours = {}
        try:
            day_divs = driver.find_elements(By.CSS_SELECTOR, SELECTORS["opening_hours"])
            sample = None
            
            for div in day_divs:
                try:
                    from_block = div.find_element(By.XPATH, ".//div[./span[text()='From']]/p")
                    to_block = div.find_element(By.XPATH, ".//div[./span[text()='To']]/p")

                    def parse_time(block):
                        parts = block.text.strip().split()
                        if len(parts) >= 2:
                            return parts[0] + " " + parts[1]
                        return block.text.strip()

                    sample = {
                        "from": parse_time(from_block), 
                        "to": parse_time(to_block)
                    }
                    if sample["from"] and sample["to"]:
                        break
                except Exception:
                    continue
            
            if sample:
                for day in WEEK_DAYS:
                    opening_hours[day] = sample.copy()
                    
        except Exception:
            pass
        
        return opening_hours
    
    @staticmethod
    def extract_prices(driver):
        """Extract pricing information."""
        try:
            price_span = driver.find_element(By.CSS_SELECTOR, SELECTORS["prices"])
            raw = price_span.text.strip()
            # Clean up duplicate whitespace and normalize line breaks
            return "\n".join(line.strip() for line in raw.replace("\\", " ").splitlines() if line.strip())
        except NoSuchElementException:
            return ""
    
    @staticmethod
    def extract_services(driver):
        """Extract services information using multiple strategies."""
        services = []

        def add_service(txt):
            """Helper to clean and append unique services."""
            txt = txt.strip()
            if txt and txt not in services:
                services.append(txt)

        # Strategy 1: Try .servicesSlider
        try:
            time.sleep(0.5)  # Small wait in case it's injected late
            slider = driver.find_element(By.CSS_SELECTOR, SELECTORS["services_slider"])
            slides = slider.find_elements(By.CSS_SELECTOR, SELECTORS["services_slides"])
            
            for slide in slides:
                try:
                    title = ""
                    desc = ""

                    try:
                        title_el = slide.find_element(By.CSS_SELECTOR, "h3")
                        title = title_el.text.strip()
                    except:
                        pass
                    
                    try:
                        p_el = slide.find_element(By.CSS_SELECTOR, "p")
                        desc = p_el.text.strip()
                    except:
                        pass

                    if title or desc:
                        combined = title if title else ""
                        if desc:
                            combined = f"{combined}: {desc}" if title else desc
                        add_service(combined)
                except Exception:
                    continue
        except Exception:
            pass

        # Strategy 2: Fallback to .servicesDetails if nothing found
        if not services:
            try:
                details_containers = driver.find_elements(By.CSS_SELECTOR, SELECTORS["services_details"])
                for cont in details_containers:
                    try:
                        # Extract headings
                        for h in cont.find_elements(By.CSS_SELECTOR, SELECTORS["services_headings"]):
                            add_service(h.text.strip())
                        
                        # Extract paragraphs or list items
                        for p in cont.find_elements(By.CSS_SELECTOR, SELECTORS["services_content"]):
                            add_service(p.text.strip())
                        
                        # If still empty, grab whole container text
                        if not services:
                            add_service(cont.text.strip())
                    except Exception:
                        continue
            except Exception:
                pass

        return services