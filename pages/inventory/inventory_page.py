from ..base.base_page import BasePage
from ..locators.inventory_locators import INVENTORY_PAGE_SELECTORS
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
        AllureReporter.navigate_to(self.base_url)
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
        AllureReporter.validate_element_step("Inventory items", "get all")
        items = self.page.locator(self.selectors["inventory_items"]).all()
        self.logger.info(f"Found {len(items)} inventory items")
        return items
    
    def add_item_to_cart(self, item_name):
        """Thêm một sản phẩm vào giỏ hàng theo tên"""
        AllureReporter.click_element_step(f"Add to cart: {item_name}", f"[data-test='add-to-cart-{item_name}']")
        try:
            add_button = self.page.locator(f"[data-test='add-to-cart-{item_name}']")
            if add_button.is_visible():
                add_button.click()
                self.logger.info(f"Added {item_name} to cart")
                return True
            else:
                self.logger.warning(f"Add to cart button not found for {item_name}")
                return False
        except Exception as e:
            self.logger.error(f"Error adding {item_name} to cart: {e}")
            return False
    
    def remove_item_from_cart(self, item_name):
        """Xoá một sản phẩm khỏi giỏ hàng theo tên"""
        AllureReporter.click_element_step(f"Remove from cart: {item_name}", f"[data-test='remove-{item_name}']")
        try:
            remove_button = self.page.locator(f"[data-test='remove-{item_name}']")
            if remove_button.is_visible():
                remove_button.click()
                self.logger.info(f"Removed {item_name} from cart")
                return True
            else:
                self.logger.warning(f"Remove button not found for {item_name}")
                return False
        except Exception as e:
            self.logger.error(f"Error removing {item_name} from cart: {e}")
            return False
    
    def go_to_cart(self):
        """Đi tới trang giỏ hàng"""
        AllureReporter.navigate_to("Cart page")
        try:
            cart_link = self.page.locator(self.selectors["cart_button"])
            cart_link.click()
            self.logger.info("Navigated to cart page")
        except Exception as e:
            self.logger.error(f"Error navigating to cart: {e}")
    
    def get_cart_count(self):
        """Lấy số lượng sản phẩm trong giỏ hàng"""
        try:
            cart_badge = self.page.locator(self.selectors["cart_badge"])
            if cart_badge.is_visible():
                count_text = cart_badge.text_content()
                return int(count_text) if count_text else 0
            return 0
        except Exception as e:
            self.logger.error(f"Error getting cart count: {e}")
            return 0
    
    def sort_items_by(self, sort_option):
        """Sắp xếp sản phẩm theo tuỳ chọn"""
        AllureReporter.validate_element_step("Sort items", sort_option)
        try:
            sort_dropdown = self.page.locator(self.selectors["sort_dropdown"])
            sort_dropdown.select_option(value=sort_option)
            self.logger.info(f"Sorted items by {sort_option}")
            return True
        except Exception as e:
            self.logger.error(f"Error sorting items: {e}")
            return False
    
    def get_item_price(self, item_name):
        """Lấy giá của một sản phẩm theo tên"""
        try:
            price_element = self.page.locator(f"[data-test='inventory-item-price']").first
            if price_element.is_visible():
                return price_element.text_content()
            return "N/A"
        except Exception as e:
            self.logger.error(f"Error getting item price: {e}")
            return "N/A"
    
    def validate_inventory_page(self):
        """Kiểm tra các thành phần chính trên trang inventory"""
        AllureReporter.validate_element_step("Inventory container", "visible")
        assert self.is_inventory_page_loaded(), "Inventory page not loaded"
        self.logger.info("Inventory page validation passed")
    
    def take_inventory_screenshot(self, description="Inventory Page"):
        """Chụp màn hình trang inventory"""
        AllureReporter.take_screenshot_step(self.page, description)
        self.take_screenshot()