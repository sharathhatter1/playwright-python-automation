#  Python Test Automation Framework

A comprehensive test automation framework built with Python, Pytest, and Playwright for testing web applications. This framework follows industry standards and best practices for automated testing.

## Features

- **Modular and Scalable**: Easy to add new tests without rewriting existing code
- **Page Object Model**: Well-organized page objects for better maintainability
- **Cross-browser Testing**: Support for Chromium, Firefox, and WebKit
- **Parallel Execution**: Run tests in parallel for faster execution
- **Parameterized Tests**: Run tests with different data sets
- **Rich Reporting**: Allure and HTML reports
- **Screenshots and Videos**: Capture on test failure
- **Environment Configuration**: Support for multiple environments
- **Jenkins Integration**: Ready for CI/CD

## Prerequisites

- Python 3.8 or higher
- Pip package manager

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:

```bash
playwright install
```

## Running Tests

### Using the run_tests.py script

```bash
# Run all tests with default settings
python run_tests.py

# Run specific tests
python run_test_with_params.py --browser firefox --parallel 2 --test_file tests/test_simple.py --headless false --allure

# Run with reporting
python run_tests.py --allure --html
```

### Using pytest directly

```bash
# Run all tests
pytest

# Run specific marker
pytest -m search

# Run in parallel
pytest -n 4
```

## Environment Configuration

The framework uses a `.env` file for configuration with sensible defaults. You can:

1. Use the default values without any configuration
2. Create a `.env` file based on `.env.example`
3. Override values via command line
4. Set environment variables directly

Example `.env` file:

```
# Browser Configuration
BROWSER=chromium
HEADLESS=true
SLOWMO=0
TIMEOUT=30000

# Test Environment
BASE_URL=https://automationexercise.com
ENVIRONMENT=staging

# Debug Options
SCREENSHOT_ON_FAILURE=true
TRACING=false
VIDEO=false
```

## Jenkins Integration

The project includes a `Jenkinsfile` for CI/CD integration. To use it:

1. Set up a Jenkins server with the required plugins (Allure, Docker)
2. Create a Jenkins pipeline job using the provided `Jenkinsfile`
3. Run the pipeline with your desired parameters

The included `Dockerfile.agent` creates a Jenkins agent with all necessary dependencies.

## Project Structure

```
├── conftest.py           # Pytest configuration and fixtures
├── .env                  # Environment variables
├── .env.example          # Example environment configuration
├── Jenkinsfile           # Jenkins pipeline configuration
├── pytest.ini           # Pytest configuration
├── README.md            # Project documentation
├── requirements.txt     # Dependencies
├── run_tests.py         # Test runner script
├── jenkins/             # Jenkins configuration files
│   └── Dockerfile.agent # Docker image for Jenkins agent
├── src/                 # Source code
│   ├── pages/           # Page objects
│   │   ├── base_page.py
│   │   ├── cart_page.py
│   │   ├── checkout_page.py
│   │   ├── home_page.py
│   │   ├── login_page.py
│   │   └── products_page.py
│   └── utils/           # Utilities
│       ├── logger.py
│       ├── screenshot_helper.py
│       └── test_data.py
└── tests/               # Test cases
    ├── test_cart.py
    ├── test_checkout.py
    ├── test_search.py
    └── test_smoke.py
```
 
