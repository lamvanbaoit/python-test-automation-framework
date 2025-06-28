from .base_page import BasePage
from playwright.sync_api import Page
from typing import Dict, Optional
from .login_locators import LOGIN_PAGE_SELECTORS

class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page, selectors: Optional[Dict[str, str]] = None):
        super().__init__(page)
        self.selectors = selectors if selectors is not None else LOGIN_PAGE_SELECTORS

    def goto(self):
        super().goto(self.URL)

    def login(self, username: str, password: str):
        self.fill_field(self.selectors["username"], username)
        self.fill_field(self.selectors["password"], password)
        self.click_button(self.selectors["login_button"])

    def get_error_message(self) -> str:
        if self.is_element_visible(self.selectors["error_message"]):
            return self.get_text(self.selectors["error_message"])
        return ""

    def is_logged_in(self) -> bool:
        return self.page.url.endswith("/inventory.html")

    def validate_login_fields(self):
        self.custom_assert(self.is_element_visible(self.selectors["username"]), "Username field not visible")
        self.custom_assert(self.is_element_visible(self.selectors["password"]), "Password field not visible")
        self.custom_assert(self.is_element_visible(self.selectors["login_button"]), "Login button not visible")

    def is_username_enabled(self):
        return self.is_element_enabled(self.selectors["username"])

    def is_password_enabled(self):
        return self.is_element_enabled(self.selectors["password"])

    def is_login_button_enabled(self):
        return self.is_element_enabled(self.selectors["login_button"]) 