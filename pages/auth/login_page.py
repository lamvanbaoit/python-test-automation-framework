from ..base.base_page import BasePage
from playwright.sync_api import Page
from typing import Dict, Optional
from ..locators.login_locators import LOGIN_PAGE_SELECTORS

# Page Object cho trang đăng nhập (Login Page) của ứng dụng
class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page, selectors: Optional[Dict[str, str]] = None):
        # Khởi tạo LoginPage với page của Playwright và bộ selector (mặc định dùng LOGIN_PAGE_SELECTORS)
        super().__init__(page)
        self.selectors = selectors if selectors is not None else LOGIN_PAGE_SELECTORS

    def goto(self):
        # Điều hướng tới trang login
        super().goto(self.URL)
        # Đợi trang load hoàn toàn
        self.page.wait_for_load_state("networkidle", timeout=10000)

    def login(self, username: str, password: str):
        # Thực hiện thao tác đăng nhập với username và password truyền vào
        self.fill_field(self.selectors["username"], username)
        self.fill_field(self.selectors["password"], password)
        self.click_button(self.selectors["login_button"])

    def get_error_message(self) -> str:
        # Lấy thông báo lỗi hiển thị trên trang (nếu có)
        try:
            # Đợi error message xuất hiện
            self.page.wait_for_selector(self.selectors["error_message"], timeout=5000)
            if self.is_element_visible(self.selectors["error_message"]):
                return self.get_text(self.selectors["error_message"])
        except Exception as e:
            self.logger.warning(f"Error getting error message: {e}")
        return ""

    def is_logged_in(self) -> bool:
        # Kiểm tra đã login thành công chưa (dựa vào url hoặc element)
        try:
            # Kiểm tra URL hoặc element chỉ định đã login
            return "inventory" in self.page.url or self.is_element_visible(".inventory_list")
        except:
            return False

    def validate_login_fields(self):
        # Kiểm tra các trường trên form login có hiển thị không
        # Đợi trang load và elements xuất hiện
        self.page.wait_for_load_state("domcontentloaded", timeout=10000)
        
        # Đợi từng element với timeout dài hơn
        self.page.wait_for_selector(self.selectors["username"], timeout=10000)
        self.page.wait_for_selector(self.selectors["password"], timeout=10000)
        self.page.wait_for_selector(self.selectors["login_button"], timeout=10000)
        
        self.custom_assert(self.is_element_visible(self.selectors["username"]), "Username field not visible")
        self.custom_assert(self.is_element_visible(self.selectors["password"]), "Password field not visible")
        self.custom_assert(self.is_element_visible(self.selectors["login_button"]), "Login button not visible")

    def is_username_enabled(self):
        # Kiểm tra ô username có enable không
        return self.is_element_enabled(self.selectors["username"])

    def is_password_enabled(self):
        # Kiểm tra ô password có enable không
        return self.is_element_enabled(self.selectors["password"])

    def is_login_button_enabled(self):
        # Kiểm tra nút login có enable không
        return self.is_element_enabled(self.selectors["login_button"]) 