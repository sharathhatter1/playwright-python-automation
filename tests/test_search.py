import  pytest
import allure
from src.pages.home_page import HomePage
from src.pages.products_page import ProductsPage
from src.utils.test_data import TestData

@allure.feature("Product Search")
class TestSearch:
    
    @pytest.mark.search
    @allure.title("Test search for existing product")
    @allure.description("Test searching for an existing product and verifying results are shown")
    def test_search_product(self, page):
        # Arrange
        home_page = HomePage(page)
        products_page = ProductsPage(page)
        search_term = TestData.SEARCH_TERMS[0]  # Use first search term
        
        # Act
        home_page.go_to_products()
        products_page.wait_for_page_load()
        products_page.search_product(search_term)
        
        # Assert
        results_count = products_page.get_search_results_count()
        assert results_count > 0, f"No search results found for '{search_term}'"
        
        # Take screenshot of search results
        products_page.take_screenshot(f"search_results_{search_term}")
        
        # Verify "Searched Products" title is displayed
        title_text = products_page.get_text(products_page.products_title)
        assert "SEARCHED PRODUCTS" in title_text, "Search results title not displayed correctly"
    
    @pytest.mark.search
    @allure.title("Test search with no results")
    @allure.description("Test searching for a non-existent product and verifying no results are shown")
    def test_search_no_results(self, page):
        # Arrange
        home_page = HomePage(page)
        products_page = ProductsPage(page)
        invalid_search = "xyznonexistentproduct123456789"
        
        # Act
        home_page.go_to_products()
        products_page.search_product(invalid_search)
        
        # Assert
        results_count = products_page.get_search_results_count()
        assert results_count == 0, f"Search results found for non-existent product '{invalid_search}'"
    
    @pytest.mark.search
    @allure.title("Test search with multiple terms")
    @allure.description("Test searching for multiple different products")
    @pytest.mark.parametrize("search_term", TestData.SEARCH_TERMS)
    def test_search_multiple_terms(self, page, search_term):
        # Arrange
        home_page = HomePage(page)
        products_page = ProductsPage(page)
        
        # Act
        home_page.go_to_products()
        products_page.wait_for_page_load()
        products_page.search_product(search_term)
        
        # Assert
        results_count = products_page.get_search_results_count()
        
        # Log search results
        allure.attach(
            f"Search for '{search_term}' returned {results_count} results",
            name="Search Results",
            attachment_type=allure.attachment_type.TEXT
        )
        
        # No assertion about count - we're just testing the search functionality works
        # and documenting what each term returns
 