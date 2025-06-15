import  os
from dotenv import load_dotenv

# Load environment variables
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
 