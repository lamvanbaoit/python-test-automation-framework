"""
Inventory Page Locators
======================

Chứa tất cả các selectors và locators cho Inventory page.
"""

# Selectors cho Inventory page
INVENTORY_PAGE_SELECTORS = {
    # Container chính
    "inventory_container": ".inventory_container",
    
    # Danh sách sản phẩm
    "inventory_items": ".inventory_item",
    
    # Nút giỏ hàng
    "cart_button": ".shopping_cart_link",
    "cart_badge": ".shopping_cart_badge",
    
    # Dropdown sắp xếp
    "sort_dropdown": "[data-test='product_sort_container']",
    
    # Menu
    "menu_button": "#react-burger-menu-btn",
    "menu_items": ".bm-item-list",
    
    # Footer
    "footer": ".footer",
    
    # Social media links
    "twitter_link": "[data-test='social-twitter']",
    "facebook_link": "[data-test='social-facebook']",
    "linkedin_link": "[data-test='social-linkedin']",
} 