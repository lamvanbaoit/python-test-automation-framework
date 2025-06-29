from .base_page import BasePage
from .login_locators import INVENTORY_PAGE_SELECTORS
import allure
from utils.allure_helpers import AllureReporter

# Page Object cho trang Inventory (sau khi đăng nhập thành công)
class InventoryPage(BasePage):
    """Page Object cho Inventory page (sau khi login thành công)"""
    
    def __init__(self, page, selectors=None):
        # Khởi tạo InventoryPage với page của Playwright và bộ selector (mặc định dùng INVENTORY_PAGE_SELECTORS)
        super().__init__(page)
        self.selectors = selectors or INVENTORY_PAGE_SELECTORS
        self.base_url = "https://www.saucedemo.com/inventory.html"
    
    def goto(self):
        """Điều hướng tới trang inventory"""
        with allure.step(f"Navigate to inventory page: {self.base_url}"):
            self.page.goto(self.base_url)
            self.logger.info(f"Navigating to {self.base_url}")
    
    def is_inventory_page_loaded(self):
        """Kiểm tra trang inventory đã load thành công chưa"""
        try:
            return self.page.locator(self.selectors["inventory_container"]).is_visible()
        except Exception as e:
            self.logger.error(f"Error checking inventory page: {e}")
            return False
    
    def get_inventory_items(self):
        """Lấy danh sách tất cả sản phẩm trên trang inventory"""
        with allure.step("Get inventory items"):
            items = self.page.locator(self.selectors["inventory_items"]).all()
            self.logger.info(f"Found {len(items)} inventory items")
            return items
    
    def add_item_to_cart(self, item_name):
        """Thêm một sản phẩm vào giỏ hàng theo tên"""
        with allure.step(f"Add item to cart: {item_name}"):
            selector = f"button[data-test='add-to-cart-{item_name}']"
            self.click_button(selector)
            AllureReporter.click_element_step(f"Add to cart button for {item_name}", selector)
    
    def remove_item_from_cart(self, item_name):
        """Xoá một sản phẩm khỏi giỏ hàng theo tên"""
        with allure.step(f"Remove item from cart: {item_name}"):
            selector = f"button[data-test='remove-{item_name}']"
            self.click_button(selector)
            AllureReporter.click_element_step(f"Remove from cart button for {item_name}", selector)
    
    def go_to_cart(self):
        """Đi tới trang giỏ hàng"""
        with allure.step("Navigate to cart"):
            self.click_button(self.selectors["cart_button"])
            AllureReporter.click_element_step("Cart button", self.selectors["cart_button"])
    
    def get_cart_count(self):
        """Lấy số lượng sản phẩm trong giỏ hàng"""
        try:
            cart_badge = self.page.locator(self.selectors["cart_badge"])
            if cart_badge.is_visible():
                text_content = cart_badge.text_content()
                if text_content:
                    return int(text_content)
            return 0
        except Exception as e:
            self.logger.error(f"Error getting cart count: {e}")
            return 0
    
    def sort_items_by(self, sort_option):
        """Sắp xếp sản phẩm theo tuỳ chọn"""
        with allure.step(f"Sort items by: {sort_option}"):
            self.page.select_option(self.selectors["sort_dropdown"], sort_option)
            AllureReporter.fill_field_step("Sort dropdown", sort_option)
    
    def get_item_price(self, item_name):
        """Lấy giá của một sản phẩm theo tên"""
        try:
            price_selector = f"[data-test='inventory-item-price']"
            items = self.page.locator(price_selector).all()
            for item in items:
                if item_name in item.locator("..").locator("[data-test='inventory-item-name']").text_content():
                    return item.text_content()
            return None
        except Exception as e:
            self.logger.error(f"Error getting item price: {e}")
            return None
    
    def validate_inventory_page(self):
        """Kiểm tra các thành phần chính trên trang inventory"""
        with allure.step("Validate inventory page elements"):
            AllureReporter.validate_element_step("Inventory container", "visible")
            assert self.is_inventory_page_loaded(), "Inventory page not loaded"
            
            AllureReporter.validate_element_step("Sort dropdown", "visible")
            assert self.page.locator(self.selectors["sort_dropdown"]).is_visible(), "Sort dropdown not visible"
            
            AllureReporter.validate_element_step("Cart button", "visible")
            assert self.page.locator(self.selectors["cart_button"]).is_visible(), "Cart button not visible"
            
            self.logger.info("Inventory page validation passed")
    
    def take_inventory_screenshot(self, description="Inventory Page"):
        """Chụp màn hình trang inventory"""
        with allure.step(f"Take screenshot: {description}"):
            AllureReporter.take_screenshot_step(self.page, description)
            self.take_screenshot() 