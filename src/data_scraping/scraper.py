"""Main scraper class that orchestrates the scraping process."""

import time
from urllib.parse import urljoin
from typing import List, Dict, Any
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException

from driver_manager import DriverManager
from extractors import DataExtractor
from data_manager import DataManager
from config import SELECTORS, REQUEST_DELAY, SCROLL_ATTEMPTS, SCROLL_DELAY, DEFAULT_TIMEOUT


class EgyptMonumentsScraper:
    """Main scraper class for Egyptian monuments website."""
    
    def __init__(self, site_type: str, base_url: str, checkpoint_file: str, output_file: str):
        self.site_type = site_type
        self.base_url = base_url
        self.data_manager = DataManager(checkpoint_file, output_file)
        self.extractor = DataExtractor()
    
    def get_site_list(self) -> List[Dict[str, Any]]:
        """Get list of all sites from the main listing page."""
        driver = DriverManager.create_driver()
        try:
            print(f"Loading main page: {self.base_url}")
            driver.get(self.base_url)
            
            # Wait for the listing container to load
            DriverManager.wait_for_element(driver, SELECTORS["listing_container"])
            
            # Scroll to load lazy-loaded content
            DriverManager.scroll_to_load_content(driver, SCROLL_ATTEMPTS, SCROLL_DELAY)
            
            # Find the listing container and extract items
            try:
                listing_div = driver.find_element(By.CSS_SELECTOR, SELECTORS["listing_container"])
                items = listing_div.find_elements(By.CSS_SELECTOR, SELECTORS["list_items"])
            except NoSuchElementException:
                print(f"Warning: Could not find listing container for {self.site_type}")
                return []
            
            sites = []
            seen_urls = set()
            
            for item in items:
                href = item.get_attribute("href") or ""
                full_url = urljoin(self.base_url, href)
                
                if full_url in seen_urls or not full_url.startswith("http"):
                    continue
                    
                seen_urls.add(full_url)
                sites.append({"name": None, "url": full_url})
            
            print(f"Found {len(sites)} {self.site_type} on main page")
            return sites
            
        except WebDriverException as e:
            print(f"Error loading main page: {e}")
            return []
        finally:
            driver.quit()
    
    def extract_site_details(self, url: str, timeout: int = DEFAULT_TIMEOUT) -> Dict[str, Any]:
        """Extract detailed information from a single site page."""
        driver = DriverManager.create_driver()
        try:
            print(f"Extracting details from: {url}")
            driver.get(url)
            
            # Wait for main content to load
            DriverManager.wait_for_element(driver, SELECTORS["title"], timeout)
            
            # Extract all data using the DataExtractor
            details = {
                "url": url,
                "name": self.extractor.extract_name(driver),
                "location": self.extractor.extract_location(driver),
                "description": self.extractor.extract_description(driver),
                "opening_hours": self.extractor.extract_opening_hours(driver),
                "prices": self.extractor.extract_prices(driver),
                "services": self.extractor.extract_services(driver),
            }
            
            return details
            
        except WebDriverException as e:
            print(f"Error extracting details from {url}: {e}")
            raise
        finally:
            driver.quit()
    
    def scrape_all(self) -> None:
        """Main method to scrape all sites of the given type."""
        print(f"Starting scrape of {self.site_type}")
        
        # Get list of all sites
        all_sites = self.get_site_list()
        if not all_sites:
            print(f"No sites found for {self.site_type}")
            return
        
        # Load existing progress
        results = self.data_manager.load_checkpoint()
        initial_count = len(results)
        
        if initial_count > 0:
            print(f"Resuming from checkpoint with {initial_count} entries")
        
        # Process each site
        for i, site in enumerate(all_sites, 1):
            url = site["url"]
            
            if url in results:
                print(f"[{i}/{len(all_sites)}] Skipping already scraped: {url}")
                continue
            
            try:
                print(f"[{i}/{len(all_sites)}] Scraping: {url}")
                details = self.extract_site_details(url)
                results[url] = details
                
                # Save progress after each successful extraction
                self.data_manager.save_checkpoint(results)
                
                # Be respectful to the server
                time.sleep(REQUEST_DELAY)
                
            except WebDriverException as e:
                print(f"Error scraping {url}: {e}")
                continue
            except KeyboardInterrupt:
                print("\nScraping interrupted by user. Progress saved to checkpoint.")
                break
            except Exception as e:
                print(f"Unexpected error scraping {url}: {e}")
                continue
        
        # Save final results
        final_count = len(results)
        if final_count > initial_count:
            self.data_manager.save_final_results(results)
            print(f"Scraping completed. Added {final_count - initial_count} new entries.")
        else:
            print("No new entries were scraped.")
    
    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about the current checkpoint data."""
        data = self.data_manager.load_checkpoint()
        return {
            "total_entries": len(data),
            "entries_with_services": sum(1 for entry in data.values() if entry.get("services")),
            "entries_with_hours": sum(1 for entry in data.values() if entry.get("opening_hours")),
            "entries_with_prices": sum(1 for entry in data.values() if entry.get("prices"))
        }