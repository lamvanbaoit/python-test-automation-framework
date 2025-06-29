# tests/test_login_ui.py

import pytest
from pages.login_page import LoginPage
from utils.helpers import get_test_user

# Test kiểm thử đăng nhập với nhiều bộ dữ liệu khác nhau (parametrize)
@pytest.mark.parametrize(
    "username,password,expected_success,expected_error",
    [
        ("standard_user", "secret_sauce", True, ""),  # Đăng nhập thành công
        ("locked_out_user", "secret_sauce", False, "Epic sadface: Sorry, this user has been locked out."),
        ("", "", False, "Epic sadface: Username is required"),
        ("standard_user", "", False, "Epic sadface: Password is required"),
        ("invalid_user", "invalid_pass", False, "Epic sadface: Username and password do not match any user in this service"),
    ]
)
def test_login_parametrized(page, username, password, expected_success, expected_error):
    # Khởi tạo trang login
    login_page = LoginPage(page)
    login_page.goto()
    # Thực hiện đăng nhập
    login_page.login(username, password)
    if expected_success:
        # Nếu mong đợi thành công, kiểm tra đã login thành công
        assert login_page.is_logged_in()
    else:
        # Nếu mong đợi thất bại, kiểm tra thông báo lỗi
        assert expected_error in login_page.get_error_message()

# Test kiểm thử đăng nhập thành công và kiểm tra các trường trên form

def test_login_success(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.logger.info("Validating login fields visibility and enabled state...")
    # Kiểm tra các trường trên form login có hiển thị và enable không
    login_page.validate_login_fields()
    assert login_page.is_username_enabled()
    assert login_page.is_password_enabled()
    assert login_page.is_login_button_enabled()
    # Lấy user test và đăng nhập
    user = get_test_user()
    login_page.login(user["username"], user["password"])
    login_page.custom_assert(login_page.is_logged_in(), "Login failed! Check credentials or page state.") 