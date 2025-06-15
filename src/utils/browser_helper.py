from  playwright.sync_api import sync_playwright
import os
import allure

def get_browser(browser_name=None):
    """Initialize browser based on environment variable or parameter"""
    if not browser_name:
        browser_name = os.getenv("BROWSER", "chromium").lower()
    
    # Explicitly check for "false" string to ensure headless=False works correctly
    headless_value = os.getenv("HEADLESS", "true").lower()
    headless = headless_value == "true"
    
    playwright = sync_playwright().start()
    
    if browser_name == "firefox":
        return playwright, playwright.firefox.launch(headless=headless)
    elif browser_name == "webkit":
        return playwright, playwright.webkit.launch(headless=headless)
    else:  # default to chromium
        return playwright, playwright.chromium.launch(headless=headless)
 