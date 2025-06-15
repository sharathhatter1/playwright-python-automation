"""
A  simple test file that can be executed with command line parameters.
Run with: python run_test_with_params.py --browser firefox --parallel 2 --test_file tests/test_simple.py
"""

import pytest
import allure
import os
from playwright.sync_api import Page, expect
from src.utils.browser_helper import get_browser
from src.pages.home_page import HomePage
from src.pages.products_page import ProductsPage
from src.pages.cart_page import CartPage

# Base URL for automation exercise
BASE_URL = "https://automationexercise.com"

@allure.feature("Simple Tests")
class TestSimpleExample:
    """Simple test examples that can run with any browser"""
    
    @pytest.mark.smoke
    @allure.title("Test search for product")
    @allure.description("Test searching for a product and verifying results")
    def test_search_product(self, page: Page):
        """Test searching for a product"""
        # Arrange
        home_page = HomePage(page)
        products_page = ProductsPage(page)
        search_term = "t-shirt"
        
        # Act
        home_page.navigate_to(f"{BASE_URL}/products")
        products_page.search_product(search_term)
        
        # Assert
        search_results = page.locator(products_page.search_result)
        expect(search_results).to_have_count(greater_than=0)
        
        # Take screenshot of results
        screenshot_path = f"screenshots/{os.getenv('BROWSER', 'browser')}_search_results.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        page.screenshot(path=screenshot_path)
        
        # Attach screenshot to Allure report
        allure.attach.file(screenshot_path, 
                          name=f"Search Results for {search_term}", 
                          attachment_type=allure.attachment_type.PNG)
    
    @pytest.mark.cart
    @allure.title("Test add to cart")
    @allure.description("Test adding a product to cart and verifying it was added")
    def test_add_to_cart(self, page: Page):
        """Test adding a product to cart"""
        # Arrange
        home_page = HomePage(page)
        products_page = ProductsPage(page)
        cart_page = CartPage(page)
        
        # Act
        home_page.navigate_to(f"{BASE_URL}/products")
        products_page.add_first_product_to_cart()
        products_page.go_to_cart()
        
        # Assert
        cart_items = page.locator(cart_page.cart_items)
        expect(cart_items).to_have_count(greater_than=0)
        
        # Take screenshot of cart
        screenshot_path = f"screenshots/{os.getenv('BROWSER', 'browser')}_cart.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        page.screenshot(path=screenshot_path)
        
        # Attach screenshot to Allure report
        allure.attach.file(screenshot_path, 
                          name="Product added to cart", 
                          attachment_type=allure.attachment_type.PNG)

@pytest.fixture(scope="function")
def page(browser):
    """Create a new page for each test"""
    page = browser.new_page()
    page.set_default_timeout(30000)
    yield page
    page.close()

@pytest.fixture(scope="module")
def browser():
    """Initialize browser based on environment variable"""
    playwright, browser = get_browser()
    yield browser
    browser.close()
    playwright.stop()
 