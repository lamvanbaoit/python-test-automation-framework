# tests/test_login_ui.py

import pytest
from playwright.sync_api import Page
from pages.auth.login_page import LoginPage
from utils.helpers import get_test_user

def test_login_success(page: Page):
    """Test login thành công"""
    login_page = LoginPage(page)
    login_page.goto()
    login_page.logger.info("Validating login fields visibility and enabled state...")
    login_page.validate_login_fields()
    assert login_page.is_username_enabled()
    assert login_page.is_password_enabled()
    assert login_page.is_login_button_enabled()
    user = get_test_user()
    login_page.login(user["username"], user["password"])
    login_page.custom_assert(login_page.is_logged_in(), "Login failed! Check credentials or page state.")

@pytest.mark.parametrize("username,password,expected_success,expected_error", [
    ("standard_user", "secret_sauce", True, ""),
    ("invalid_user", "invalid_pass", False, "Epic sadface: Username and password do not match any user in this service"),
    ("", "", False, "Epic sadface: Username is required"),
    ("standard_user", "", False, "Epic sadface: Password is required"),
])
def test_login_parametrized(page: Page, username, password, expected_success, expected_error):
    """Test login với nhiều trường hợp khác nhau"""
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(username, password)
    
    if expected_success:
        page.wait_for_timeout(2000)
        assert login_page.is_logged_in()
    else:
        error_message = login_page.get_error_message()
        if expected_error:
            assert expected_error in error_message or error_message != "" 