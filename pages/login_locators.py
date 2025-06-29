# pages/locators.py

# Định nghĩa các selector cho các trang (login, inventory, cart) để dễ tái sử dụng và bảo trì

LOGIN_PAGE_SELECTORS = {
    # Selector cho ô nhập username
    "username": 'input[data-test="username"]',
    # Selector cho ô nhập password
    "password": 'input[data-test="password"]',
    # Selector cho nút login
    "login_button": 'input[data-test="login-button"]',
    # Selector cho thông báo lỗi khi login
    "error_message": 'h3[data-test="error"]',
    # Selector cho container của trang login
    "login_container": ".login_container"
}

INVENTORY_PAGE_SELECTORS = {
    # Selector cho danh sách sản phẩm
    "inventory_container": ".inventory_list",
    # Selector cho từng sản phẩm
    "inventory_items": ".inventory_item",
    # Selector cho nút giỏ hàng
    "cart_button": ".shopping_cart_link",
    # Selector cho badge số lượng sản phẩm trong giỏ
    "cart_badge": ".shopping_cart_badge",
    # Selector cho dropdown sắp xếp sản phẩm
    "sort_dropdown": "[data-test='product_sort_container']",
    # Selector cho nút menu
    "menu_button": "#react-burger-menu-btn",
    # Selector cho link logout
    "logout_link": "#logout_sidebar_link"
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