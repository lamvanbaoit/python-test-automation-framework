# pages/locators.py

LOGIN_PAGE_SELECTORS = {
    "username": 'input[data-test="username"]',
    "password": 'input[data-test="password"]',
    "login_button": 'input[data-test="login-button"]',
    "error_message": 'h3[data-test="error"]',
    "login_container": ".login_container"
}

INVENTORY_PAGE_SELECTORS = {
    "inventory_container": ".inventory_list",
    "inventory_items": ".inventory_item",
    "cart_button": ".shopping_cart_link",
    "cart_badge": ".shopping_cart_badge",
    "sort_dropdown": "[data-test='product_sort_container']",
    "menu_button": "#react-burger-menu-btn",
    "logout_link": "#logout_sidebar_link"
}

CART_PAGE_SELECTORS = {
    "cart_container": ".cart_list",
    "cart_items": ".cart_item",
    "checkout_button": "[data-test='checkout']",
    "continue_shopping": "[data-test='continue-shopping']",
    "remove_button": "[data-test^='remove-']"
} 