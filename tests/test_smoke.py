import  pytest
import allure
from src.pages.home_page import HomePage
from src.pages.products_page import ProductsPage
from src.pages.login_page import LoginPage
from src.pages.cart_page import CartPage

@allure.feature("Smoke Tests")
class TestSmoke:
    
    @pytest.mark.smoke
    @allure.title("Test homepage loads")
    @allure.description("Verify that the homepage loads correctly")
    def test_homepage_load(self, page):
        home_page = HomePage(page)
        assert home_page.is_loaded(), "Homepage did not load correctly"
        
        # Take screenshot of homepage
        home_page.take_screenshot("homepage")
    
    @pytest.mark.smoke
    @allure.title("Test products page loads")
    @allure.description("Verify that the products page loads correctly")
    def test_products_page_load(self, page):
        home_page = HomePage(page)
        home_page.go_to_products()
        
        products_page = ProductsPage(page)
        assert products_page.is_loaded(), "Products page did not load correctly"
        
        # Check for products displayed
        product_count = products_page.get_count(products_page.product_list + " .product-image-wrapper")
        assert product_count > 0, "No products displayed on products page"
    
    @pytest.mark.smoke
    @allure.title("Test login page loads")
    @allure.description("Verify that the login page loads correctly")
    def test_login_page_load(self, page):
        home_page = HomePage(page)
        home_page.go_to_login()
        
        login_page = LoginPage(page)
        assert login_page.is_loaded(), "Login page did not load correctly"
        
        # Verify login form elements
        assert login_page.is_visible(login_page.login_email), "Login email field not visible"
        assert login_page.is_visible(login_page.login_password), "Login password field not visible"
        assert login_page.is_visible(login_page.login_button), "Login button not visible"
    
    @pytest.mark.smoke
    @allure.title("Test cart page loads")
    @allure.description("Verify that the cart page loads correctly")
    def test_cart_page_load(self, page):
        home_page = HomePage(page)
        home_page.go_to_cart()
        
        cart_page = CartPage(page)
        assert cart_page.is_loaded(), "Cart page did not load correctly"
 