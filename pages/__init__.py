"""
Pages Module - Page Object Model (POM) Implementation
====================================================

Cấu trúc thư mục pages/:
├── __init__.py              # Module initialization
├── base/                    # Base classes và common functionality
│   ├── __init__.py
│   ├── base_page.py         # BasePage class
│   └── common_actions.py    # Common UI actions
├── locators/                # Page locators và selectors
│   ├── __init__.py
│   ├── login_locators.py
│   ├── inventory_locators.py
│   └── common_locators.py
├── auth/                    # Authentication related pages
│   ├── __init__.py
│   ├── login_page.py
│   └── register_page.py
├── inventory/               # Inventory và product pages
│   ├── __init__.py
│   ├── inventory_page.py
│   ├── product_page.py
│   └── cart_page.py
├── checkout/                # Checkout process pages
│   ├── __init__.py
│   ├── checkout_page.py
│   └── confirmation_page.py
└── admin/                   # Admin và management pages
    ├── __init__.py
    ├── admin_dashboard.py
    └── user_management.py
"""

# Import các base classes
from .base import BasePage

# Import các page objects chính
from .auth import LoginPage
from .inventory import InventoryPage

# Import các locators
from .locators.login_locators import LOGIN_PAGE_SELECTORS
from .locators.inventory_locators import INVENTORY_PAGE_SELECTORS

__all__ = [
    # Base classes
    'BasePage',
    
    # Page Objects
    'LoginPage',
    'InventoryPage',
    
    # Locators
    'LOGIN_PAGE_SELECTORS',
    'INVENTORY_PAGE_SELECTORS',
] 