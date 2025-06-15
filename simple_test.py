#!/usr/bin/env  python3
"""
Simple standalone test script using Playwright and pytest.
This file can be run directly without the full framework.
"""

import os
import time
import pytest
from playwright.sync_api import sync_playwright, expect

class TestSimpleExample:
    """Simple test examples that can run standalone"""
    
    def test_search_product(self):
        """Test searching for a product on the automation exercise site"""
        # Setup
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            try:
                # Navigate to website
                print("Navigating to website...")
                page.goto("https://automationexercise.com")
                
                # Verify homepage loaded
                expect(page.locator(".logo")).to_be_visible()
                print("Homepage loaded successfully")
                
                # Go to Products page
                print("Going to Products page...")
                page.click("a[href='/products']")
                page.wait_for_load_state("networkidle")
                
                # Search for a product
                search_term = "tops"
                print(f"Searching for '{search_term}'...")
                page.fill("#search_product", search_term)
                page.click("#submit_search")
                page.wait_for_load_state("networkidle")
                
                # Take screenshot of results
                os.makedirs("screenshots", exist_ok=True)
                screenshot_path = f"screenshots/search_results_{int(time.time())}.png"
                page.screenshot(path=screenshot_path)
                print(f"Screenshot saved to {screenshot_path}")
                
                # Verify search results
                results = page.locator(".features_items .product-image-wrapper")
                count = results.count()
                print(f"Found {count} products matching '{search_term}'")
                
                # Add first product to cart
                if count > 0:
                    print("Adding first product to cart...")
                    page.hover(".features_items .product-image-wrapper:first-child")
                    page.click(".features_items .product-image-wrapper:first-child .add-to-cart")
                    
                    # Wait for modal and click continue shopping
                    page.wait_for_selector(".modal-content", state="visible")
                    page.click(".btn-success")
                    print("Product added to cart successfully")
                
            finally:
                # Clean up
                browser.close()
                print("Test completed")

if __name__ == "__main__":
    # Run the test directly
    test = TestSimpleExample()
    test.test_search_product()
    print("\nTo run with pytest: pytest simple_test.py -v")
 