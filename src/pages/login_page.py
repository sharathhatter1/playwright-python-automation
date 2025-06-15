import  allure
from src.pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.login_email = "input[data-qa='login-email']"
        self.login_password = "input[data-qa='login-password']"
        self.login_button = "button[data-qa='login-button']"
        self.signup_name = "input[data-qa='signup-name']"
        self.signup_email = "input[data-qa='signup-email']"
        self.signup_button = "button[data-qa='signup-button']"
        self.error_message = ".login-form .alert-danger"
        self.logout_button = "a[href='/logout']"
        self.delete_account_button = "a[href='/delete_account']"
        self.account_created_message = "h2.title"
    
    @allure.step("Check if login page is loaded")
    def is_loaded(self):
        """Check if login page is loaded correctly"""
        self.logger.info("Checking if login page is loaded")
        return (
            self.is_visible(self.login_email) and
            self.is_visible(self.login_password) and
            self.is_visible(self.login_button)
        )
    
    @allure.step("Login with email: {email}")
    def login(self, email, password):
        """Login with email and password"""
        self.logger.info(f"Logging in with email: {email}")
        self.fill(self.login_email, email)
        self.fill(self.login_password, password)
        self.click(self.login_button)
        self.wait_for_page_load()
        # Check if login was successful (logout button is visible)
        return self.is_visible(self.logout_button)
    
    @allure.step("Sign up with name: {name}, email: {email}")
    def signup(self, name, email):
        """Sign up with name and email"""
        self.logger.info(f"Signing up with name: {name}, email: {email}")
        self.fill(self.signup_name, name)
        self.fill(self.signup_email, email)
        self.click(self.signup_button)
        self.wait_for_page_load()
        # Check if signup form is loaded
        return self.is_visible("form[action='/signup']")
    
    @allure.step("Complete registration form")
    def complete_registration(self, user_data):
        """Complete the registration form after signup"""
        self.logger.info("Completing registration form")
        
        # Title selection
        if "gender" in user_data:
            gender = "1" if user_data["gender"].lower() == "male" else "2"
            self.click(f"#id_gender{gender}")
        else:
            self.click("#id_gender1")  # Default to male
        
        # Password
        self.fill("input[data-qa='password']", user_data["password"])
        
        # Date of birth
        self.page.select_option("select[data-qa='days']", user_data["day"])
        self.page.select_option("select[data-qa='months']", user_data["month"])
        self.page.select_option("select[data-qa='years']", user_data["year"])
        
        # Newsletter and offers checkboxes
        self.page.check("#newsletter")
        self.page.check("#optin")
        
        # Address information
        self.fill("input[data-qa='first_name']", user_data["first_name"])
        self.fill("input[data-qa='last_name']", user_data["last_name"])
        self.fill("input[data-qa='company']", user_data["company"])
        self.fill("input[data-qa='address']", user_data["address1"])
        self.fill("input[data-qa='address2']", user_data["address2"])
        self.page.select_option("select[data-qa='country']", user_data["country"])
        self.fill("input[data-qa='state']", user_data["state"])
        self.fill("input[data-qa='city']", user_data["city"])
        self.fill("input[data-qa='zipcode']", user_data["zipcode"])
        self.fill("input[data-qa='mobile_number']", user_data["mobile_number"])
        
        # Submit form
        self.click("button[data-qa='create-account']")
        self.wait_for_page_load()
        
        # Check if account was created successfully
        return "ACCOUNT CREATED!" in self.get_text(self.account_created_message)
    
    @allure.step("Logout")
    def logout(self):
        """Logout from account"""
        self.logger.info("Logging out")
        if self.is_visible(self.logout_button):
            self.click(self.logout_button)
            self.wait_for_page_load()
            return self.is_loaded()
        return False
 