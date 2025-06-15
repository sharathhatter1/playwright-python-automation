import  allure
from src.pages.base_page import BasePage

class ProductsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.products_title = ".title"
        self.product_list = ".features_items"
        self.add_to_cart_buttons = ".add-to-cart"
        self.view_product_buttons = ".choose a"
        self.product_info = ".productinfo"
        self.search_result = ".features_items .product-image-wrapper"
        self.continue_shopping_button = ".btn-success"
        self.view_cart_button = "p a[href='/view_cart']"
        self.category_list = ".category-products"
        self.brands_list = ".brands-name"
        self.product_details_link = "a[href='/product_details/']"
        self.search_box = "#search_product"
        self.search_button = "#submit_search"
    
    @allure.step("Check if products page is loaded")
    def is_loaded(self):
        """Check if products page is loaded correctly"""
        self.logger.info("Checking if products page is loaded")
        return (
            self.is_visible(self.products_title) and
            self.is_visible(self.product_list)
        )
    
    @allure.step("Get all product names")
    def get_product_names(self):
        """Get all product names on the page"""
        self.logger.info("Getting all product names")
        products = self.page.locator(f"{self.product_info} p")
        return [products.nth(i).text_content() for i in range(products.count())]
    
    @allure.step("Add product to cart: {product_name}")
    def add_to_cart(self, product_name):
        """Add a product to cart by name"""
        self.logger.info(f"Adding product to cart: {product_name}")
        # Find product by name and get its index
        product_names = self.get_product_names()
        if product_name in product_names:
            index = product_names.index(product_name)
            # Click on add to cart button for this product
            self.page.locator(self.add_to_cart_buttons).nth(index).click()
            # Wait for modal to appear
            self.wait_for_selector("#cartModal", state="visible")
            # Click continue shopping
            self.click(self.continue_shopping_button)
            return True
        else:
            self.logger.error(f"Product not found: {product_name}")
            return False
    
    @allure.step("View product details: {product_name}")
    def view_product_details(self, product_name):
        """View details of a product by name"""
        self.logger.info(f"Viewing product details: {product_name}")
        # Find product by name and get its index
        product_names = self.get_product_names()
        if product_name in product_names:
            index = product_names.index(product_name)
            # Click on view product button for this product
            self.page.locator(self.view_product_buttons).nth(index).click()
            self.wait_for_page_load()
            return True
        else:
            self.logger.error(f"Product not found: {product_name}")
            return False
    
    @allure.step("Get search results count")
    def get_search_results_count(self):
        """Get count of search results"""
        self.logger.info("Getting search results count")
        return self.get_count(self.search_result)
    
    @allure.step("Go to cart after adding product")
    def go_to_cart(self):
        """Go to cart page after adding product"""
        self.logger.info("Going to cart after adding product")
        self.click(self.view_cart_button)
        self.wait_for_page_load()
        
    @allure.step("Search for product: {search_term}")
    def search_product(self, search_term):
        """Search for a product using the search box"""
        self.logger.info(f"Searching for product: {search_term}")
        self.fill(self.search_box, search_term)
        self.click(self.search_button)
        self.wait_for_page_load()
        
    @allure.step("Add first product to cart")
    def add_first_product_to_cart(self):
        """Add the first product on the page to cart"""
        self.logger.info("Adding first product to cart")
        # Hover over the first product to make the add to cart button visible
        self.page.locator(self.product_info).first.hover()
        # Click the first add to cart button
        self.page.locator(self.add_to_cart_buttons).first.click()
        # Wait for modal to appear
        self.wait_for_selector("#cartModal", state="visible")
        # Click continue shopping
        self.click(self.continue_shopping_button)
 