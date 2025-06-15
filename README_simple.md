#  Simple Playwright Test Example

This is a standalone example of how to use Playwright with Python for automated testing.

## Setup

1. Install the required packages:

```bash
pip install -r requirements_simple.txt
```

2. Install Playwright browsers:

```bash
playwright install chromium
```

## Running the Test

You can run the test directly:

```bash
python simple_test.py
```

Or using pytest:

```bash
pytest simple_test.py -v
```

## What the Test Does

1. Opens the Automation Exercise website
2. Navigates to the Products page
3. Searches for "tops"
4. Takes a screenshot of the search results
5. Adds the first product to the cart

## Features Demonstrated

- Browser automation with Playwright
- Page navigation
- Form filling
- Element interaction (clicks, hovers)
- Screenshots
- Verification using expect assertions
 