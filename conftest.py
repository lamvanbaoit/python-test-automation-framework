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

# Logging cấu hình ra file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test.log'),
        logging.StreamHandler()
    ]
)

# Đa trình duyệt, đa môi trường

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

@pytest.fixture(scope="session")
def browser_type_launch_args(request):
    """Cấu hình browser launch arguments"""
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
    """Cấu hình browser context"""
    return {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "record_video_dir": "videos/",
        "record_video_size": {"width": 1920, "height": 1080}
    }

@pytest.fixture(scope="session")
def base_url(request):
    """Base URL cho application"""
    return request.config.getoption("--app-base-url")

@pytest.fixture(scope="function")
def page(browser, base_url):
    """Page fixture với cấu hình cơ bản"""
    page = browser.new_page()
    
    # Set base URL
    page.set_extra_http_headers({
        "User-Agent": "Playwright Test Automation"
    })
    
    # Add Allure environment info
    allure.dynamic.description(f"Test running on {base_url}")
    
    yield page
    
    # Cleanup
    if not page.is_closed():
        page.close()

# BaseTest class cho các test kế thừa
class BaseTest:
    def login_quick(self, page, username, password):
        from pages.login_page import LoginPage
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(username, password)
        login_page.custom_assert(login_page.is_logged_in(), "Login failed in BaseTest.login_quick")

@pytest.fixture(scope="function")
def api_client():
    """API client fixture"""
    from api_clients.user_api_client import UserApiClient
    return UserApiClient()

@pytest.fixture(scope="function")
def grpc_client():
    """gRPC client fixture"""
    from api_clients.order_grpc_client import OrderGrpcClient
    return OrderGrpcClient()

@pytest.fixture(scope="function")
def test_data():
    """Test data fixture"""
    return CommonFunctions.generate_test_data("user")

@pytest.fixture(scope="function")
def allure_environment(request):
    """Allure environment fixture"""
    browser = request.config.getoption("--test-browser")
    base_url = request.config.getoption("--app-base-url")
    headless = request.config.getoption("--headless")
    
    # Create environment.properties for Allure
    allure_results_dir = "allure-results"
    os.makedirs(allure_results_dir, exist_ok=True)
    
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
    """Tự động setup Allure metadata cho mỗi test"""
    # Add test metadata
    allure.dynamic.feature("Test Automation Framework")
    allure.dynamic.story("Automated Testing")
    
    # Add environment info
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
    """Tự động chụp screenshot khi test fail"""
    yield
    
    # Check if test failed
    if request.node.rep_call.failed:
        # Create screenshots directory if not exists
        os.makedirs("screenshots", exist_ok=True)
        
        # Generate screenshot filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        test_name = request.node.name.replace("/", "_").replace("\\", "_")
        screenshot_path = f"screenshots/failure_{test_name}_{timestamp}.png"
        
        # Take screenshot
        page.screenshot(path=screenshot_path, full_page=True)
        
        # Attach to Allure report
        with open(screenshot_path, "rb") as f:
            allure.attach(
                f.read(),
                f"Failure Screenshot - {test_name}",
                allure.attachment_type.PNG
            )

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook để capture test result cho screenshot fixture và Allure"""
    outcome = yield
    rep = outcome.get_result()
    
    # Set attribute để screenshot fixture có thể check
    setattr(item, "rep_" + rep.when, rep)
    
    # Screenshot cho pytest-html
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

@pytest.fixture(scope="session")
def allure_results_dir():
    """Allure results directory"""
    return "allure-results"

@pytest.fixture(scope="session")
def allure_report_dir():
    """Allure report directory"""
    return "allure-report"

# Custom markers
def pytest_configure(config):
    """Cấu hình custom markers"""
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

# Allure specific fixtures
@pytest.fixture(scope="function")
def allure_step_logger():
    """Allure step logger fixture"""
    from utils.allure_helpers import AllureReporter
    return AllureReporter

@pytest.fixture(scope="function")
def allure_attach_screenshot(page):
    """Allure screenshot attachment fixture"""
    def _attach_screenshot(description="Screenshot"):
        from utils.allure_helpers import AllureReporter
        return AllureReporter.take_screenshot_step(page, description)
    
    return _attach_screenshot 