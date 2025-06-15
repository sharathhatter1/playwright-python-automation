import  os
import allure
from datetime import datetime

class ScreenshotHelper:
    def __init__(self, page):
        self.page = page
        self.screenshot_dir = "screenshots"
        
        # Create screenshots directory if it doesn't exist
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
    
    def take_screenshot(self, name):
        """Take a screenshot of the entire page"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshot_dir}/{name}_{timestamp}.png"
        self.page.screenshot(path=filename)
        
        # Attach to Allure report
        allure.attach.file(filename, name=name, attachment_type=allure.attachment_type.PNG)
        
        return filename
    
    def take_element_screenshot(self, selector, name):
        """Take a screenshot of a specific element"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshot_dir}/{name}_{timestamp}.png"
        
        # Locate element and take screenshot
        element = self.page.locator(selector)
        element.screenshot(path=filename)
        
        # Attach to Allure report
        allure.attach.file(filename, name=name, attachment_type=allure.attachment_type.PNG)
        
        return filename
 