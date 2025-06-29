from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
import logging
import os
from datetime import datetime
import time
import allure
from typing import Optional, Dict, Any, List, Literal, Callable
from functools import wraps

# Lớp cơ sở cho tất cả các Page Object, cung cấp các hàm thao tác chung với trang web
class BasePage:
    def __init__(self, page: Page, mass_test_mode: bool = False):
        # Đối tượng page của Playwright để thao tác với browser
        self.page = page
        # Logger để ghi log cho từng class kế thừa
        self.logger = logging.getLogger(self.__class__.__name__)
        # Mass testing mode để tối ưu performance
        self.mass_test_mode = mass_test_mode
        # Cache cho selectors để tăng performance
        self._selector_cache = {}
        # Performance metrics
        self._performance_metrics = {
            "page_loads": 0,
            "total_load_time": 0,
            "screenshots_taken": 0,
            "retry_attempts": 0
        }

    @staticmethod
    def performance_monitor(func: Callable):
        """Decorator để monitor performance của các operations"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            try:
                result = func(self, *args, **kwargs)
                execution_time = time.time() - start_time
                
                # Log performance metrics
                if hasattr(self, 'mass_test_mode') and self.mass_test_mode:
                    self.logger.debug(f"{func.__name__} executed in {execution_time:.3f}s")
                
                # Update metrics
                if hasattr(self, '_performance_metrics'):
                    self._performance_metrics['total_load_time'] += execution_time
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                self.logger.error(f"{func.__name__} failed after {execution_time:.3f}s: {e}")
                raise
        return wrapper

    @performance_monitor
    def goto(self, url: str, wait_until: Literal["commit", "domcontentloaded", "load", "networkidle"] = "networkidle"):
        # Hàm điều hướng tới một URL cụ thể với performance optimization
        self.logger.info(f"Navigating to {url}")
        
        # Optimize for mass testing
        if self.mass_test_mode:
            wait_until = "domcontentloaded"  # Faster than networkidle
        
        self.page.goto(url, wait_until=wait_until)
        self._performance_metrics["page_loads"] += 1

    @performance_monitor
    def wait_for_selector(self, selector: str, timeout: int = 5000, state: Literal["attached", "detached", "hidden", "visible"] = "visible"):
        # Chờ cho đến khi selector xuất hiện trên trang với caching
        if self.mass_test_mode and timeout > 3000:
            timeout = 3000  # Reduce timeout for mass testing
        
        # Check cache first
        if selector in self._selector_cache:
            cached_state = self._selector_cache[selector]
            if cached_state == state:
                return True
        
        try:
            self.page.wait_for_selector(selector, timeout=timeout, state=state)
            # Cache the result
            self._selector_cache[selector] = state
            return True
        except PlaywrightTimeoutError:
            self.logger.error(f"Timeout waiting for selector: {selector}")
            return False

    def take_screenshot(self, name: str = "", optimize: bool = True):
        # Chụp màn hình toàn trang với optimization cho mass testing
        if not name:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        path = os.path.join("screenshots", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Optimize screenshot for mass testing
        if self.mass_test_mode and optimize:
            # Take smaller screenshots for mass testing
            self.page.screenshot(path=path, full_page=False)
        else:
            self.page.screenshot(path=path, full_page=True)
        
        self._performance_metrics["screenshots_taken"] += 1
        self.logger.info(f"Screenshot saved to {path}")
        
        # Attach to Allure report
        allure.attach.file(path, name, allure.attachment_type.PNG)
        
        return path

    def custom_assert(self, condition, message: str, take_screenshot: bool = True):
        # Hàm assert tuỳ chỉnh với enhanced error handling
        if not condition:
            self.logger.error(f"Assertion failed: {message}")
            
            if take_screenshot:
                self.take_screenshot(f"assertion_failed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
            # Add to Allure report
            allure.attach(f"Assertion failed: {message}", "Error Details", allure.attachment_type.TEXT)
            
            assert condition, message

    def is_element_visible(self, selector: str, timeout: int = 5000) -> bool:
        # Kiểm tra một phần tử có hiển thị trên trang không với caching
        try:
            # Đợi element xuất hiện trước khi check visibility
            self.page.wait_for_selector(selector, timeout=timeout, state="attached")
            return self.page.is_visible(selector)
        except Exception as e:
            self.logger.warning(f"Element {selector} not visible: {e}")
            return False

    def is_element_enabled(self, selector: str) -> bool:
        # Kiểm tra một phần tử có enable không
        try:
            return self.page.is_enabled(selector)
        except Exception:
            return False

    def is_element_disabled(self, selector: str) -> bool:
        # Kiểm tra một phần tử có disable không
        try:
            return self.page.is_disabled(selector)
        except Exception:
            return False

    @performance_monitor
    def fill_field(self, selector: str, value: str, timeout: int = 5000, retry: int = 2, clear_first: bool = True):
        # Điền giá trị vào ô input với enhanced retry mechanism
        for attempt in range(retry):
            try:
                self.logger.info(f"Filling field {selector} with value '{value}' (attempt {attempt+1})")
                
                # Clear field first if requested
                if clear_first:
                    self.page.fill(selector, "", timeout=timeout)
                
                self.page.fill(selector, value, timeout=timeout)
                return
            except Exception as e:
                self.logger.warning(f"Fill failed (attempt {attempt+1}): {e}")
                self._performance_metrics["retry_attempts"] += 1
                
                if attempt < retry - 1:
                    time.sleep(0.5 * (attempt + 1))  # Exponential backoff
                else:
                    self.custom_assert(False, f"Failed to fill field {selector} after {retry} attempts")

    @performance_monitor
    def click_button(self, selector: str, timeout: int = 5000, retry: int = 2, force: bool = False):
        # Click vào button với enhanced retry mechanism
        for attempt in range(retry):
            try:
                self.logger.info(f"Clicking button {selector} (attempt {attempt+1})")
                
                if force:
                    self.page.click(selector, timeout=timeout, force=True)
                else:
                    self.page.click(selector, timeout=timeout)
                return
            except Exception as e:
                self.logger.warning(f"Click failed (attempt {attempt+1}): {e}")
                self._performance_metrics["retry_attempts"] += 1
                
                if attempt < retry - 1:
                    time.sleep(0.5 * (attempt + 1))  # Exponential backoff
                else:
                    self.custom_assert(False, f"Failed to click button {selector} after {retry} attempts")

    def get_text(self, selector: str, timeout: int = 5000) -> str:
        # Lấy text của một phần tử trên trang với error handling
        self.logger.info(f"Getting text from {selector}")
        try:
            self.wait_for_selector(selector, timeout)
            msg = self.page.text_content(selector)
            return msg if msg is not None else ""
        except Exception as e:
            self.logger.error(f"Error getting text from {selector}: {e}")
            return ""

    def get_attribute(self, selector: str, attribute: str, timeout: int = 5000) -> Optional[str]:
        # Lấy attribute của một phần tử
        try:
            self.wait_for_selector(selector, timeout)
            return self.page.get_attribute(selector, attribute)
        except Exception as e:
            self.logger.error(f"Error getting attribute {attribute} from {selector}: {e}")
            return None

    def select_option(self, selector: str, value: str, timeout: int = 5000):
        # Chọn option từ dropdown
        try:
            self.logger.info(f"Selecting option {value} from {selector}")
            self.page.select_option(selector, value, timeout=timeout)
        except Exception as e:
            self.logger.error(f"Error selecting option {value} from {selector}: {e}")
            raise

    def wait_for_navigation(self, timeout: int = 10000):
        # Chờ navigation hoàn thành
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
        except Exception as e:
            self.logger.warning(f"Navigation timeout: {e}")

    def get_performance_metrics(self) -> Dict[str, Any]:
        # Lấy performance metrics của page
        return {
            **self._performance_metrics,
            "avg_load_time": self._performance_metrics["total_load_time"] / max(self._performance_metrics["page_loads"], 1),
            "cache_hit_rate": len(self._selector_cache) / max(self._performance_metrics["page_loads"], 1)
        }

    def clear_cache(self):
        # Clear selector cache
        self._selector_cache.clear()
        self.logger.info("Selector cache cleared")

    def optimize_for_mass_testing(self):
        # Tối ưu page cho mass testing
        if self.mass_test_mode:
            # Disable unnecessary features
            self.page.route("**/*.{png,jpg,jpeg,gif,svg,ico}", lambda route: route.abort())
            self.page.route("**/*.{css}", lambda route: route.abort())
            
            # Set faster timeouts
            self.page.set_default_timeout(5000)  # 5 seconds
            self.page.set_default_navigation_timeout(10000)  # 10 seconds
            
            self.logger.info("Page optimized for mass testing")

    def wait_for_network_idle(self, timeout: int = 10000):
        # Chờ network idle với timeout
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
        except Exception as e:
            self.logger.warning(f"Network idle timeout: {e}")

    def scroll_to_element(self, selector: str, timeout: int = 5000):
        # Scroll đến element
        try:
            self.page.locator(selector).scroll_into_view_if_needed(timeout=timeout)
        except Exception as e:
            self.logger.error(f"Error scrolling to {selector}: {e}")

    def hover_element(self, selector: str, timeout: int = 5000):
        # Hover over element
        try:
            self.page.hover(selector, timeout=timeout)
        except Exception as e:
            self.logger.error(f"Error hovering over {selector}: {e}")

    def get_element_count(self, selector: str) -> int:
        # Đếm số lượng elements matching selector
        try:
            return len(self.page.query_selector_all(selector))
        except Exception as e:
            self.logger.error(f"Error counting elements {selector}: {e}")
            return 0 