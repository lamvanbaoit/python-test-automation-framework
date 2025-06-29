# Python Test Automation Framework

[![Test Automation Framework](https://github.com/lamvanbaoit/python-test-automation-framework/workflows/Test%20Automation%20Framework/badge.svg)](https://github.com/lamvanbaoit/python-test-automation-framework/actions)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.44%2B-green.svg)](https://playwright.dev/)
[![Allure](https://img.shields.io/badge/allure-2.24%2B-orange.svg)](https://docs.qameta.io/allure/)

Framework test automation hoàn chỉnh sử dụng **Playwright + Pytest + Page Object Model (POM)** với hỗ trợ UI Testing, API Testing, gRPC Testing và **Allure Framework** cho report step-by-step chuyên nghiệp.

> 🚀 **Mới?** Xem [QUICK_START.md](QUICK_START.md) để chạy nhanh trong 5 phút!

## 🚀 Features

- **UI Testing**: Playwright với Page Object Model nâng cao
- **API Testing**: REST API với requests library
- **gRPC Testing**: gRPC client với protobuf
- **Multi-browser**: Hỗ trợ Chromium, Firefox, WebKit
- **Multi-environment**: Dev, Staging, Production
- **Advanced Reporting**: Pytest-HTML, **Allure Framework** (step-by-step)
- **Screenshot & Logging**: Tự động chụp screenshot khi fail
- **Parallel Execution**: Chạy test song song với pytest-xdist
- **Common Functions**: Thư viện hàm tiện ích dùng chung
- **Allure Helpers**: Step-by-step reporting như ZaloPay

## 📁 Project Structure

```
Playwright/
├── api_clients/           # API & gRPC clients
│   ├── user_api_client.py
│   └── order_grpc_client.py
├── config/               # Cấu hình môi trường
│   └── settings.py
├── pages/                # Page Objects
│   ├── base_page.py      # Base class cho tất cả pages
│   ├── login_page.py     # Login page object
│   └── locators.py       # Quản lý selector tập trung
├── tests/                # Test cases
│   ├── test_login_ui.py  # UI tests
│   ├── test_login_ui_allure.py  # UI tests với Allure
│   ├── test_user_api.py  # API tests
│   └── test_order_grpc.py # gRPC tests
├── utils/                # Helper functions
│   ├── helpers.py
│   ├── common_functions.py # Thư viện hàm tiện ích
│   └── allure_helpers.py # Allure reporting helpers
├── screenshots/          # Screenshots khi test fail
├── conftest.py           # Pytest configuration & fixtures
├── requirements.txt      # Dependencies
└── README.md
```

## 🛠️ Setup

### 1. Clone & Navigate
```bash
cd /Users/lap14947/Documents/Playwright
```

### 2. Tạo Virtual Environment
```bash
python3 -m venv .venv
```

### 3. Kích hoạt Virtual Environment
```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 4. Cài đặt Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Cài đặt Playwright Browsers
```bash
playwright install
```

### 6. Cài đặt Allure Framework

Có 3 cách cài đặt Allure Framework:

#### **Cách 1: Cài đặt Global (Khuyến nghị)**
```bash
# macOS
brew install allure

# Windows
scoop install allure

# Linux
wget -qO- https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.24.0/allure-commandline-2.24.0.tgz | tar -xz -C /opt/
sudo ln -s /opt/allure-2.24.0/bin/allure /usr/bin/allure
```

#### **Cách 2: Cài đặt qua NPM (Local)**
```bash
# Cài đặt Node.js và NPM trước
npm install --save-dev allure-commandline

# Sử dụng với npx
npx allure --version
```

#### **Cách 3: Cài đặt Local trong Source Code**
```bash
# Sử dụng script tự động
python allure_runner.py install

# Hoặc chạy demo script (tự động cài đặt)
python run_allure_demo.py
```

#### **Kiểm tra cài đặt:**
```bash
# Global
allure --version

# NPM
npx allure --version

# Local
python allure_runner.py serve
```

## 🚀 Quick Start

### Chạy toàn bộ test
```bash
pytest
```

### Chạy test cụ thể
```bash
# UI Test
pytest tests/test_login_ui.py

# UI Test với Allure
pytest tests/test_login_ui_allure.py

# API Test  
pytest tests/test_user_api.py

# gRPC Test
pytest tests/test_order_grpc.py
```

### Chạy với tùy chọn
```bash
# Chọn browser
pytest --test-browser=firefox

# Chọn base URL
pytest --app-base-url=https://staging.example.com

# Chạy song song
pytest -n auto
```

### Chạy theo nhóm test
```bash
# Smoke tests (nhanh)
pytest -m smoke

# Regression tests (đầy đủ)
pytest -m regression

# UI tests
pytest -m ui

# API tests
pytest -m api

# gRPC tests
pytest -m grpc

# Allure tests
pytest -m allure
```

## 🛠️ Development Tools

### Code Quality Tools
```bash
# Format code
python scripts/dev_tools.py format

# Lint code
python scripts/dev_tools.py lint

# Type check
python scripts/dev_tools.py type

# Chạy tất cả checks
python scripts/dev_tools.py all
```

### Test Tools
```bash
# Chạy tests nhanh
python scripts/dev_tools.py test

# Chạy smoke tests
python scripts/dev_tools.py smoke

# Chạy tests với Allure
python scripts/dev_tools.py allure

# Mở Allure report
python scripts/dev_tools.py report
```

### Manual Commands
```bash
# Format code với Black
black .

# Lint với Flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Type check với MyPy
mypy . --ignore-missing-imports
```

## 📊 Reporting

### Pytest-HTML Report
```bash
pytest --html=report.html --self-contained-html
```

### 🎯 **Allure Framework Report (Step-by-Step như ZaloPay)**

#### Chạy test và tạo Allure report
```bash
# Chạy test với Allure
pytest tests/test_login_ui_allure.py --alluredir=allure-results

# Xem report
allure serve allure-results
```

#### Tạo report HTML static
```bash
# Generate HTML report
allure generate allure-results --clean -o allure-report

# Mở report
allure open allure-report
```

#### Report features:
- ✅ **Step-by-step execution** như ZaloPay
- ✅ **Screenshots tự động** cho mỗi step
- ✅ **Test data tracking** 
- ✅ **Environment info**
- ✅ **Assertion details**
- ✅ **Error analysis**
- ✅ **Timeline view**
- ✅ **Trends & statistics**

### 📊 **Hướng dẫn mở Allure Report**

> 📖 **Xem hướng dẫn chi tiết:** [OPEN_REPORT_GUIDE.md](OPEN_REPORT_GUIDE.md)

#### **🚀 Cách nhanh nhất:**
```bash
# Tự động detect và mở
python open_allure_report.py auto

# Serve mode (real-time)
python open_allure_report.py serve

# Generate HTML
python open_allure_report.py generate
```

#### **Cách 1: Serve Report (Khuyến nghị cho development)**
```bash
# Mở report với local server - tự động mở browser
allure serve allure-results

# Hoặc với NPM
npx allure serve allure-results

# Hoặc với local runner
python allure_runner.py serve allure-results

# Hoặc với Python script
python open_allure_report.py serve allure-results
```
- ✅ **Tự động mở browser** tại `http://localhost:8080`
- ✅ **Real-time updates** khi có thay đổi
- ✅ **Không cần lưu file** - temporary directory
- ✅ **Phù hợp cho development** và testing

#### **Cách 2: Generate và Mở HTML Report (Khuyến nghị cho sharing)**
```bash
# Bước 1: Generate HTML report
allure generate allure-results --clean -o allure-report

# Bước 2: Mở report
allure open allure-report

# Hoặc mở trực tiếp trong browser
open allure-report/index.html  # macOS
start allure-report/index.html  # Windows
xdg-open allure-report/index.html  # Linux
```
- ✅ **Report được lưu** trong `allure-report/` directory
- ✅ **Có thể share** qua email, Slack, file hosting
- ✅ **Phù hợp cho sharing** với team

#### **Cách 3: Sử dụng Demo Script**
```bash
# Chạy demo tự động (bao gồm cài đặt, chạy test, tạo report)
python run_allure_demo.py
```

#### **Cách 4: Sử dụng NPM Scripts**
```bash
# Chạy test và tạo report
npm run test:allure

# Serve report
npm run allure:serve

# Generate và mở report
npm run allure:generate
npm run allure:open
```

### 🚨 **Troubleshooting mở report**

#### **Vấn đề: Report cứ load và không lên**
**Nguyên nhân:** CORS Policy khi mở file HTML trực tiếp

**Giải pháp:**
```bash
# Cách 1: Sử dụng HTTP Server (Khuyến nghị)
cd allure-report
python -m http.server 8080
open http://localhost:8080

# Cách 2: Sử dụng Allure Serve
npx allure serve allure-results

# Cách 3: Sử dụng Python Script
python open_allure_report.py serve allure-results
```

#### **Port 8080 bị chiếm:**
```bash
# Dùng port khác
allure serve allure-results --port 8081
npx allure serve allure-results --port 8081
python open_allure_report.py serve allure-results 8081
```

#### **Report không hiển thị:**
```bash
# Clear cache và regenerate
rm -rf allure-results allure-report
pytest tests/ --alluredir=allure-results
allure generate allure-results --clean -o allure-report
```

#### **Browser không mở tự động:**
```bash
# Mở thủ công
open http://localhost:8080  # macOS
start http://localhost:8080  # Windows
xdg-open http://localhost:8080  # Linux
```

#### **Allure chưa cài đặt:**
```bash
# Cài đặt global
brew install allure  # macOS

# Hoặc cài đặt local
npm install --save-dev allure-commandline
python allure_runner.py install
```

> 🔍 **Xem troubleshooting chi tiết:** [OPEN_REPORT_GUIDE.md#troubleshooting](OPEN_REPORT_GUIDE.md#troubleshooting)

## 🧪 Writing Tests với Allure

### 1. UI Test với Step-by-Step Reporting

```python
# tests/test_example_allure.py
import allure
from pages.login_page import LoginPage
from utils.allure_helpers import AllureReporter

@allure.feature("Authentication")
@allure.story("User Login")
class TestLoginWithAllure:
    
    @allure.testcase("TC001", "Login Success")
    def test_login_success_with_steps(self, page):
        # Step 1: Navigate
        AllureReporter.navigate_to("https://example.com")
        login_page = LoginPage(page)
        login_page.goto()
        
        # Step 2: Fill credentials
        AllureReporter.fill_field_step("Username", "testuser")
        AllureReporter.fill_field_step("Password", "***")
        login_page.login("testuser", "password")
        
        # Step 3: Take screenshot
        AllureReporter.take_screenshot_step(page, "After Login")
        
        # Step 4: Assert
        AllureReporter.assert_step("Login successful", True, login_page.is_logged_in())
        assert login_page.is_logged_in()
```

### 2. API Test với Allure

```python
# tests/test_api_allure.py
from utils.allure_helpers import AllureReporter

def test_api_with_allure(api_client):
    # Step 1: Prepare request
    request_data = {"username": "test", "password": "pass"}
    AllureReporter.api_request_step("POST", "/login", request_data)
    
    # Step 2: Make request
    response = api_client.login("test", "pass")
    
    # Step 3: Log response
    AllureReporter.api_response_step(response.status_code, response.json())
    
    # Step 4: Assert
    AllureReporter.assert_step("Status code", 200, response.status_code)
    assert response.status_code == 200
```

### 3. Allure Decorators

```python
import allure

@allure.feature("Feature Name")
@allure.story("Story Name")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Test description")
@allure.testcase("TC001", "Test Case Name")
@allure.issue("BUG-001", "https://jira.example.com/browse/BUG-001")
def test_with_allure_decorators():
    pass
```

## 📝 Page Object Model

### Tạo Page Object mới

```python
# pages/inventory_page.py
from .base_page import BasePage
from .locators import INVENTORY_PAGE_SELECTORS

class InventoryPage(BasePage):
    def __init__(self, page, selectors=None):
        super().__init__(page)
        self.selectors = selectors or INVENTORY_PAGE_SELECTORS
    
    def add_item_to_cart(self, item_name):
        self.click_button(f"button[data-test='add-to-cart-{item_name}']")
    
    def go_to_cart(self):
        self.click_button(self.selectors["cart_button"])
```

### Thêm Selector mới

```python
# pages/locators.py
INVENTORY_PAGE_SELECTORS = {
    "inventory_container": ".inventory_list",
    "cart_button": ".shopping_cart_link",
    "add_to_cart_button": "button[data-test^='add-to-cart']",
}
```

## 🔧 Common Functions

### Tạo Test Data
```python
from utils.common_functions import CommonFunctions

# Tạo user test
user = CommonFunctions.generate_test_data("user")

# Tạo order test  
order = CommonFunctions.generate_test_data("order")

# Tạo product test
product = CommonFunctions.generate_test_data("product")
```

### Screenshot với Metadata
```python
# Chụp screenshot với thông tin
CommonFunctions.save_screenshot_with_metadata(
    page, 
    "test_screenshot.png",
    {"test_name": "login_test", "user": user}
)
```

### Retry Action
```python
# Thực hiện action với retry
CommonFunctions.retry_action(
    lambda: page.click("button"),
    max_retries=3,
    delay=1.0
)
```

## 🌍 Environment Configuration

### Cấu hình môi trường
```python
# config/settings.py
BASE_URL = "https://www.saucedemo.com/"
API_BASE_URL = "https://api.example.com"
GRPC_SERVER = "localhost:50051"
```

### Chạy với môi trường khác
```bash
# Staging
pytest --app-base-url=https://staging.example.com

# Production  
pytest --app-base-url=https://prod.example.com
```

## 🔍 Debug & Troubleshooting

### Xem log chi tiết
```bash
# Log được lưu trong test.log
tail -f test.log
```

### Screenshot khi fail
- Screenshots tự động được lưu trong thư mục `screenshots/`
- Metadata được lưu kèm theo file JSON
- Allure tự động attach screenshot vào report

### Chạy với browser hiển thị
```bash
# Mặc định headless=False trong conftest.py
pytest tests/test_login_ui.py
```

## 📚 Best Practices

### 1. Page Object Model
- Tách biệt logic test và UI interaction
- Sử dụng selector tập trung trong `locators.py`
- Kế thừa `BasePage` cho các page mới

### 2. Test Data Management
- Sử dụng `CommonFunctions.generate_test_data()` cho dữ liệu động
- Tránh hardcode dữ liệu trong test

### 3. Error Handling
- Sử dụng `custom_assert()` thay vì `assert` thông thường
- Tự động chụp screenshot khi fail

### 4. Logging
- Sử dụng `log_test_info()` để log thông tin test
- Log được lưu vào file và console

### 5. Allure Reporting
- Sử dụng `AllureReporter` cho step-by-step reporting
- Thêm decorators phù hợp cho test cases
- Attach screenshots và data vào report

## 🚀 Advanced Usage

### Parallel Execution
```bash
# Cài đặt
pip install pytest-xdist

# Chạy song song
pytest -n auto
```

### Custom Fixtures
```python
# conftest.py
@pytest.fixture
def test_user():
    return CommonFunctions.generate_test_data("user")
```

### BaseTest Class
```python
# Kế thừa BaseTest cho test class
class TestLogin(BaseTest):
    def test_login_quick(self, page):
        self.login_quick(page, "username", "password")
```

### Allure Environment Variables
```bash
# Tạo file environment.properties
echo "Browser=Chrome" > allure-results/environment.properties
echo "Version=1.0.0" >> allure-results/environment.properties
echo "Platform=macOS" >> allure-results/environment.properties
```

## 📞 Support

- **Documentation**: Xem comments trong code
- **Issues**: Kiểm tra log file `test.log`
- **Screenshots**: Xem thư mục `screenshots/` khi test fail
- **Allure Report**: Xem step-by-step execution trong Allure

## 🔄 Updates

Framework được thiết kế để dễ mở rộng:
- Thêm page objects mới trong `pages/`
- Thêm test cases mới trong `tests/`
- Thêm common functions trong `utils/common_functions.py`
- Thêm Allure helpers trong `utils/allure_helpers.py`
- Cập nhật selectors trong `pages/locators.py`

## 🎯 **Allure Report Features (như ZaloPay)**

### Step-by-Step Execution
- Mỗi action được log thành step riêng biệt
- Screenshots tự động cho mỗi step quan trọng
- Timeline view cho toàn bộ test execution

### Rich Attachments
- Screenshots với metadata
- API request/response data
- Test data và environment info
- Error details và stack traces

### Analytics & Trends
- Test execution trends
- Failure analysis
- Performance metrics
- Environment comparison

### Integration Ready
- JIRA integration
- Slack notifications
- CI/CD pipeline support
- Custom dashboards 