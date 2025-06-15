import  allure
import re
from src.pages.base_page import BasePage

class CheckoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.address_details = "#address_delivery"
        self.order_info = "#cart_info"
        self.place_order_button = "a.check_out"
        self.payment_name = "input[name='name_on_card']"
        self.payment_card_number = "input[name='card_number']"
        self.payment_cvc = "input[name='cvc']"
        self.payment_expiry_month = "input[name='expiry_month']"
        self.payment_expiry_year = "input[name='expiry_year']"
        self.payment_submit_button = "#submit"
        self.order_placed_message = ".title"
        self.download_invoice_button = ".check_out"
        self.continue_button = "a[data-qa='continue-button']"
    
    @allure.step("Check if checkout page is loaded")
    def is_loaded(self):
        """Check if checkout page is loaded correctly"""
        self.logger.info("Checking if checkout page is loaded")
        return (
            self.is_visible(self.address_details) and
            self.is_visible(self.order_info) and
            self.is_visible(self.place_order_button)
        )
    
    @allure.step("Get delivery address")
    def get_delivery_address(self):
        """Get delivery address information"""
        self.logger.info("Getting delivery address")
        if not self.is_visible(self.address_details):
            return None
        return self.get_text(self.address_details)
    
    @allure.step("Place order")
    def place_order(self):
        """Place order and proceed to payment"""
        self.logger.info("Placing order")
        if self.is_visible(self.place_order_button):
            self.click(self.place_order_button)
            self.wait_for_page_load()
            return self.is_visible(self.payment_name)
        return False
    
    @allure.step("Complete payment")
    def complete_payment(self, payment_info):
        """Complete payment with card details"""
        self.logger.info("Completing payment")
        if not self.is_visible(self.payment_name):
            return False
        
        # Fill payment information
        self.fill(self.payment_name, payment_info["name_on_card"])
        self.fill(self.payment_card_number, payment_info["card_number"])
        self.fill(self.payment_cvc, payment_info["cvc"])
        self.fill(self.payment_expiry_month, payment_info["expiry_month"])
        self.fill(self.payment_expiry_year, payment_info["expiry_year"])
        
        # Submit payment
        self.click(self.payment_submit_button)
        self.wait_for_page_load()
        
        # Check if order was placed successfully
        return self.is_visible(self.order_placed_message) and "ORDER PLACED!" in self.get_text(self.order_placed_message)
    
    @allure.step("Download invoice")
    def download_invoice(self):
        """Download invoice for the order"""
        self.logger.info("Downloading invoice")
        if self.is_visible(self.download_invoice_button):
            with self.page.expect_download() as download_info:
                self.click(self.download_invoice_button)
            download = download_info.value
            return download.path()
        return None
    
    @allure.step("Continue after order")
    def continue_after_order(self):
        """Continue after placing order"""
        self.logger.info("Continuing after order")
        if self.is_visible(self.continue_button):
            self.click(self.continue_button)
            self.wait_for_page_load()
            return True
        return False
    
    @allure.step("Get order confirmation message")
    def get_confirmation_message(self):
        """Get order confirmation message"""
        self.logger.info("Getting order confirmation message")
        if self.is_visible(self.order_placed_message):
            return self.get_text(self.order_placed_message)
        return None
 