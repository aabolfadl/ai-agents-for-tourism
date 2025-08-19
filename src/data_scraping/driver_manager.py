"""WebDriver management utilities."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


class DriverManager:
    """Manages Chrome WebDriver instances with consistent configuration."""
    
    @staticmethod
    def create_driver():
        """Create a new Chrome WebDriver instance with optimal settings."""
        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=opts)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    
    @staticmethod
    def wait_for_element(driver, selector, timeout=20):
        """Wait for an element to be present on the page."""
        wait = WebDriverWait(driver, timeout)
        try:
            return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        except TimeoutException:
            # Give it one more chance with a short sleep
            time.sleep(2)
            return None
    
    @staticmethod
    def scroll_to_load_content(driver, attempts=3, delay=1):
        """Scroll to bottom of page to trigger lazy loading."""
        for _ in range(attempts):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(delay)