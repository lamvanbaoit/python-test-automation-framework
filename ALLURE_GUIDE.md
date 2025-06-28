# 🎯 Allure Framework Guide - Step-by-Step Reporting như ZaloPay

## 📋 Tổng quan

Allure Framework là công cụ reporting chuyên nghiệp nhất hiện tại, được sử dụng bởi các công ty lớn như ZaloPay để tạo report step-by-step chi tiết cho test automation.

## 🚀 Quick Start

### 1. Cài đặt Allure Framework

```bash
# macOS
brew install allure

# Windows
scoop install allure

# Linux
wget -qO- https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.24.0/allure-commandline-2.24.0.tgz | tar -xz -C /opt/
sudo ln -s /opt/allure-2.24.0/bin/allure /usr/bin/allure
```

### 2. Chạy test với Allure

```bash
# Chạy test và tạo results
pytest tests/test_login_ui_allure.py --alluredir=allure-results -v

# Xem report với server
allure serve allure-results

# Tạo HTML report static
allure generate allure-results --clean -o allure-report
```

### 3. Sử dụng Demo Script

```bash
# Chạy demo tự động
python run_allure_demo.py
```

## 📊 Allure Report Features

### ✅ Step-by-Step Execution
- Mỗi action được log thành step riêng biệt
- Screenshots tự động cho mỗi step quan trọng
- Timeline view cho toàn bộ test execution

### ✅ Rich Attachments
- Screenshots với metadata
- API request/response data
- Test data và environment info
- Error details và stack traces

### ✅ Analytics & Trends
- Test execution trends
- Failure analysis
- Performance metrics
- Environment comparison

## 🧪 Writing Tests với Allure

### 1. Basic Test với Allure

```python
import allure
from utils.allure_helpers import AllureReporter

@allure.feature("Authentication")
@allure.story("User Login")
class TestLoginWithAllure:
    
    @allure.testcase("TC001", "Login Success")
    def test_login_success_with_steps(self, page):
        # Step 1: Navigate
        AllureReporter.navigate_to("https://example.com")
        
        # Step 2: Fill credentials
        AllureReporter.fill_field_step("Username", "testuser")
        AllureReporter.fill_field_step("Password", "***")
        
        # Step 3: Take screenshot
        AllureReporter.take_screenshot_step(page, "After Login")
        
        # Step 4: Assert
        AllureReporter.assert_step("Login successful", True, True)
```

### 2. Allure Decorators

```python
import allure

@allure.feature("Feature Name")           # Feature category
@allure.story("Story Name")              # User story
@allure.severity(allure.severity_level.CRITICAL)  # Severity level
@allure.description("Test description")   # Test description
@allure.testcase("TC001", "Test Case Name")  # Test case ID
@allure.issue("BUG-001", "https://jira.example.com/browse/BUG-001")  # Issue link
def test_with_allure_decorators():
    pass
```

### 3. AllureReporter Methods

```python
from utils.allure_helpers import AllureReporter

# Navigation
AllureReporter.navigate_to("https://example.com")

# Form actions
AllureReporter.fill_field_step("Username", "testuser")
AllureReporter.click_element_step("Login Button", "#login-btn")

# Validation
AllureReporter.validate_element_step("Dashboard", "visible")

# Screenshots
AllureReporter.take_screenshot_step(page, "After Login")

# API calls
AllureReporter.api_request_step("POST", "/login", {"user": "test"})
AllureReporter.api_response_step(200, {"token": "abc123"})

# Assertions
AllureReporter.assert_step("Login successful", True, True)

# Test data
AllureReporter.test_data_step("User Data", {"username": "test"})

# Environment info
AllureReporter.environment_step("Chrome", "https://example.com", "test")
```

## 🎨 Allure Report Sections

### 1. Overview
- Test execution summary
- Pass/Fail statistics
- Duration trends
- Environment info

### 2. Behaviors
- Features và Stories
- Test cases grouped by functionality
- Step-by-step execution details

### 3. Suites
- Test suites và test classes
- Execution timeline
- Detailed test results

### 4. Timeline
- Chronological view of test execution
- Parallel execution visualization
- Performance analysis

### 5. Categories
- Defect classification
- Custom failure categories
- Issue tracking integration

## 🔧 Configuration

### 1. Environment Properties

```bash
# allure-results/environment.properties
Browser=Chrome
BaseURL=https://www.saucedemo.com/
Headless=False
Platform=macOS
PythonVersion=3.9.0
Framework=Playwright + Pytest + Allure
```

### 2. Allure Categories

```xml
<!-- allure-results/categories.json -->
[
  {
    "name": "Product defects",
    "matchedStatuses": ["failed"]
  },
  {
    "name": "Test defects",
    "matchedStatuses": ["broken"]
  },
  {
    "name": "Won't fix",
    "matchedStatuses": ["skipped"]
  }
]
```

### 3. Allure Severities

```python
# Severity levels
allure.severity_level.BLOCKER    # Critical issues
allure.severity_level.CRITICAL   # Major issues
allure.severity_level.NORMAL     # Minor issues
allure.severity_level.MINOR      # Cosmetic issues
allure.severity_level.TRIVIAL    # Trivial issues
```

## 🌐 Integration

### 1. CI/CD Pipeline

```yaml
# GitHub Actions example
- name: Run tests with Allure
  run: |
    pytest tests/ --alluredir=allure-results
    allure generate allure-results --clean -o allure-report
    
- name: Upload Allure report
  uses: actions/upload-artifact@v2
  with:
    name: allure-report
    path: allure-report/
```

### 2. JIRA Integration

```python
@allure.issue("PROJ-123", "https://jira.company.com/browse/PROJ-123")
def test_with_jira_link():
    pass
```

### 3. Slack Notifications

```python
# Custom notification
def send_allure_notification():
    allure_results = "allure-results"
    report_url = "https://your-server.com/allure-report"
    
    # Send to Slack
    slack_message = f"Test execution completed. View report: {report_url}"
    # ... send to Slack
```

## 📈 Advanced Features

### 1. Custom Allure Steps

```python
@allure.step("Custom step: {step_name}")
def custom_step(step_name, data):
    allure.attach(
        json.dumps(data, indent=2),
        f"Data for {step_name}",
        allure.attachment_type.JSON
    )
    return data
```

### 2. Dynamic Allure Properties

```python
def test_with_dynamic_properties():
    allure.dynamic.description("Dynamic description")
    allure.dynamic.feature("Dynamic feature")
    allure.dynamic.story("Dynamic story")
```

### 3. Allure Attachments

```python
# Attach file
with open("screenshot.png", "rb") as f:
    allure.attach(
        f.read(),
        "Screenshot",
        allure.attachment_type.PNG
    )

# Attach text
allure.attach(
    "Test data content",
    "Test Data",
    allure.attachment_type.TEXT
)

# Attach JSON
allure.attach(
    json.dumps(data, indent=2),
    "API Response",
    allure.attachment_type.JSON
)
```

## 🎯 Best Practices

### 1. Step Naming
- Sử dụng tên step rõ ràng, mô tả hành động
- Bao gồm thông tin quan trọng trong tên step
- Sử dụng consistent naming convention

### 2. Screenshots
- Chụp screenshot cho các step quan trọng
- Chụp screenshot khi có lỗi
- Đặt tên screenshot có ý nghĩa

### 3. Test Data
- Log test data sử dụng `AllureReporter.test_data_step()`
- Không log sensitive data (passwords, tokens)
- Sử dụng consistent data format

### 4. Assertions
- Sử dụng `AllureReporter.assert_step()` cho assertions
- Bao gồm expected và actual values
- Mô tả rõ ràng điều kiện assert

### 5. Environment Info
- Luôn include environment properties
- Log browser, OS, framework versions
- Include test execution timestamp

## 🚨 Troubleshooting

### 1. Allure không cài được
```bash
# Kiểm tra Java
java -version

# Cài Java nếu cần
# macOS: brew install openjdk
# Ubuntu: sudo apt install openjdk-11-jdk
```

### 2. Report không hiển thị
```bash
# Clear cache
rm -rf allure-results allure-report

# Regenerate report
pytest tests/ --alluredir=allure-results
allure generate allure-results --clean -o allure-report
```

### 3. Screenshots không attach
```python
# Đảm bảo page object tồn tại
if page and not page.is_closed():
    AllureReporter.take_screenshot_step(page, "Screenshot")
```

## 📚 Resources

- [Allure Framework Documentation](https://docs.qameta.io/allure/)
- [Allure GitHub Repository](https://github.com/allure-framework/allure2)
- [Allure Examples](https://github.com/allure-examples)
- [Allure Community](https://github.com/allure-framework/allure2/discussions)

## 🎉 Kết luận

Allure Framework cung cấp reporting chuyên nghiệp với step-by-step execution như ZaloPay, giúp team QA và developers hiểu rõ test execution flow và debug issues hiệu quả. 