# conftest.py

import pytest
import allure
import logging
import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright
from config import settings
from api_clients.user_api_client import UserApiClient
from api_clients.order_grpc_client import OrderGrpcClient
from utils.common_functions import CommonFunctions

# Cấu hình logging để ghi log ra file và hiển thị ra màn hình
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test.log'),
        logging.StreamHandler()
    ]
)

# =====================
# Thêm các tuỳ chọn dòng lệnh cho pytest (browser, base_url, headless)
# =====================
def pytest_addoption(parser):
    """Thêm command line options cho pytest"""
    parser.addoption(
        "--test-browser",
        action="store",
        default="chromium",
        help="Browser to use for testing: chromium, firefox, webkit"
    )
    parser.addoption(
        "--app-base-url",
        action="store",
        default="https://www.saucedemo.com/",
        help="Base URL for the application under test"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )

# =====================
# Cấu hình browser và context cho Playwright
# =====================
@pytest.fixture(scope="session")
def browser_type_launch_args(request):
    """Cấu hình các tham số khi khởi tạo browser"""
    browser = request.config.getoption("--test-browser")
    headless = request.config.getoption("--headless")
    
    if browser == "chromium":
        return {
            "headless": headless,
            "args": [
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor"
            ]
        }
    elif browser == "firefox":
        return {
            "headless": headless,
            "args": [
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        }
    elif browser == "webkit":
        return {
            "headless": headless,
            "args": [
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        }
    else:
        return {"headless": headless}

@pytest.fixture(scope="session")
def browser_context_args():
    """Cấu hình context cho browser (viewport, video, ...)."""
    return {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "record_video_dir": "videos/",
        "record_video_size": {"width": 1920, "height": 1080}
    }

@pytest.fixture(scope="session")
def base_url(request):
    """Base URL cho ứng dụng test"""
    return request.config.getoption("--app-base-url")

@pytest.fixture(scope="function")
def page(browser, base_url):
    """Khởi tạo page mới cho mỗi test function"""
    page = browser.new_page()
    # Set user-agent cho page
    page.set_extra_http_headers({
        "User-Agent": "Playwright Test Automation"
    })
    # Gắn mô tả môi trường vào Allure
    allure.dynamic.description(f"Test running on {base_url}")
    yield page
    # Đóng page sau khi test xong
    if not page.is_closed():
        page.close()

# =====================
# BaseTest class cho các test kế thừa
# =====================
class BaseTest:
    def login_quick(self, page, username, password):
        # Hàm login nhanh cho các test kế thừa
        from pages.login_page import LoginPage
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(username, password)
        login_page.custom_assert(login_page.is_logged_in(), "Login failed in BaseTest.login_quick")

# =====================
# Fixtures cho API/gRPC client, test data, Allure, screenshot, ...
# =====================
@pytest.fixture(scope="function")
def api_client():
    """Khởi tạo API client cho test API"""
    from api_clients.user_api_client import UserApiClient
    return UserApiClient()

@pytest.fixture(scope="function")
def grpc_client():
    """Khởi tạo gRPC client cho test gRPC"""
    from api_clients.order_grpc_client import OrderGrpcClient
    return OrderGrpcClient()

@pytest.fixture(scope="function")
def test_data():
    """Sinh dữ liệu test mẫu cho mỗi test function"""
    return CommonFunctions.generate_test_data("user")

@pytest.fixture(scope="function")
def allure_environment(request):
    """Tạo file environment.properties cho Allure report"""
    browser = request.config.getoption("--test-browser")
    base_url = request.config.getoption("--app-base-url")
    headless = request.config.getoption("--headless")
    # Tạo thư mục allure-results nếu chưa có
    allure_results_dir = "allure-results"
    os.makedirs(allure_results_dir, exist_ok=True)
    # Ghi thông tin môi trường vào file
    env_file = os.path.join(allure_results_dir, "environment.properties")
    with open(env_file, "w") as f:
        f.write(f"Browser={browser}\n")
        f.write(f"BaseURL={base_url}\n")
        f.write(f"Headless={headless}\n")
        f.write(f"Platform={os.name}\n")
        f.write(f"PythonVersion={sys.version}\n")
        f.write(f"Timestamp={datetime.now().isoformat()}\n")
    return {
        "browser": browser,
        "base_url": base_url,
        "headless": headless
    }

@pytest.fixture(autouse=True)
def setup_allure_metadata(request, allure_environment):
    """Tự động gắn metadata cho Allure report mỗi test"""
    # Gắn thông tin feature/story
    allure.dynamic.feature("Test Automation Framework")
    allure.dynamic.story("Automated Testing")
    # Gắn thông tin môi trường
    allure.attach(
        f"Browser: {allure_environment['browser']}\n"
        f"Base URL: {allure_environment['base_url']}\n"
        f"Headless: {allure_environment['headless']}\n"
        f"Test: {request.node.name}",
        "Test Environment",
        allure.attachment_type.TEXT
    )

@pytest.fixture(scope="function")
def screenshot_on_failure(page, request):
    """Tự động chụp screenshot khi test fail và attach vào Allure report"""
    yield
    # Nếu test fail thì chụp screenshot
    if request.node.rep_call.failed:
        os.makedirs("screenshots", exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        test_name = request.node.name.replace("/", "_").replace("\\", "_")
        screenshot_path = f"screenshots/failure_{test_name}_{timestamp}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        with open(screenshot_path, "rb") as f:
            allure.attach(
                f.read(),
                f"Failure Screenshot - {test_name}",
                allure.attachment_type.PNG
            )

# =====================
# Hook để capture test result cho screenshot fixture và Allure
# =====================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook để lấy kết quả test, phục vụ cho việc chụp screenshot khi fail"""
    outcome = yield
    rep = outcome.get_result()
    # Gắn thuộc tính rep_call cho request.node để fixture screenshot_on_failure sử dụng
    setattr(item, "rep_" + rep.when, rep)
    # Nếu test fail thì chụp screenshot cho pytest-html
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page", None)
        if page:
            screenshot_path = f"screenshots/{item.name}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            if hasattr(rep, "extra"):
                rep.extra.append({"name": "screenshot", "content": screenshot_path})
            else:
                rep.extra = [{"name": "screenshot", "content": screenshot_path}]
            print(f"Screenshot saved to {screenshot_path}")

# =====================
# Các fixture cho Allure report, custom marker, ...
# =====================
@pytest.fixture(scope="session")
def allure_results_dir():
    """Trả về thư mục lưu kết quả Allure"""
    return "allure-results"

@pytest.fixture(scope="session")
def allure_report_dir():
    """Trả về thư mục lưu report Allure"""
    return "allure-report"

# Đăng ký custom marker cho pytest
# =====================
def pytest_configure(config):
    """Đăng ký các custom marker cho pytest (ui, api, grpc, smoke, regression, allure)"""
    config.addinivalue_line(
        "markers", "ui: mark test as UI test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as API test"
    )
    config.addinivalue_line(
        "markers", "grpc: mark test as gRPC test"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "allure: mark test as using Allure reporting"
    )

# =====================
# Các fixture hỗ trợ Allure step logger, attach screenshot
# =====================
@pytest.fixture(scope="function")
def allure_step_logger():
    """Fixture trả về AllureReporter để log step vào Allure report"""
    from utils.allure_helpers import AllureReporter
    return AllureReporter

@pytest.fixture(scope="function")
def allure_attach_screenshot(page):
    """Fixture hỗ trợ attach screenshot vào Allure report"""
    def _attach_screenshot(description="Screenshot"):
        from utils.allure_helpers import AllureReporter
        return AllureReporter.take_screenshot_step(page, description)
    return _attach_screenshot 