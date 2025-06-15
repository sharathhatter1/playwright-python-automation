import  allure
import logging
from src.utils.logger import Logger

class BasePage:
    """Base page for all page objects"""
    
    def __init__(self, page):
        self.page = page
        self.logger = Logger.get_logger(self.__class__.__name__)
    
    @allure.step("Wait for page to load")
    def wait_for_page_load(self):
        """Wait for page to load completely"""
        self.page.wait_for_load_state("networkidle")
    
    @allure.step("Wait for selector: {selector}")
    def wait_for_selector(self, selector, state="visible", timeout=10000):
        """Wait for an element to be visible"""
        self.logger.info(f"Waiting for selector: {selector}")
        return self.page.wait_for_selector(selector, state=state, timeout=timeout)
    
    @allure.step("Click on element: {selector}")
    def click(self, selector):
        """Click on an element"""
        self.logger.info(f"Clicking on: {selector}")
        self.page.click(selector)
    
    @allure.step("Fill text: {value} in field: {selector}")
    def fill(self, selector, value):
        """Fill a text field"""
        self.logger.info(f"Filling {selector} with: {value}")
        self.page.fill(selector, value)
    
    @allure.step("Get text from element: {selector}")
    def get_text(self, selector):
        """Get text from an element"""
        self.logger.info(f"Getting text from: {selector}")
        return self.page.text_content(selector)
    
    @allure.step("Check if element exists: {selector}")
    def is_visible(self, selector, timeout=5000):
        """Check if an element is visible"""
        self.logger.info(f"Checking if visible: {selector}")
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except:
            return False
    
    @allure.step("Get count of elements: {selector}")
    def get_count(self, selector):
        """Get count of elements matching a selector"""
        self.logger.info(f"Getting count of: {selector}")
        return self.page.locator(selector).count()
    
    @allure.step("Take screenshot: {name}")
    def take_screenshot(self, name):
        """Take a screenshot"""
        self.logger.info(f"Taking screenshot: {name}")
        return self.page.screenshot_helper.take_screenshot(name)
    
    @allure.step("Navigate to URL: {url}")
    def navigate_to(self, url):
        """Navigate to a URL"""
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url)
        self.wait_for_page_load()
 