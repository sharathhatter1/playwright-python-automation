#  Test Examples

This document provides examples of using the test automation framework.

## Running Tests with pytest

You can directly use pytest to run tests, with various options:

### Basic Test Run

Run all tests:

```bash
pytest
```

### Run Specific Test Group

Run tests with a specific marker:

```bash
pytest -m smoke
pytest -m search
pytest -m cart
pytest -m checkout
```

### Run with Specific Browser

```bash
BROWSER=firefox pytest
BROWSER=webkit pytest
```

### Run in Headless/Headed Mode

```bash
HEADLESS=true pytest
HEADLESS=false pytest
```

### Run in Parallel

```bash
pytest -n 4
```

### Generate Reports

```bash
# Generate HTML report
pytest --html=report.html

# Generate Allure report
pytest --alluredir=allure-results
allure generate allure-results --clean -o allure-report
```

### Run Specific Test File

```bash
pytest tests/test_smoke.py
```

### Run Specific Test Function

```bash
pytest tests/test_smoke.py::TestSmoke::test_homepage_load
```

## Example Test Cases

### Basic Product Search Test

```python
@pytest.mark.search
def test_search_product(page):
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    
    # Search for a product
    home_page.search_product("t-shirt")
    
    # Verify search results
    assert products_page.is_product_found(), "No products found in search results"
    assert products_page.get_search_results_count() > 0, "Search results count should be greater than 0"
```

### Add to Cart Test

```python
@pytest.mark.cart
def test_add_to_cart(page):
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    
    # Navigate to products page
    home_page.go_to_products()
    
    # Add first product to cart
    products_page.add_product_to_cart(0)
    products_page.view_cart()
    
    # Verify product was added to cart
    assert cart_page.get_cart_item_count() > 0, "No items in cart after adding product"
```

### End-to-End Checkout Test

```python
@pytest.mark.checkout
@pytest.mark.e2e
def test_checkout_process(page):
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    
    # Add product to cart
    home_page.go_to_products()
    products_page.add_product_to_cart(0)
    products_page.view_cart()
    
    # Proceed to checkout
    cart_page.proceed_to_checkout()
    
    # Fill payment details
    checkout_page.place_order()
    checkout_page.fill_payment_details({
        "name_on_card": "Test User",
        "card_number": "4111111111111111",
        "cvc": "123",
        "expiry_month": "12",
        "expiry_year": "2025"
    })
    
    # Complete payment
    checkout_page.complete_payment()
    
    # Verify order was placed successfully
    assert checkout_page.is_order_placed(), "Order was not placed successfully"
```

## Parameterized Tests

```python
@pytest.mark.search
@pytest.mark.parametrize("search_term", ["t-shirt", "dress", "jeans", "tops"])
def test_search_multiple_terms(page, search_term):
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    
    # Search for the product
    home_page.search_product(search_term)
    
    # Log search results
    results_count = products_page.get_search_results_count()
    print(f"Search term '{search_term}' returned {results_count} results")
```

## Data-Driven Tests

```python
@pytest.mark.parametrize("product_index, expected_in_cart", [
    (0, True),
    (1, True),
    (5, True),
    (10, False)  # Assuming index 10 is out of bounds
])
def test_add_different_products(page, product_index, expected_in_cart):
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    
    # Navigate to products
    home_page.go_to_products()
    
    # Try to add product
    result = products_page.add_product_to_cart(product_index)
    
    # If expected to succeed, check cart
    if expected_in_cart:
        assert result, f"Failed to add product at index {product_index}"
        products_page.view_cart()
        assert cart_page.get_cart_item_count() > 0, "Cart is empty"
    else:
        assert not result, f"Should not be able to add product at index {product_index}"
```
 