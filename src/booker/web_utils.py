"""
Web automation utilities for EgyMonuments booking system.

This module contains utility functions for web driver setup,
element finding, and basic web interactions.
"""

import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


def web_driver():
    """
    Create and configure a Chrome WebDriver instance.
    
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def load_bookings(json_path):
    """
    Load booking entries from a JSON file.
    
    Args:
        json_path (str): Path to the JSON file containing booking data
        
    Returns:
        list: List of booking dictionaries loaded from JSON
    """
    with open(json_path, 'r') as f:
        return json.load(f)


def find_location_button(driver, wait, location_name):
    """
    Find and return the location button element matching the given name.
    
    Args:
        driver: Selenium WebDriver instance
        wait: WebDriverWait instance
        location_name (str): Name of the location to find
        
    Returns:
        WebElement or None: The location button element if found, None otherwise
    """
    try:
        location_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.p-2.w-100.align-self-center"))
        )
    except Exception:
        print("❌ Could not find any location elements.")
        return None

    target = location_name.strip().lower()
    for elem in location_elements:
        if elem.text.strip().lower() == target:
            print(f"✅ Found location: {elem.text}")
            return elem

    print(f"❌ Location '{location_name}' not found.")
    return None


def select_nationality(driver, nationality):
    """
    Select nationality button based on input.
    
    Args:
        driver: Selenium WebDriver instance
        nationality (str): Nationality to select ("egyptian", "arab", or other)
    """
    try:
        if nationality.lower() in ["egyptian", "arab", "egyptian/arab", "arabic"]:
            button = driver.find_element(By.XPATH, "//button[contains(text(), 'Egyptian')]")
        else:
            button = driver.find_element(By.XPATH, "//button[contains(text(), 'Other Nationality')]")
        driver.execute_script("arguments[0].click();", button)
        print(f"Clicked button for nationality: {nationality}")
    except NoSuchElementException:
        print("Nationality selection button not found.")


def book_location(driver, wait, entry):
    """
    Automate the booking process for a single entry.
    
    Args:
        driver: Selenium WebDriver instance
        wait: WebDriverWait instance
        entry (dict): Dictionary containing booking information with keys:
                     'location', 'date', 'adults', 'students', 'nationality'
    """
    location_name = entry["location"]
    target_date = entry["date"]  # e.g., "1754784000000"
    adults = entry["adults"]
    students = entry["students"]
    nationality = entry["nationality"]

    try:
        # Step 1: Find and click location
        location_button = find_location_button(driver, wait, location_name)
        if not location_button:
            print(f"Location '{location_name}' not found.")
            return
        driver.execute_script("arguments[0].click();", location_button)
        print("New page URL (via JS click):", driver.current_url)

        # Step 2: Click "Book Now"
        try:
            book_now_button = driver.find_element(By.CSS_SELECTOR, "a.btn-get-download")
            driver.execute_script("arguments[0].click();", book_now_button)
            print("Redirected to booking page URL:", driver.current_url)
        except NoSuchElementException:
            print("Book Now button not found.")
            return

        # Step 3: Select nationality
        select_nationality(driver, nationality)

        # Step 4: Select date
        try:
            date_element = driver.find_element(By.CSS_SELECTOR, f'td.day[data-date="{target_date}"]')
            driver.execute_script("arguments[0].click();", date_element)
            selected_date = driver.find_element(By.ID, "selectedDate").get_attribute("value")
            print("Selected date:", selected_date)
        except NoSuchElementException:
            print(f"Date not selectable: {target_date}")
            return

        # Step 5: Add adults and students
        plus_buttons = driver.find_elements(By.CSS_SELECTOR, "input.plus")
        if len(plus_buttons) >= 2:
            for _ in range(adults):
                driver.execute_script("arguments[0].click();", plus_buttons[0])
            for _ in range(students):
                driver.execute_script("arguments[0].click();", plus_buttons[1])
            print(f"Added {adults} adults and {students} students.")
        else:
            print("Plus buttons not found.")
            return

        # Step 6: Click Add to Cart & Continue
        continue_button = wait.until(EC.element_to_be_clickable((By.ID, "button1")))
        driver.execute_script("arguments[0].click();", continue_button)
        print("Clicked Add to cart & continue booking.")

    except Exception as e:
        print("Unexpected error during booking:", e)