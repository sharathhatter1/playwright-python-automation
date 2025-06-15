import  allure
import re
from src.pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.cart_table = "#cart_info"
        self.checkout_button = ".check_out"
        self.delete_buttons = ".cart_quantity_delete"
        self.cart_items = ".cart_info tbody tr"
        self.empty_cart_message = "#empty_cart"
        self.product_price = ".cart_price p"
        self.product_quantity = ".cart_quantity button"
        self.product_total = ".cart_total_price"
        self.product_name = ".cart_description h4 a"
        self.continue_shopping_button = ".btn-success"
    
    @allure.step("Check if cart page is loaded")
    def is_loaded(self):
        """Check if cart page is loaded correctly"""
        self.logger.info("Checking if cart page is loaded")
        return self.is_visible(self.cart_table) or self.is_visible(self.empty_cart_message)
    
    @allure.step("Get cart items count")
    def get_cart_items_count(self):
        """Get number of items in cart"""
        self.logger.info("Getting cart items count")
        if self.is_visible(self.empty_cart_message):
            return 0
        return self.get_count(self.cart_items)
    
    @allure.step("Check if product is in cart: {product_name}")
    def is_product_in_cart(self, product_name):
        """Check if a product is in the cart"""
        self.logger.info(f"Checking if product is in cart: {product_name}")
        if self.is_visible(self.empty_cart_message):
            return False
        
        product_names = self.page.locator(self.product_name)
        for i in range(product_names.count()):
            if product_names.nth(i).text_content().strip() == product_name:
                return True
        return False
    
    @allure.step("Get product price: {product_name}")
    def get_product_price(self, product_name):
        """Get price of a product in cart"""
        self.logger.info(f"Getting price for product: {product_name}")
        if not self.is_product_in_cart(product_name):
            return None
        
        # Find product index
        product_names = self.page.locator(self.product_name)
        for i in range(product_names.count()):
            if product_names.nth(i).text_content().strip() == product_name:
                price_text = self.page.locator(self.product_price).nth(i).text_content().strip()
                # Extract number from price text (e.g., "Rs. 500" -> 500)
                match = re.search(r'\d+', price_text)
                if match:
                    return int(match.group())
        return None
    
    @allure.step("Get total price")
    def get_total_price(self):
        """Get total price of all items in cart"""
        self.logger.info("Getting total price of cart")
        if self.is_visible(self.empty_cart_message):
            return 0
        
        total = 0
        prices = self.page.locator(self.product_total)
        for i in range(prices.count()):
            price_text = prices.nth(i).text_content().strip()
            match = re.search(r'\d+', price_text)
            if match:
                total += int(match.group())
        return total
    
    @allure.step("Remove product from cart: {product_name}")
    def remove_product(self, product_name):
        """Remove a product from cart"""
        self.logger.info(f"Removing product from cart: {product_name}")
        if not self.is_product_in_cart(product_name):
            return False
        
        # Find product index
        product_names = self.page.locator(self.product_name)
        for i in range(product_names.count()):
            if product_names.nth(i).text_content().strip() == product_name:
                self.page.locator(self.delete_buttons).nth(i).click()
                self.wait_for_page_load()
                return True
        return False
    
    @allure.step("Proceed to checkout")
    def proceed_to_checkout(self):
        """Click on checkout button"""
        self.logger.info("Proceeding to checkout")
        if self.is_visible(self.checkout_button):
            self.click(self.checkout_button)
            self.wait_for_page_load()
            return True
        return False
 