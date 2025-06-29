# pages/locators.py

# Định nghĩa các selector cho các trang (login, inventory, cart) để dễ tái sử dụng và bảo trì

"""
Login Page Locators
==================

Chứa tất cả các selectors và locators cho Login page.
"""

# Selectors cho Login page (SauceDemo)
LOGIN_PAGE_SELECTORS = {
    # Form fields
    "username": "#user-name",
    "password": "#password",
    "login_button": "#login-button",
    
    # Error message
    "error_message": "[data-test='error']",
    
    # Success elements
    "user_name": ".user-name",
    "logout_button": "#logout_sidebar_link",
    
    # Form container
    "login_form": ".login-box",
    
    # Additional elements
    "new_user_button": "#newUser",
    "register_link": "text=New User",
}

# Selectors cho Inventory page (SauceDemo)
INVENTORY_PAGE_SELECTORS = {
    # Container chính
    "inventory_container": ".inventory_list",
    
    # Danh sách sản phẩm
    "inventory_items": ".inventory_item",
    
    # Nút giỏ hàng
    "cart_button": ".shopping_cart_link",
    "cart_badge": ".shopping_cart_badge",
    
    # Dropdown sắp xếp
    "sort_dropdown": "[data-test='product_sort_container']",
    
    # Menu
    "menu_button": "#react-burger-menu-btn",
    "menu_items": ".bm-menu",
    
    # Footer
    "footer": ".footer",
    
    # Profile elements
    "profile_header": ".inventory_details_name",
    "user_info": ".user-info",
}

CART_PAGE_SELECTORS = {
    # Selector cho container của trang giỏ hàng
    "cart_container": ".cart_list",
    # Selector cho từng sản phẩm trong giỏ
    "cart_items": ".cart_item",
    # Selector cho nút checkout
    "checkout_button": "[data-test='checkout']",
    # Selector cho nút tiếp tục mua hàng
    "continue_shopping": "[data-test='continue-shopping']",
    # Selector cho nút xoá sản phẩm khỏi giỏ
    "remove_button": "[data-test^='remove-']"
} 