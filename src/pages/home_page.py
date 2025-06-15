import  allure
from src.pages.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.products_button = "a[href='/products']"
        self.login_button = "a[href='/login']"
        self.cart_button = "a[href='/view_cart']"
        self.search_box = "#search_product"
        self.search_button = "#submit_search"
        self.slider = "#slider-carousel"
        self.logo = ".logo"
        self.recommended_items = "#recommended-item-carousel"
        self.subscription_email = "#susbscribe_email"
        self.subscription_button = "#subscribe"
        self.features_items = ".features_items"
    
    @allure.step("Check if homepage is loaded")
    def is_loaded(self):
        """Check if homepage is loaded correctly"""
        self.logger.info("Checking if homepage is loaded")
        return (
            self.is_visible(self.logo) and
            self.is_visible(self.slider) and
            self.is_visible(self.features_items)
        )
    
    @allure.step("Navigate to products page")
    def go_to_products(self):
        """Navigate to products page"""
        self.logger.info("Navigating to products page")
        self.click(self.products_button)
        self.wait_for_page_load()
    
    @allure.step("Navigate to login page")
    def go_to_login(self):
        """Navigate to login page"""
        self.logger.info("Navigating to login page")
        self.click(self.login_button)
        self.wait_for_page_load()
    
    @allure.step("Navigate to cart page")
    def go_to_cart(self):
        """Navigate to cart page"""
        self.logger.info("Navigating to cart page")
        self.click(self.cart_button)
        self.wait_for_page_load()
    
    @allure.step("Search for product: {product_name}")
    def search_product(self, product_name):
        """Search for a product"""
        self.logger.info(f"Searching for product: {product_name}")
        self.fill(self.search_box, product_name)
        self.click(self.search_button)
        self.wait_for_page_load()
    
    @allure.step("Subscribe with email: {email}")
    def subscribe(self, email):
        """Subscribe to newsletter"""
        self.logger.info(f"Subscribing with email: {email}")
        # Scroll to subscription area
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.fill(self.subscription_email, email)
        self.click(self.subscription_button)
        # Wait for success message
        return self.is_visible(".alert-success", 5000)
 