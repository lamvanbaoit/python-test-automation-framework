# Pages Module - Page Object Model (POM)

## Cấu trúc thư mục

```
pages/
├── __init__.py              # Module initialization và exports
├── README.md               # Tài liệu này
├── base/                   # Base classes và common functionality
│   ├── __init__.py
│   ├── base_page.py        # BasePage class - lớp cơ sở cho tất cả Page Objects
│   └── common_actions.py   # Common UI actions (sẽ tạo sau)
├── locators/               # Page locators và selectors
│   ├── __init__.py
│   ├── login_locators.py   # Selectors cho login page
│   ├── inventory_locators.py # Selectors cho inventory page
│   ├── cart_locators.py    # Selectors cho cart page
│   └── common_locators.py  # Common selectors (sẽ tạo sau)
├── auth/                   # Authentication related pages
│   ├── __init__.py
│   ├── login_page.py       # LoginPage class
│   └── register_page.py    # RegisterPage class (mẫu)
├── inventory/              # Inventory và product pages
│   ├── __init__.py
│   ├── inventory_page.py   # InventoryPage class
│   ├── product_page.py     # ProductPage class (sẽ tạo sau)
│   └── cart_page.py        # CartPage class (mẫu)
├── checkout/               # Checkout process pages
│   ├── __init__.py
│   ├── checkout_page.py    # CheckoutPage class (sẽ tạo sau)
│   └── confirmation_page.py # ConfirmationPage class (sẽ tạo sau)
└── admin/                  # Admin và management pages
    ├── __init__.py
    ├── admin_dashboard.py  # AdminDashboardPage class (sẽ tạo sau)
    └── user_management.py  # UserManagementPage class (sẽ tạo sau)
```

## Lợi ích của cấu trúc mới

### 1. **Tổ chức rõ ràng**
- Phân chia theo chức năng: auth, inventory, checkout, admin
- Tách biệt locators và page objects
- Base classes riêng biệt

### 2. **Dễ mở rộng**
- Thêm page mới chỉ cần tạo file trong thư mục phù hợp
- Locators được tổ chức theo từng trang
- Không ảnh hưởng đến các page khác

### 3. **Dễ bảo trì**
- Mỗi page có locators riêng
- Base functionality được chia sẻ
- Import paths rõ ràng

### 4. **Performance optimization**
- BasePage có performance monitoring
- Caching cho selectors
- Mass testing support

## Cách sử dụng

### Import Page Objects
```python
# Import từ module chính
from pages import LoginPage, InventoryPage

# Hoặc import trực tiếp
from pages.auth.login_page import LoginPage
from pages.inventory.inventory_page import InventoryPage
```

### Import Locators
```python
# Import locators
from pages.locators.login_locators import LOGIN_PAGE_SELECTORS
from pages.locators.inventory_locators import INVENTORY_PAGE_SELECTORS
```

### Tạo Page Object mới
```python
# Ví dụ: tạo ProductPage
from ..base.base_page import BasePage
from ..locators.product_locators import PRODUCT_PAGE_SELECTORS

class ProductPage(BasePage):
    def __init__(self, page, selectors=None):
        super().__init__(page)
        self.selectors = selectors or PRODUCT_PAGE_SELECTORS
```

## Quy tắc đặt tên

1. **Page Objects**: `{PageName}Page` (ví dụ: `LoginPage`, `InventoryPage`)
2. **Locators**: `{PAGE_NAME}_SELECTORS` (ví dụ: `LOGIN_PAGE_SELECTORS`)
3. **Files**: `{page_name}_page.py` (ví dụ: `login_page.py`)
4. **Directories**: lowercase với underscore (ví dụ: `auth`, `inventory`)

## Migration từ cấu trúc cũ

Các file đã được di chuyển:
- `base_page.py` → `base/base_page.py`
- `login_page.py` → `auth/login_page.py`
- `inventory_page.py` → `inventory/inventory_page.py`
- `login_locators.py` → `locators/login_locators.py`

Các test files đã được cập nhật để sử dụng import paths mới. 