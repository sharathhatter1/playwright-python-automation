#  Page Object Model

This framework uses the Page Object Model (POM) design pattern to create an abstraction layer for UI elements and actions. This helps make tests more maintainable, reusable, and readable.

## Basic Structure

```
src/
└── pages/
    ├── base_page.py
    ├── home_page.py
    ├── products_page.py
    ├── cart_page.py
    ├── checkout_page.py
    └── login_page.py
```

## Base Page

All page objects inherit from the `BasePage` class, which provides common functionality:

```python
class BasePage:
    def __init__(self, page):
        self.page = page
        self.logger = Logger.get_logger(self.__class__.__name__)
    
    def navigate_to(self, url):
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url)
    
    def click(self, selector):
        self.logger.info(f"Clicking on: {selector}")
        self.page.click(selector)
    
    def fill(self, selector, text):
        self.logger.info(f"Filling '{text}' into: {selector}")
        self.page.fill(selector, text)
    
    # ... other common methods
```

## Page Object Example

Here's an example of a page object for the product search page:

```python
class ProductsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Selectors
        self.products_title = ".title"
        self.product_list = ".features_items"
        self.add_to_cart_buttons = ".add-to-cart"
        self.view_product_buttons = ".choose a"
        self.product_info = ".productinfo"
        self.search_result = ".features_items .product-image-wrapper"
        
    def is_loaded(self):
        """Check if products page is loaded"""
        return self.is_visible(self.products_title)
    
    def get_product_count(self):
        """Get the number of products displayed"""
        products = self.page.query_selector_all(f"{self.product_list} .product-image-wrapper")
        return len(products)
    
    def add_product_to_cart(self, index=0):
        """Add a product to cart by index"""
        # Hover over the product to make add-to-cart button visible
        products = self.page.query_selector_all(self.product_info)
        if index < len(products):
            products[index].hover()
            add_buttons = self.page.query_selector_all(self.add_to_cart_buttons)
            add_buttons[index].click()
            self.logger.info(f"Added product at index {index} to cart")
            return True
        else:
            self.logger.error(f"Product index {index} not found")
            return False
    
    # ... other methods
```

## Best Practices

1. **Keep selectors at the top**: Define all selectors in the constructor for easy maintenance.

2. **Use descriptive method names**: Methods should describe the user action or business process they represent.

3. **Return values when appropriate**: Methods should return values that can be used for assertions in tests.

4. **Chain methods when possible**: Design methods to allow chaining for better readability.

5. **Include verification methods**: Add methods to verify page state (e.g., `is_loaded()`, `is_product_found()`).

6. **Handle errors gracefully**: Include error handling and logging in methods.

7. **Keep methods focused**: Each method should perform a single action or verification.

## Using Page Objects in Tests

Here's an example of using page objects in a test:

```python
def test_add_to_cart(page):
    # Initialize page objects
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    
    # Navigate to products page
    home_page.go_to_products()
    
    # Add product to cart
    products_page.add_product_to_cart(0)
    products_page.view_cart()
    
    # Verify product was added to cart
    assert cart_page.get_cart_item_count() > 0, "No items in cart after adding product"
```

## Benefits of Page Object Model

1. **Reduced code duplication**: Common interactions are defined once and reused.

2. **Improved maintainability**: When the UI changes, only the page object needs to be updated.

3. **Better readability**: Tests express intent clearly using business-oriented language.

4. **Separation of concerns**: Test logic is separated from page interactions.

5. **Easier test debugging**: When a test fails, it's easier to identify whether the issue is with the test or the application.
 