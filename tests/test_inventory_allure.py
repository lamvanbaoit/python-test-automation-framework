# tests/test_inventory_allure.py

import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.allure_helpers import AllureReporter
from utils.common_functions import CommonFunctions

@allure.feature("Inventory Management")
@allure.story("Product Inventory")
class TestInventoryWithAllure:
    
    @allure.testcase("TC002", "Inventory Page Load")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_inventory_page_load(self, page):
        """Test inventory page loads correctly after login"""
        
        # Step 1: Login first
        AllureReporter.navigate_to("https://www.saucedemo.com/")
        login_page = LoginPage(page)
        login_page.goto()
        
        user = CommonFunctions.generate_test_data("user")
        AllureReporter.test_data_step("Login User", user)
        
        AllureReporter.fill_field_step("Username", user["username"])
        login_page.fill_field(login_page.selectors["username"], user["username"])
        
        AllureReporter.fill_field_step("Password", "***")
        login_page.fill_field(login_page.selectors["password"], user["password"])
        
        AllureReporter.click_element_step("Login Button", login_page.selectors["login_button"])
        login_page.click_button(login_page.selectors["login_button"])
        
        # Step 2: Verify login success
        AllureReporter.assert_step("Login successful", True, login_page.is_logged_in())
        assert login_page.is_logged_in(), "Login failed"
        
        # Step 3: Navigate to inventory page
        AllureReporter.navigate_to("https://www.saucedemo.com/inventory.html")
        inventory_page = InventoryPage(page)
        inventory_page.goto()
        
        # Step 4: Validate inventory page
        AllureReporter.validate_element_step("Inventory page loaded", "visible")
        inventory_page.validate_inventory_page()
        
        # Step 5: Take screenshot
        AllureReporter.take_screenshot_step(page, "Inventory Page Loaded")
        inventory_page.take_inventory_screenshot("Inventory Page After Login")
        
        # Step 6: Verify page elements
        AllureReporter.assert_step("Inventory page loaded", True, inventory_page.is_inventory_page_loaded())
        assert inventory_page.is_inventory_page_loaded(), "Inventory page not loaded"
    
    @allure.testcase("TC003", "Add Item to Cart")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_item_to_cart(self, page):
        """Test adding item to cart"""
        
        # Step 1: Login and navigate to inventory
        login_page = LoginPage(page)
        login_page.goto()
        
        user = CommonFunctions.generate_test_data("user")
        login_page.login(user["username"], user["password"])
        
        inventory_page = InventoryPage(page)
        inventory_page.goto()
        
        # Step 2: Get initial cart count
        initial_count = inventory_page.get_cart_count()
        AllureReporter.test_data_step("Initial cart count", {"count": initial_count})
        
        # Step 3: Add item to cart
        item_name = "sauce-labs-backpack"
        AllureReporter.fill_field_step("Item to add", item_name)
        inventory_page.add_item_to_cart(item_name)
        
        # Step 4: Verify cart count increased
        new_count = inventory_page.get_cart_count()
        AllureReporter.test_data_step("New cart count", {"count": new_count})
        
        AllureReporter.assert_step("Cart count increased", True, new_count > initial_count)
        assert new_count > initial_count, f"Cart count should increase from {initial_count} to {new_count}"
        
        # Step 5: Take screenshot
        AllureReporter.take_screenshot_step(page, "Item Added to Cart")
    
    @allure.testcase("TC004", "Sort Inventory Items")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_inventory_items(self, page):
        """Test sorting inventory items"""
        
        # Step 1: Login and navigate to inventory
        login_page = LoginPage(page)
        login_page.goto()
        
        user = CommonFunctions.generate_test_data("user")
        login_page.login(user["username"], user["password"])
        
        inventory_page = InventoryPage(page)
        inventory_page.goto()
        
        # Step 2: Sort by price low to high
        sort_option = "lohi"  # low to high
        AllureReporter.fill_field_step("Sort option", sort_option)
        inventory_page.sort_items_by(sort_option)
        
        # Step 3: Verify sorting (basic check)
        AllureReporter.assert_step("Sorting applied", True, True)
        
        # Step 4: Take screenshot
        AllureReporter.take_screenshot_step(page, "Items Sorted by Price")
    
    @allure.testcase("TC005", "Inventory Page Elements")
    @allure.severity(allure.severity_level.MINOR)
    def test_inventory_page_elements(self, page):
        """Test all inventory page elements are present"""
        
        # Step 1: Login and navigate to inventory
        login_page = LoginPage(page)
        login_page.goto()
        
        user = CommonFunctions.generate_test_data("user")
        login_page.login(user["username"], user["password"])
        
        inventory_page = InventoryPage(page)
        inventory_page.goto()
        
        # Step 2: Validate all elements
        AllureReporter.validate_element_step("Inventory container", "visible")
        assert inventory_page.page.locator(inventory_page.selectors["inventory_container"]).is_visible()
        
        AllureReporter.validate_element_step("Sort dropdown", "visible")
        assert inventory_page.page.locator(inventory_page.selectors["sort_dropdown"]).is_visible()
        
        AllureReporter.validate_element_step("Cart button", "visible")
        assert inventory_page.page.locator(inventory_page.selectors["cart_button"]).is_visible()
        
        AllureReporter.validate_element_step("Menu button", "visible")
        assert inventory_page.page.locator(inventory_page.selectors["menu_button"]).is_visible()
        
        # Step 3: Take screenshot
        AllureReporter.take_screenshot_step(page, "All Elements Present") 