from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
import logging
import os
from datetime import datetime
import time

# Lớp cơ sở cho tất cả các Page Object, cung cấp các hàm thao tác chung với trang web
class BasePage:
    def __init__(self, page: Page):
        # Đối tượng page của Playwright để thao tác với browser
        self.page = page
        # Logger để ghi log cho từng class kế thừa
        self.logger = logging.getLogger(self.__class__.__name__)

    def goto(self, url: str):
        # Hàm điều hướng tới một URL cụ thể
        self.logger.info(f"Navigating to {url}")
        self.page.goto(url)

    def wait_for_selector(self, selector: str, timeout: int = 5000):
        # Chờ cho đến khi selector xuất hiện trên trang (timeout mặc định 5s)
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            self.logger.error(f"Timeout waiting for selector: {selector}")
            return False

    def take_screenshot(self, name: str = ""):
        # Chụp màn hình toàn trang, lưu vào thư mục screenshots
        if not name:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join("screenshots", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.page.screenshot(path=path, full_page=True)
        self.logger.info(f"Screenshot saved to {path}")
        return path

    def custom_assert(self, condition, message):
        # Hàm assert tuỳ chỉnh: nếu sai sẽ chụp màn hình và ghi log lỗi
        if not condition:
            self.logger.error(f"Assertion failed: {message}")
            self.take_screenshot()
            assert condition, message

    def is_element_visible(self, selector: str):
        # Kiểm tra một phần tử có hiển thị trên trang không
        return self.page.is_visible(selector)

    def is_element_enabled(self, selector: str):
        # Kiểm tra một phần tử có enable không
        return self.page.is_enabled(selector)

    def is_element_disabled(self, selector: str):
        # Kiểm tra một phần tử có disable không
        return self.page.is_disabled(selector)

    def fill_field(self, selector: str, value: str, timeout: int = 5000, retry: int = 2):
        # Điền giá trị vào ô input, có retry nếu gặp lỗi
        for attempt in range(retry):
            try:
                self.logger.info(f"Filling field {selector} with value '{value}' (attempt {attempt+1})")
                self.page.fill(selector, value, timeout=timeout)
                return
            except Exception as e:
                self.logger.warning(f"Fill failed: {e}")
                time.sleep(0.5)
        self.custom_assert(False, f"Failed to fill field {selector}")

    def click_button(self, selector: str, timeout: int = 5000, retry: int = 2):
        # Click vào button, có retry nếu gặp lỗi
        for attempt in range(retry):
            try:
                self.logger.info(f"Clicking button {selector} (attempt {attempt+1})")
                self.page.click(selector, timeout=timeout)
                return
            except Exception as e:
                self.logger.warning(f"Click failed: {e}")
                time.sleep(0.5)
        self.custom_assert(False, f"Failed to click button {selector}")

    def get_text(self, selector: str, timeout: int = 5000) -> str:
        # Lấy text của một phần tử trên trang
        self.logger.info(f"Getting text from {selector}")
        self.wait_for_selector(selector, timeout)
        msg = self.page.text_content(selector)
        return msg if msg is not None else "" 