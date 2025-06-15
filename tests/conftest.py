import  pytest
from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
from datetime import datetime
import allure

load_dotenv()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # Test failed, capture screenshot
            page = item.funcargs.get("page")
            if page:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"screenshots/failure_{item.name}_{timestamp}.png"
                if not os.path.exists("screenshots"):
                    os.makedirs("screenshots")
                page.screenshot(path=screenshot_path)
                allure.attach.file(screenshot_path, name="screenshot", attachment_type=allure.attachment_type.PNG)

@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {
        "headless": os.getenv("HEADLESS", "true").lower() == "true",
        "slow_mo": int(os.getenv("SLOW_MO", "0")),
        "timeout": int(os.getenv("TIMEOUT", "30000")),
    }

@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
        "record_video_dir": "videos/" if os.getenv("VIDEO", "off") != "off" else None,
    }

@pytest.fixture(scope="function")
def page(browser, base_url):
    context = browser.new_context(
        record_video_dir="videos/" if os.getenv("VIDEO", "off") != "off" else None
    )
    page = context.new_page()
    page.goto(base_url)
    yield page
    context.close()

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://automationexercise.com")

@pytest.fixture(scope="session")
def env():
    return os.getenv("ENVIRONMENT", "staging")
 