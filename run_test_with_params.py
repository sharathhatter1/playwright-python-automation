#!/usr/bin/env  python3
import os
import sys
import subprocess
import argparse

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Run tests with specific browser in parallel")
    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"], 
                      default="chromium", help="Browser to use for tests")
    parser.add_argument("--parallel", type=int, default=1, 
                      help="Number of parallel workers (default: 1)")
    parser.add_argument("--headless", type=str, choices=["true", "false"], default="true",
                      help="Run in headless mode (default: true)")
    parser.add_argument("--allure", action="store_true", 
                      help="Generate Allure report")
    parser.add_argument("--test_file", default="tests/test_smoke.py",
                      help="Test file to run (default: tests/test_smoke.py)")
    parser.add_argument("--test_mark", 
                      help="Run tests with specific marker (e.g. smoke, search)")
    return parser.parse_args()

def run_test_with_params():
    """Run the test with specified parameters"""
    args = parse_args()
    
    # Build the pytest command
    cmd = f"python -m pytest {args.test_file} -v"
    
    # Add test marker if specified
    if args.test_mark:
        cmd += f" -m {args.test_mark}"
    
    # Add parallel execution if requested
    if args.parallel > 1:
        cmd += f" -n {args.parallel}"
    
    # Add Allure reporting if requested
    if args.allure:
        os.makedirs("allure-results", exist_ok=True)
        cmd += " --alluredir=allure-results"
    
    # Set environment variables for the browser
    os.environ["BROWSER"] = args.browser
    
    # Get headless mode from command line or environment
    headless = args.headless.lower()
    if "HEADLESS" in os.environ:
        headless = os.environ["HEADLESS"].lower()
    os.environ["HEADLESS"] = headless
    
    print(f"Running tests with browser: {args.browser}")
    print(f"Headless mode: {headless}")
    print(f"Parallel workers: {args.parallel}")
    print(f"Command: {cmd}")
    
    # Run the command
    result = subprocess.run(cmd, shell=True)
    
    # Generate Allure report if requested
    if args.allure and result.returncode == 0:
        print("Generating Allure report...")
        subprocess.run("allure generate allure-results --clean -o allure-report", shell=True)
        print("Allure report generated in allure-report directory")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_test_with_params())
 