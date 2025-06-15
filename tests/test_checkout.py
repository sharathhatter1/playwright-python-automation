import  pytest
import allure
from src.pages.home_page import HomePage
from src.pages.products_page import ProductsPage
from src.pages.cart_page import CartPage
from src.pages.login_page import LoginPage
from src.pages.checkout_page import CheckoutPage
from src.utils.test_data import TestData

@allure.feature("Checkout Process")
class TestCheckout:
    
    @pytest.mark.checkout
    @allure.title("Test checkout process")
    @allure.description("Test the complete checkout process from adding items to payment")
    def test_checkout_process(self, page):
        # Arrange
        home_page = HomePage(page)
        products_page = ProductsPage(page)
        cart_page = CartPage(page)
        checkout_page = CheckoutPage(page)
        login_page = LoginPage(page)
        
        # Login first (checkout requires account)
        home_page.go_to_login()
        login_success = login_page.login(TestData.TEST_USER["email"], TestData.TEST_USER["password"])
        
        if not login_success:
            # Create account if login failed (likely first run)
            login_page.signup(TestData.TEST_USER["name"], TestData.TEST_USER["email"])
            # Complete registration would be here, but automationexercise.com redirects
            # directly to login after signup, so we'll try login again
            login_page.login(TestData.TEST_USER["email"], TestData.TEST_USER["password"])
        
        # Add product to cart
        home_page.go_to_products()
        product_name = TestData.TEST_PRODUCTS[0]
        products_page.add_to_cart(product_name)
        products_page.go_to_cart()
        
        # Act - proceed to checkout
        cart_page.proceed_to_checkout()
        
        # Assert - verify checkout page loaded
        assert checkout_page.is_loaded(), "Checkout page did not load correctly"
        
        # Get address information for verification
        address = checkout_page.get_delivery_address()
        assert address is not None, "Delivery address not displayed"
        
        # Place order
        checkout_page.place_order()
        
        # Complete payment
        payment_success = checkout_page.complete_payment(TestData.PAYMENT_INFO)
        assert payment_success, "Payment was not successful"
        
        # Verify confirmation message
        confirmation = checkout_page.get_confirmation_message()
        assert "ORDER PLACED" in confirmation, "Order confirmation message not displayed"
        
        # Take screenshot of confirmation
        checkout_page.take_screenshot("order_confirmation")
    
    @pytest.mark.checkout
    @allure.title("Test cart calculation")
    @allure.description("Test that cart total is calculated correctly")
    def test_cart_calculation(self, page):
        # Arrange
        home_page = HomePage(page)
        products_page = ProductsPage(page)
        cart_page = CartPage(page)
        
        # Add multiple products to cart
        home_page.go_to_products()
        
        added_products = []
        expected_total = 0
        
        # Add first two test products and calculate expected total
        for i in range(2):
            product_name = TestData.TEST_PRODUCTS[i]
            products_page.add_to_cart(product_name)
            added_products.append(product_name)
        
        products_page.go_to_cart()
        
        # Calculate expected total from individual product prices
        for product_name in added_products:
            price = cart_page.get_product_price(product_name)
            if price:
                expected_total += price
        
        # Assert - check total matches expected
        actual_total = cart_page.get_total_price()
        assert actual_total == expected_total, f"Cart total {actual_total} doesn't match expected {expected_total}"
        
        # Log price information
        allure.attach(
            f"Products: {', '.join(added_products)}\nExpected total: {expected_total}\nActual total: {actual_total}",
            name="Cart Calculation",
            attachment_type=allure.attachment_type.TEXT
        )
 