#!/usr/bin/env  python3
import os
import sys
import argparse
import subprocess
from dotenv import load_dotenv

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Run automated tests with Playwright")
    
    # Browser selection
    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"], 
                        default="chromium", help="Browser to use for tests")
    
    # Test selection
    parser.add_argument("--test", help="Run specific test file or directory")
    parser.add_argument("--marker", help="Run tests with specific marker")
    
    # Environment selection
    parser.add_argument("--env", choices=["local", "dev", "staging", "prod"], 
                        default="staging", help="Environment to run tests against")
    
    # Debug options
    parser.add_argument("--headed", action="store_true", help="Run in headed mode")
    parser.add_argument("--slowmo", type=int, default=0, help="Slow down execution by ms")
    parser.add_argument("--screenshot", action="store_true", help="Take screenshots on failure")
    parser.add_argument("--video", action="store_true", help="Record video of tests")
    parser.add_argument("--trace", action="store_true", help="Record trace of tests")
    
    # Report options
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--allure", action="store_true", help="Generate Allure report")
    
    # Parallel execution
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel workers")
    
    return parser.parse_args()

def setup_env_vars(args):
    """Set environment variables based on command line arguments"""
    # Load existing .env file if available
    load_dotenv()
    
    # Set environment variables from arguments
    os.environ["BROWSER"] = args.browser
    os.environ["HEADLESS"] = "false" if args.headed else "true"
    os.environ["SLOWMO"] = str(args.slowmo)
    os.environ["ENVIRONMENT"] = args.env
    os.environ["SCREENSHOT_ON_FAILURE"] = "true" if args.screenshot else "false"
    os.environ["VIDEO"] = "true" if args.video else "false"
    os.environ["TRACING"] = "true" if args.trace else "false"
    
    # Set environment-specific base URL
    if args.env == "local":
        os.environ["BASE_URL"] = os.getenv("LOCAL_URL", "http://localhost:3000")
    elif args.env == "dev":
        os.environ["BASE_URL"] = os.getenv("DEV_URL", "https://dev-automationexercise.com")
    elif args.env == "staging":
        os.environ["BASE_URL"] = os.getenv("STAGING_URL", "https://automationexercise.com")
    elif args.env == "prod":
        os.environ["BASE_URL"] = os.getenv("PROD_URL", "https://automationexercise.com")

def build_pytest_command(args):
    """Build pytest command based on arguments"""
    cmd = ["pytest"]
    
    # Test selection
    if args.test:
        cmd.append(args.test)
    
    if args.marker:
        cmd.append(f"-m {args.marker}")
    
    # Parallel execution
    if args.workers > 1:
        cmd.append(f"-n {args.workers}")
    
    # Reporting options
    if args.html:
        cmd.append("--html=reports/report.html")
    
    if args.allure:
        cmd.append("--alluredir=allure-results")
    
    # Verbosity
    cmd.append("-v")
    
    return " ".join(cmd)

def run_tests():
    """Main function to run tests"""
    args = parse_args()
    setup_env_vars(args)
    
    # Ensure directories exist
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("videos", exist_ok=True)
    os.makedirs("traces", exist_ok=True)
    os.makedirs("allure-results", exist_ok=True)
    
    # Build and run pytest command
    cmd = build_pytest_command(args)
    print(f"Running command: {cmd}")
    
    result = subprocess.run(cmd, shell=True)
    
    # Generate Allure report if requested
    if args.allure:
        print("Generating Allure report...")
        subprocess.run("allure generate allure-results --clean -o allure-report", shell=True)
        print("Allure report generated in allure-report directory")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())
 