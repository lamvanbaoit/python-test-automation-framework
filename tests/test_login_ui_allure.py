# tests/test_login_ui_allure.py

import pytest
import allure
from pages.login_page import LoginPage
from utils.common_functions import get_random_user
from utils.allure_helpers import AllureReporter

@allure.feature("Authentication")
@allure.story("User Login")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Test login functionality with step-by-step reporting.
This test demonstrates Allure Framework integration with detailed steps.
""")
class TestLoginWithAllure:
    
    @allure.testcase("TC001", "Login Success Test")
    @allure.issue("BUG-001", "https://jira.example.com/browse/BUG-001")
    def test_login_success_with_steps(self, page, request):
        """Test login success với step-by-step reporting"""
        
        # Environment info
        AllureReporter.environment_step(
            browser=request.config.getoption("--test-browser"),
            base_url="https://www.saucedemo.com/",
            environment="test"
        )
        
        # Step 1: Navigate to login page
        AllureReporter.navigate_to("https://www.saucedemo.com/")
        login_page = LoginPage(page)
        login_page.goto()
        
        # Step 2: Validate login fields
        AllureReporter.validate_element_step("Username field", "visible and enabled")
        AllureReporter.validate_element_step("Password field", "visible and enabled")
        AllureReporter.validate_element_step("Login button", "visible and enabled")
        
        login_page.validate_login_fields()
        assert login_page.is_username_enabled()
        assert login_page.is_password_enabled()
        assert login_page.is_login_button_enabled()
        
        # Step 3: Prepare test data
        user = get_random_user()
        AllureReporter.test_data_step("Login User", user)
        
        # Step 4: Fill username
        AllureReporter.fill_field_step("Username", user["username"])
        login_page.fill_field(login_page.selectors["username"], user["username"])
        
        # Step 5: Fill password
        AllureReporter.fill_field_step("Password", "***")
        login_page.fill_field(login_page.selectors["password"], user["password"])
        
        # Step 6: Take screenshot before login
        AllureReporter.take_screenshot_step(page, "Before Login")
        
        # Step 7: Click login button
        AllureReporter.click_element_step("Login Button", login_page.selectors["login_button"])
        login_page.click_button(login_page.selectors["login_button"])
        
        # Step 8: Wait for page load
        AllureReporter.wait_for_element_step("Inventory page", 10000)
        page.wait_for_load_state("networkidle", timeout=10000)
        
        # Step 9: Take screenshot after login
        AllureReporter.take_screenshot_step(page, "After Login")
        
        # Step 10: Assert login success
        AllureReporter.assert_step("Login successful", True, login_page.is_logged_in())
        login_page.custom_assert(login_page.is_logged_in(), "Login failed! Check credentials or page state.")

    @allure.testcase("TC002", "Login Failure Test")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_failure_with_steps(self, page):
        """Test login failure với step-by-step reporting"""
        
        # Step 1: Navigate to login page
        AllureReporter.navigate_to("https://www.saucedemo.com/")
        login_page = LoginPage(page)
        login_page.goto()
        
        # Step 2: Prepare invalid test data
        invalid_user = {
            "username": "invalid_user",
            "password": "invalid_password"
        }
        AllureReporter.test_data_step("Invalid User", invalid_user)
        
        # Step 3: Fill invalid credentials
        AllureReporter.fill_field_step("Username", invalid_user["username"])
        AllureReporter.fill_field_step("Password", "***")
        
        login_page.fill_field(login_page.selectors["username"], invalid_user["username"])
        login_page.fill_field(login_page.selectors["password"], invalid_user["password"])
        
        # Step 4: Take screenshot before login attempt
        AllureReporter.take_screenshot_step(page, "Before Invalid Login")
        
        # Step 5: Click login button
        AllureReporter.click_element_step("Login Button", login_page.selectors["login_button"])
        login_page.click_button(login_page.selectors["login_button"])
        
        # Step 6: Wait for error message
        AllureReporter.wait_for_element_step("Error message", 5000)
        page.wait_for_selector(login_page.selectors["error_message"], timeout=5000)
        
        # Step 7: Take screenshot with error
        AllureReporter.take_screenshot_step(page, "Login Error")
        
        # Step 8: Get and validate error message
        error_message = login_page.get_error_message()
        AllureReporter.assert_step(
            "Error message contains expected text",
            "Epic sadface: Username and password do not match any user in this service",
            error_message
        )
        
        assert "Epic sadface: Username and password do not match any user in this service" in error_message

    @allure.testcase("TC003", "Login with Locked User")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_locked_user_with_steps(self, page):
        """Test login với locked user"""
        
        # Step 1: Navigate to login page
        AllureReporter.navigate_to("https://www.saucedemo.com/")
        login_page = LoginPage(page)
        login_page.goto()
        
        # Step 2: Prepare locked user data
        locked_user = {
            "username": "locked_out_user",
            "password": "secret_sauce"
        }
        AllureReporter.test_data_step("Locked User", locked_user)
        
        # Step 3: Fill locked user credentials
        AllureReporter.fill_field_step("Username", locked_user["username"])
        AllureReporter.fill_field_step("Password", "***")
        
        login_page.fill_field(login_page.selectors["username"], locked_user["username"])
        login_page.fill_field(login_page.selectors["password"], locked_user["password"])
        
        # Step 4: Take screenshot before login
        AllureReporter.take_screenshot_step(page, "Before Locked User Login")
        
        # Step 5: Click login button
        AllureReporter.click_element_step("Login Button", login_page.selectors["login_button"])
        login_page.click_button(login_page.selectors["login_button"])
        
        # Step 6: Wait for error message
        AllureReporter.wait_for_element_step("Locked user error message", 5000)
        page.wait_for_selector(login_page.selectors["error_message"], timeout=5000)
        
        # Step 7: Take screenshot with locked user error
        AllureReporter.take_screenshot_step(page, "Locked User Error")
        
        # Step 8: Validate locked user error message
        error_message = login_page.get_error_message()
        AllureReporter.assert_step(
            "Locked user error message",
            "Epic sadface: Sorry, this user has been locked out.",
            error_message
        )
        
        assert "Epic sadface: Sorry, this user has been locked out." in error_message

# Test function với parametrize và Allure
@allure.feature("Authentication")
@allure.story("Login Parametrized")
@pytest.mark.parametrize(
    "username,password,expected_success,expected_error",
    [
        ("standard_user", "secret_sauce", True, ""),
        ("locked_out_user", "secret_sauce", False, "Epic sadface: Sorry, this user has been locked out."),
        ("", "", False, "Epic sadface: Username is required"),
        ("standard_user", "", False, "Epic sadface: Password is required"),
    ]
)
def test_login_parametrized_with_allure(page, username, password, expected_success, expected_error):
    """Test login parametrized với Allure reporting"""
    
    # Step 1: Navigate to login page
    AllureReporter.navigate_to("https://www.saucedemo.com/")
    login_page = LoginPage(page)
    login_page.goto()
    
    # Step 2: Prepare test data
    test_data = {
        "username": username,
        "password": password,
        "expected_success": expected_success,
        "expected_error": expected_error
    }
    AllureReporter.test_data_step("Parametrized Test Data", test_data)
    
    # Step 3: Fill credentials
    AllureReporter.fill_field_step("Username", username)
    AllureReporter.fill_field_step("Password", "***" if password else "")
    
    login_page.fill_field(login_page.selectors["username"], username)
    login_page.fill_field(login_page.selectors["password"], password)
    
    # Step 4: Take screenshot before login
    AllureReporter.take_screenshot_step(page, f"Before Login - {username}")
    
    # Step 5: Click login button
    AllureReporter.click_element_step("Login Button", login_page.selectors["login_button"])
    login_page.click_button(login_page.selectors["login_button"])
    
    # Step 6: Handle result
    if expected_success:
        # Step 6a: Wait for success
        AllureReporter.wait_for_element_step("Inventory page", 10000)
        page.wait_for_load_state("networkidle", timeout=10000)
        
        # Step 6b: Take success screenshot
        AllureReporter.take_screenshot_step(page, f"Login Success - {username}")
        
        # Step 6c: Assert success
        AllureReporter.assert_step("Login successful", True, login_page.is_logged_in())
        assert login_page.is_logged_in()
    else:
        # Step 6a: Wait for error message
        AllureReporter.wait_for_element_step("Error message", 5000)
        page.wait_for_selector(login_page.selectors["error_message"], timeout=5000)
        
        # Step 6b: Take error screenshot
        AllureReporter.take_screenshot_step(page, f"Login Error - {username}")
        
        # Step 6c: Validate error message
        error_message = login_page.get_error_message()
        AllureReporter.assert_step(
            "Error message validation",
            expected_error,
            error_message
        )
        assert expected_error in error_message 