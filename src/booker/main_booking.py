"""
Main booking script for EgyMonuments automation.

This script orchestrates the booking process by using the utilities
from web_utils.py to perform the complete booking workflow.
"""

import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import our web utilities
from web_utils import web_driver, load_bookings, book_location


def complete_checkout(driver, wait):
    """
    Complete the checkout process by opening cart and proceeding to checkout.
    
    Args:
        driver: Selenium WebDriver instance
        wait: WebDriverWait instance
        
    Returns:
        bool: True if checkout completed successfully, False otherwise
    """
    try:
        # Step 7: Go to Cart
        cart_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='pull-right' and contains(text(), 'CART')]")
        ))
        driver.execute_script("arguments[0].click();", cart_button)
        print("Opened cart.")
        
        # Step 8: Checkout
        checkout_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Checkout') and contains(@class, 'btn-cart-next')]")
        ))
        driver.execute_script("arguments[0].click();", checkout_button)
        print("Proceeded to checkout.")
        
        print("Next page URL:", driver.current_url)
        return True
        
    except Exception as e:
        print(f"Error during checkout: {e}")
        return False


def main():
    """
    Main function that runs the complete booking automation process.
    """
    # Initialize WebDriver
    driver = web_driver()
    wait = WebDriverWait(driver, 10)
    
    try:
        # Navigate to the locations page
        driver.get('https://egymonuments.com/locations')
        print("Navigated to EgyMonuments locations page")
        
        # Load booking data from JSON file
        try:
            with open("planning_agent/booking_details.json", "r") as f:
                booking_data = json.load(f)
            print(f"Loaded {len(booking_data)} booking entries")
        except FileNotFoundError:
            print("❌ Error: booking_details file not found")
            return
        except json.JSONDecodeError:
            print("❌ Error: Invalid JSON format in booking_details")
            return
        
        # Process each booking entry
        successful_bookings = 0
        failed_bookings = 0
        
        for i, entry in enumerate(booking_data, 1):
            print(f"\n--- Processing booking {i}/{len(booking_data)} ---")
            print(f"Location: {entry.get('location', 'Unknown')}")
            
            try:
                book_location(driver, wait, entry)
                successful_bookings += 1
                print(f"✅ Booking {i} completed successfully")
            except Exception as e:
                failed_bookings += 1
                print(f"❌ Booking {i} failed: {e}")
        
        # Print booking summary
        print(f"\n{'='*50}")
        print("BOOKING SUMMARY")
        print(f"{'='*50}")
        print(f"Total bookings processed: {len(booking_data)}")
        print(f"Successful bookings: {successful_bookings}")
        print(f"Failed bookings: {failed_bookings}")
        print(f"Success rate: {(successful_bookings/len(booking_data)*100):.1f}%")
        
        # Complete checkout process if any bookings were successful
        if successful_bookings > 0:
            print(f"\n--- Completing checkout process ---")
            checkout_success = complete_checkout(driver, wait)
            
            if checkout_success:
                print("✅ Checkout process completed successfully")
            else:
                print("❌ Checkout process failed")
        else:
            print("❌ No successful bookings to checkout")
        
        # Wait for user input before closing
        input("Press Enter to close the browser...")
        
    except KeyboardInterrupt:
        print("\n❌ Process interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Clean up - close the browser
        try:
            driver.quit()
            print("Browser closed successfully")
        except Exception as e:
            print(f"Error closing browser: {e}")


if __name__ == "__main__":
    main()