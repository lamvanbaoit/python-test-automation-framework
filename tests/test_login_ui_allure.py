# tests/test_login_ui_allure.py

import pytest
import allure
from pages.login_page import LoginPage
from utils.common_functions import get_random_user
from utils.allure_helpers import AllureReporter

# Test class kiểm thử chức năng đăng nhập với Allure step-by-step reporting
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
        """Test đăng nhập thành công với báo cáo từng bước Allure"""
        
        # Thông tin môi trường
        AllureReporter.environment_step(
            browser=request.config.getoption("--test-browser"),
            base_url="https://www.saucedemo.com/",
            environment="test"
        )
        
        # Bước 1: Điều hướng tới trang login
        AllureReporter.navigate_to("https://www.saucedemo.com/")
        login_page = LoginPage(page)
        login_page.goto()
        
        # Bước 2: Kiểm tra các trường login
        AllureReporter.validate_element_step("Username field", "visible and enabled")
        AllureReporter.validate_element_step("Password field", "visible and enabled")
        AllureReporter.validate_element_step("Login button", "visible and enabled")
        
        login_page.validate_login_fields()
        assert login_page.is_username_enabled()
        assert login_page.is_password_enabled()
        assert login_page.is_login_button_enabled()
        
        # Bước 3: Chuẩn bị dữ liệu test
        user = get_random_user()
        AllureReporter.test_data_step("Login User", user)
        
        # Bước 4: Điền username
        AllureReporter.fill_field_step("Username", user["username"])
        login_page.fill_field(login_page.selectors["username"], user["username"])
        
        # Bước 5: Điền password
        AllureReporter.fill_field_step("Password", "***")
        login_page.fill_field(login_page.selectors["password"], user["password"])
        
        # Bước 6: Chụp màn hình trước khi login
        AllureReporter.take_screenshot_step(page, "Before Login")
        
        # Bước 7: Click login
        AllureReporter.click_element_step("Login Button", login_page.selectors["login_button"])
        login_page.click_button(login_page.selectors["login_button"])
        
        # Bước 8: Đợi trang load
        AllureReporter.wait_for_element_step("Inventory page", 10000)
        page.wait_for_load_state("networkidle", timeout=10000)
        
        # Bước 9: Chụp màn hình sau khi login
        AllureReporter.take_screenshot_step(page, "After Login")
        
        # Bước 10: Kiểm tra đăng nhập thành công
        AllureReporter.assert_step("Login successful", True, login_page.is_logged_in())
        login_page.custom_assert(login_page.is_logged_in(), "Login failed! Check credentials or page state.")

    @allure.testcase("TC002", "Login Failure Test")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_failure_with_steps(self, page):
        """Test đăng nhập thất bại với báo cáo từng bước Allure"""
        
        # Bước 1: Điều hướng tới trang login
        AllureReporter.navigate_to("https://www.saucedemo.com/")
        login_page = LoginPage(page)
        login_page.goto()
        
        # Bước 2: Chuẩn bị dữ liệu test sai
        invalid_user = {
            "username": "invalid_user",
            "password": "invalid_password"
        }
        AllureReporter.test_data_step("Invalid User", invalid_user)
        
        # Bước 3: Điền thông tin sai
        AllureReporter.fill_field_step("Username", invalid_user["username"])
        AllureReporter.fill_field_step("Password", "***")
        
        login_page.fill_field(login_page.selectors["username"], invalid_user["username"])
        login_page.fill_field(login_page.selectors["password"], invalid_user["password"])
        
        # Bước 4: Chụp màn hình trước khi login
        AllureReporter.take_screenshot_step(page, "Before Invalid Login")
        
        # Bước 5: Click login
        AllureReporter.click_element_step("Login Button", login_page.selectors["login_button"])
        login_page.click_button(login_page.selectors["login_button"])
        
        # Bước 6: Đợi thông báo lỗi
        AllureReporter.wait_for_element_step("Error message", 5000)
        page.wait_for_selector(login_page.selectors["error_message"], timeout=5000)
        
        # Bước 7: Chụp màn hình lỗi
        AllureReporter.take_screenshot_step(page, "Login Error")
        
        # Bước 8: Lấy và kiểm tra thông báo lỗi
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
        """Test đăng nhập với locked user"""
        
        # Bước 1: Điều hướng tới trang login
        AllureReporter.navigate_to("https://www.saucedemo.com/")
        login_page = LoginPage(page)
        login_page.goto()
        
        # Bước 2: Chuẩn bị dữ liệu locked user
        locked_user = {
            "username": "locked_out_user",
            "password": "secret_sauce"
        }
        AllureReporter.test_data_step("Locked User", locked_user)
        
        # Bước 3: Điền thông tin locked user
        AllureReporter.fill_field_step("Username", locked_user["username"])
        AllureReporter.fill_field_step("Password", "***")
        
        login_page.fill_field(login_page.selectors["username"], locked_user["username"])
        login_page.fill_field(login_page.selectors["password"], locked_user["password"])
        
        # Bước 4: Chụp màn hình trước khi login
        AllureReporter.take_screenshot_step(page, "Before Locked User Login")
        
        # Bước 5: Click login
        AllureReporter.click_element_step("Login Button", login_page.selectors["login_button"])
        login_page.click_button(login_page.selectors["login_button"])
        
        # Bước 6: Đợi thông báo lỗi
        AllureReporter.wait_for_element_step("Locked user error message", 5000)
        page.wait_for_selector(login_page.selectors["error_message"], timeout=5000)
        
        # Bước 7: Chụp màn hình lỗi locked user
        AllureReporter.take_screenshot_step(page, "Locked User Error")
        
        # Bước 8: Kiểm tra thông báo lỗi locked user
        error_message = login_page.get_error_message()
        AllureReporter.assert_step(
            "Locked user error message",
            "Epic sadface: Sorry, this user has been locked out.",
            error_message
        )
        
        assert "Epic sadface: Sorry, this user has been locked out." in error_message

# Test function kiểm thử đăng nhập với parametrize và Allure
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
    """Test đăng nhập parametrize với Allure reporting"""
    
    # Bước 1: Điều hướng tới trang login
    AllureReporter.navigate_to("https://www.saucedemo.com/")
    login_page = LoginPage(page)
    login_page.goto()
    
    # Bước 2: Chuẩn bị dữ liệu test
    test_data = {
        "username": username,
        "password": password,
        "expected_success": expected_success,
        "expected_error": expected_error
    }
    AllureReporter.test_data_step("Parametrized Test Data", test_data)
    
    # Bước 3: Điền thông tin đăng nhập
    AllureReporter.fill_field_step("Username", username)
    AllureReporter.fill_field_step("Password", "***" if password else "")
    
    login_page.fill_field(login_page.selectors["username"], username)
    login_page.fill_field(login_page.selectors["password"], password)
    
    # Bước 4: Chụp màn hình trước khi login
    AllureReporter.take_screenshot_step(page, f"Before Login - {username}")
    
    # Bước 5: Click login
    AllureReporter.click_element_step("Login Button", login_page.selectors["login_button"])
    login_page.click_button(login_page.selectors["login_button"])
    
    # Bước 6: Xử lý kết quả
    if expected_success:
        # Bước 6a: Đợi thành công
        AllureReporter.wait_for_element_step("Inventory page", 10000)
        page.wait_for_load_state("networkidle", timeout=10000)
        
        # Bước 6b: Chụp màn hình thành công
        AllureReporter.take_screenshot_step(page, f"Login Success - {username}")
        
        # Bước 6c: Kiểm tra thành công
        AllureReporter.assert_step("Login successful", True, login_page.is_logged_in())
        assert login_page.is_logged_in()
    else:
        # Bước 6a: Đợi thông báo lỗi
        AllureReporter.wait_for_element_step("Error message", 5000)
        page.wait_for_selector(login_page.selectors["error_message"], timeout=5000)
        
        # Bước 6b: Chụp màn hình lỗi
        AllureReporter.take_screenshot_step(page, f"Login Error - {username}")
        
        # Bước 6c: Kiểm tra thông báo lỗi
        error_message = login_page.get_error_message()
        AllureReporter.assert_step(
            "Error message validation",
            expected_error,
            error_message
        )
        assert expected_error in error_message 