import  pytest
import allure
from src.pages.home_page import HomePage
from src.pages.products_page import ProductsPage
from src.pages.cart_page import CartPage
from src.utils.test_data import TestData

@allure.feature("Shopping Cart")
class TestCart:
    
    @pytest.mark.cart
    @allure.title("Test add product to cart")
    @allure.description("Test adding a product to the cart and verifying it appears correctly")
    def test_add_to_cart(self, page):
        # Arrange
        home_page = HomePage(page)
        products_page = ProductsPage(page)
        cart_page = CartPage(page)
        
        # Act
        home_page.go_to_products()
        product_name = TestData.TEST_PRODUCTS[0]  # Use first test product
        
        # Add product to cart
        products_page.add_to_cart(product_name)
        products_page.go_to_cart()
        
        # Assert
        assert cart_page.is_loaded(), "Cart page did not load correctly"
        assert cart_page.is_product_in_cart(product_name), f"Product '{product_name}' not found in cart"
        
        # Take screenshot of cart
        cart_page.take_screenshot("product_in_cart")
    
    @pytest.mark.cart
    @allure.title("Test add multiple products to cart")
    @allure.description("Test adding multiple products to the cart and verifying they appear correctly")
    def test_add_multiple_products(self, page):
        # Arrange
        home_page = HomePage(page)
        products_page = ProductsPage(page)
        cart_page = CartPage(page)
        
        # Act
        home_page.go_to_products()
        
        # Add all test products to cart
        for product_name in TestData.TEST_PRODUCTS:
            products_page.add_to_cart(product_name)
        
        products_page.go_to_cart()
        
        # Assert
        assert cart_page.is_loaded(), "Cart page did not load correctly"
        
        # Check all products are in cart
        for product_name in TestData.TEST_PRODUCTS:
            assert cart_page.is_product_in_cart(product_name), f"Product '{product_name}' not found in cart"
        
        # Check cart count matches expected
        cart_count = cart_page.get_cart_items_count()
        assert cart_count == len(TestData.TEST_PRODUCTS), f"Cart count {cart_count} doesn't match expected {len(TestData.TEST_PRODUCTS)}"
    
    @pytest.mark.cart
    @allure.title("Test remove product from cart")
    @allure.description("Test removing a product from the cart")
    def test_remove_from_cart(self, page):
        # Arrange
        home_page = HomePage(page)
        products_page = ProductsPage(page)
        cart_page = CartPage(page)
        
        # Add product to cart
        home_page.go_to_products()
        product_name = TestData.TEST_PRODUCTS[0]
        products_page.add_to_cart(product_name)
        products_page.go_to_cart()
        
        # Verify product is in cart before removing
        assert cart_page.is_product_in_cart(product_name), f"Product '{product_name}' not found in cart"
        
        # Act - remove product
        cart_page.remove_product(product_name)
        
        # Assert
        assert not cart_page.is_product_in_cart(product_name), f"Product '{product_name}' still in cart after removal"
 