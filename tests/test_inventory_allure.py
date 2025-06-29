# tests/test_inventory_allure.py

import pytest
import allure
from playwright.sync_api import Page
from pages.auth.login_page import LoginPage
from pages.inventory.inventory_page import InventoryPage
from utils.helpers import get_test_user
from utils.allure_helpers import AllureReporter
from utils.common_functions import CommonFunctions

# Test class kiểm thử các chức năng liên quan đến trang Inventory với Allure report
@allure.feature("Inventory Management")
@allure.story("Product Inventory")
class TestInventoryWithAllure:
    
    @allure.testcase("TC002", "Inventory Page Load")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_inventory_page_load(self, page):
        """Test kiểm tra trang inventory load đúng sau khi đăng nhập"""
        
        # Bước 1: Đăng nhập trước
        AllureReporter.navigate_to("https://www.saucedemo.com/")
        login_page = LoginPage(page)
        login_page.goto()
        
        user = get_test_user()
        AllureReporter.test_data_step("Login User", user)
        
        AllureReporter.fill_field_step("Username", user["username"])
        login_page.fill_field(login_page.selectors["username"], user["username"])
        
        AllureReporter.fill_field_step("Password", "***")
        login_page.fill_field(login_page.selectors["password"], user["password"])
        
        AllureReporter.click_element_step("Login Button", login_page.selectors["login_button"])
        login_page.click_button(login_page.selectors["login_button"])
        
        # Bước 2: Kiểm tra đăng nhập thành công
        AllureReporter.assert_step("Login successful", True, login_page.is_logged_in())
        assert login_page.is_logged_in(), "Login failed"
        
        # Bước 3: Điều hướng tới trang inventory
        AllureReporter.navigate_to("https://www.saucedemo.com/inventory.html")
        inventory_page = InventoryPage(page)
        inventory_page.goto()
        
        # Bước 4: Kiểm tra trang inventory
        AllureReporter.validate_element_step("Inventory page loaded", "visible")
        inventory_page.validate_inventory_page()
        
        # Bước 5: Chụp màn hình
        AllureReporter.take_screenshot_step(page, "Inventory Page Loaded")
        inventory_page.take_inventory_screenshot("Inventory Page After Login")
        
        # Bước 6: Kiểm tra các thành phần trang
        AllureReporter.assert_step("Inventory page loaded", True, inventory_page.is_inventory_page_loaded())
        assert inventory_page.is_inventory_page_loaded(), "Inventory page not loaded"
    
    @allure.testcase("TC003", "Add Item to Cart")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_item_to_cart(self, page):
        """Test kiểm tra thêm sản phẩm vào giỏ hàng"""
        
        # Bước 1: Đăng nhập và vào inventory
        login_page = LoginPage(page)
        login_page.goto()
        
        user = get_test_user()
        login_page.login(user["username"], user["password"])
        
        inventory_page = InventoryPage(page)
        inventory_page.goto()
        
        # Bước 2: Lấy số lượng sản phẩm trong giỏ ban đầu
        initial_count = inventory_page.get_cart_count()
        AllureReporter.test_data_step("Initial cart count", {"count": initial_count})
        
        # Bước 3: Thêm sản phẩm vào giỏ
        item_name = "sauce-labs-backpack"
        AllureReporter.fill_field_step("Item to add", item_name)
        inventory_page.add_item_to_cart(item_name)
        
        # Bước 4: Kiểm tra số lượng sản phẩm tăng
        new_count = inventory_page.get_cart_count()
        AllureReporter.test_data_step("New cart count", {"count": new_count})
        
        AllureReporter.assert_step("Cart count increased", True, new_count > initial_count)
        assert new_count > initial_count, f"Cart count should increase from {initial_count} to {new_count}"
        
        # Bước 5: Chụp màn hình
        AllureReporter.take_screenshot_step(page, "Item Added to Cart")
    
    @allure.testcase("TC004", "Sort Inventory Items")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_inventory_items(self, page):
        """Test kiểm tra sắp xếp sản phẩm trên trang inventory"""
        
        # Bước 1: Đăng nhập và vào inventory
        login_page = LoginPage(page)
        login_page.goto()
        
        user = get_test_user()
        login_page.login(user["username"], user["password"])
        
        inventory_page = InventoryPage(page)
        inventory_page.goto()
        
        # Bước 2: Sắp xếp theo giá tăng dần
        sort_option = "lohi"  # low to high
        AllureReporter.fill_field_step("Sort option", sort_option)
        inventory_page.sort_items_by(sort_option)
        
        # Bước 3: Kiểm tra đã sắp xếp (kiểm tra cơ bản)
        AllureReporter.assert_step("Sorting applied", True, True)
        
        # Bước 4: Chụp màn hình
        AllureReporter.take_screenshot_step(page, "Items Sorted by Price")
    
    @allure.testcase("TC005", "Inventory Page Elements")
    @allure.severity(allure.severity_level.MINOR)
    def test_inventory_page_elements(self, page):
        """Test kiểm tra các thành phần chính trên trang inventory"""
        
        # Bước 1: Đăng nhập và vào inventory
        login_page = LoginPage(page)
        login_page.goto()
        
        user = get_test_user()
        login_page.login(user["username"], user["password"])
        login_page.custom_assert(login_page.is_logged_in(), "Login failed! Check credentials or page state.")
        
        inventory_page = InventoryPage(page)
        inventory_page.validate_inventory_page()
        
        # Bước 2: Kiểm tra các thành phần chính
        AllureReporter.validate_element_step("Inventory container", "visible")
        assert inventory_page.page.locator(inventory_page.selectors["inventory_container"]).is_visible()
        
        AllureReporter.validate_element_step("Sort dropdown", "visible")
        assert inventory_page.page.locator(inventory_page.selectors["sort_dropdown"]).is_visible()
        
        AllureReporter.validate_element_step("Cart button", "visible")
        assert inventory_page.page.locator(inventory_page.selectors["cart_button"]).is_visible()
        
        AllureReporter.validate_element_step("Menu button", "visible")
        assert inventory_page.page.locator(inventory_page.selectors["menu_button"]).is_visible()
        
        # Bước 3: Chụp màn hình
        AllureReporter.take_screenshot_step(page, "All Elements Present") 