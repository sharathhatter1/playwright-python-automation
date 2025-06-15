import  os
import pytest
import allure
from datetime import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def get_config():
    """
    Get configuration from environment variables with defaults
    """
    return {
        "browser_name": os.getenv("BROWSER", "chromium"),
        "headless": os.getenv("HEADLESS", "true").lower() == "true",
        "slow_mo": int(os.getenv("SLOWMO", "0")),
        "timeout": int(os.getenv("TIMEOUT", "30000")),
        "viewport": {"width": 1280, "height": 720},
        "base_url": os.getenv("BASE_URL", "https://automationexercise.com"),
        "screenshot": os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true",
        "trace": os.getenv("TRACING", "false").lower() == "true",
        "video": os.getenv("VIDEO", "false").lower() == "true",
    }

def get_browser_args():
    """
    Get browser-specific launch arguments
    """
    browser_name = os.getenv("BROWSER", "chromium")
    args = {}
    
    if browser_name == "chromium":
        args["args"] = [
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-gpu",
            "--disable-web-security",
            "--disable-features=IsolateOrigins,site-per-process"
        ]
    
    return args

@pytest.fixture(scope="session")
def env():
    """Return environment configuration"""
    return get_config()

@pytest.fixture(scope="session")
def playwright_browser_type():
    """Fixture to provide browser type"""
    config = get_config()
    browser_name = config["browser_name"]
    
    with sync_playwright() as playwright:
        if browser_name == "chromium":
            yield playwright.chromium
        elif browser_name == "firefox":
            yield playwright.firefox
        elif browser_name == "webkit":
            yield playwright.webkit
        else:
            yield playwright.chromium

@pytest.fixture(scope="function")
def browser(playwright_browser_type):
    """Fixture to provide browser instance"""
    config = get_config()
    browser_args = get_browser_args()
    
    browser = playwright_browser_type.launch(
        headless=config["headless"],
        slow_mo=config["slow_mo"],
        **browser_args
    )
    
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    """Fixture to provide page instance"""
    config = get_config()
    
    context = browser.new_context(
        viewport=config["viewport"],
        record_video_dir="videos/" if config["video"] else None
    )
    
    if config["trace"]:
        context.tracing.start(screenshots=True, snapshots=True)
    
    page = context.new_page()
    page.set_default_timeout(config["timeout"])
    
    # Add screenshot helper as a page attribute
    from src.utils.screenshot_helper import ScreenshotHelper
    page.screenshot_helper = ScreenshotHelper(page)
    
    # Navigate to base URL
    page.goto(config["base_url"])
    
    yield page
    
    # Take screenshot on test failure if enabled
    if hasattr(pytest, "current_test") and pytest.current_test.failed and config["screenshot"]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshots/failure_{pytest.current_test.name}_{timestamp}.png"
        page.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name="screenshot", attachment_type=allure.attachment_type.PNG)
    
    # Stop tracing and save trace file if enabled
    if config["trace"] and hasattr(pytest, "current_test"):
        trace_path = f"traces/{pytest.current_test.name}.zip"
        context.tracing.stop(path=trace_path)
    
    context.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to store test result for later use in fixtures"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call":
        setattr(pytest, "current_test", item)
        setattr(pytest.current_test, "failed", rep.failed)
        setattr(pytest.current_test, "name", item.name)
 