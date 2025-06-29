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

# Import performance optimization modules
try:
    from utils.performance_optimizer import performance_optimizer
    from test_data.test_data_manager import test_data_manager
    from utils.test_suite_manager import test_suite_manager
except ImportError:
    # Fallback if modules not available
    performance_optimizer = None
    test_data_manager = None
    test_suite_manager = None

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
        default=None,
        help="Run browser in headless mode"
    )
    # Thêm options cho mass testing
    parser.addoption(
        "--mass-test",
        action="store_true",
        default=False,
        help="Enable mass testing optimizations for 1000+ test cases"
    )
    parser.addoption(
        "--optimize-performance",
        action="store_true",
        default=False,
        help="Enable performance optimizations"
    )
    parser.addoption(
        "--test-suite",
        action="store",
        default=None,
        help="Test suite name for mass testing"
    )
    # Thêm option để disable Allure nếu có lỗi
    parser.addoption(
        "--no-allure",
        action="store_true",
        default=False,
        help="Disable Allure reporting to avoid plugin errors"
    )

# =====================
# Cấu hình browser và context cho Playwright
# =====================
@pytest.fixture(scope="session")
def browser_type_launch_args(request):
    """Cấu hình các tham số khi khởi tạo browser"""
    browser = request.config.getoption("--test-browser")
    headless_option = request.config.getoption("--headless")
    mass_test = request.config.getoption("--mass-test")
    
    # Tự động detect CI environment và set headless=True
    # Kiểm tra các biến môi trường CI phổ biến
    ci_environment = any([
        os.getenv('CI') == 'true',
        os.getenv('GITHUB_ACTIONS') == 'true',
        os.getenv('TRAVIS') == 'true',
        os.getenv('CIRCLECI') == 'true',
        os.getenv('JENKINS_URL') is not None,
        os.getenv('BUILD_ID') is not None,
        os.getenv('DISPLAY') is None and os.name != 'nt'  # Linux/Unix không có DISPLAY
    ])
    
    # Nếu không có option --headless được chỉ định, tự động detect
    if headless_option is None:
        headless = ci_environment or mass_test  # Force headless for mass testing
        print(f"🔍 Auto-detect headless mode: {headless} (CI: {ci_environment}, Mass Test: {mass_test})")
    else:
        headless = headless_option
        print(f"🎯 Manual headless mode: {headless}")
    
    if browser == "chromium":
        args = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-web-security",
            "--disable-features=VizDisplayCompositor"
        ]
        
        # Add mass testing optimizations
        if mass_test:
            args.extend([
                "--disable-images",  # Disable images for faster loading
                "--disable-javascript",  # Disable JS if not needed
                "--disable-plugins",
                "--disable-extensions",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--disable-field-trial-config",
                "--disable-ipc-flooding-protection"
            ])
        
        return {
            "headless": headless,
            "args": args
        }
    elif browser == "firefox":
        args = [
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
        
        if mass_test:
            args.extend([
                "--disable-images",
                "--disable-javascript"
            ])
        
        return {
            "headless": headless,
            "args": args
        }
    elif browser == "webkit":
        args = [
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
        
        if mass_test:
            args.extend([
                "--disable-images",
                "--disable-javascript"
            ])
        
        return {
            "headless": headless,
            "args": args
        }
    else:
        return {"headless": headless}

@pytest.fixture(scope="session")
def browser_context_args(request):
    """Cấu hình context cho browser (viewport, video, ...)."""
    mass_test = request.config.getoption("--mass-test")
    
    context_args = {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "record_video_dir": "videos/",
        "record_video_size": {"width": 1920, "height": 1080}
    }
    
    # Optimize for mass testing
    if mass_test:
        context_args.update({
            "record_video_dir": None,  # Disable video recording for mass tests
            "record_har_path": None,   # Disable HAR recording
            "record_har_omit_content": True,
            "extra_http_headers": {
                "User-Agent": "Playwright Mass Test Runner"
            }
        })
    
    return context_args

# =====================
# Fixtures cho browser và page
# =====================
@pytest.fixture(scope="session")
def base_url(request):
    """Base URL cho ứng dụng test"""
    return request.config.getoption("--app-base-url")

@pytest.fixture(scope="session")
def browser(browser_type_launch_args):
    """Fixture tạo browser instance cho toàn bộ session test"""
    with sync_playwright() as p:
        browser_type = getattr(p, "chromium")  # Default to chromium
        browser = browser_type.launch(**browser_type_launch_args)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser, base_url, request):
    """Fixture tạo page instance cho mỗi test function"""
    context = browser.new_context(**request.getfixturevalue("browser_context_args"))
    page = context.new_page()
    page.set_default_timeout(30000)  # 30 seconds timeout
    page.set_default_navigation_timeout(30000)
    
    # Log test start
    test_name = request.node.name
    print(f"🧪 Running test: {test_name}")
    
    yield page
    
    # Cleanup
    try:
        page.close()
    except Exception as e:
        print(f"Warning: Error closing page: {e}")

# =====================
# Performance monitoring fixtures
# =====================
@pytest.fixture(scope="session")
def performance_monitor(request):
    """Fixture để monitor performance trong quá trình test"""
    if performance_optimizer:
        return performance_optimizer
    return None

@pytest.fixture(scope="function")
def test_data_optimized(request):
    """Fixture cung cấp test data được optimize cho mass testing"""
    mass_test = request.config.getoption("--mass-test")
    test_suite = request.config.getoption("--test-suite")
    
    if mass_test and test_data_manager and test_suite:
        return test_data_manager.get_test_data(test_suite)
    return None

# =====================
# Base test class với các helper methods
# =====================
class BaseTest:
    def login_quick(self, page, username, password):
        # Hàm login nhanh cho các test kế thừa
        page.goto("https://www.saucedemo.com/")
        page.fill("#user-name", username)
        page.fill("#password", password)
        page.click("#login-button")
        page.wait_for_load_state("networkidle")

# =====================
# API và gRPC client fixtures
# =====================
@pytest.fixture(scope="function")
def api_client():
    """Fixture tạo API client cho test"""
    return UserApiClient()

@pytest.fixture(scope="function")
def grpc_client():
    """Fixture tạo gRPC client cho test"""
    return OrderGrpcClient()

@pytest.fixture(scope="function")
def test_data():
    """Fixture cung cấp test data cho các test"""
    from utils.helpers import get_test_user, get_random_user
    return {
        "valid_user": get_test_user(),
        "random_user": get_random_user()
    }

# =====================
# Allure configuration fixtures (chỉ chạy khi không có --no-allure)
# =====================
@pytest.fixture(scope="function")
def allure_environment(request):
    """Fixture cung cấp thông tin môi trường cho Allure"""
    if request.config.getoption("--no-allure"):
        return None
    
    return {
        "browser": request.config.getoption("--test-browser"),
        "base_url": request.config.getoption("--app-base-url"),
        "environment": "test",
        "timestamp": datetime.now().isoformat()
    }

@pytest.fixture(autouse=True)
def setup_allure_metadata(request, allure_environment):
    """Tự động setup Allure metadata cho mỗi test"""
    if request.config.getoption("--no-allure") or not allure_environment:
        return
    
    # Add environment info
    if allure_environment:
        allure.dynamic.description(f"""
        **Environment:**
        - Browser: {allure_environment['browser']}
        - Base URL: {allure_environment['base_url']}
        - Environment: {allure_environment['environment']}
        - Timestamp: {allure_environment['timestamp']}
        """)

# =====================
# Screenshot và logging fixtures
# =====================
@pytest.fixture(scope="function")
def screenshot_on_failure(page, request):
    """Fixture tự động chụp screenshot khi test fail"""
    yield
    
    # Chụp screenshot nếu test fail
    if request.node.rep_call.failed:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = f"screenshots/failure_{request.node.name}_{timestamp}.png"
        
        # Đảm bảo thư mục tồn tại
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        
        try:
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot saved: {screenshot_path}")
            
            # Attach to Allure nếu có
            if not request.config.getoption("--no-allure"):
                with open(screenshot_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        f"Failure Screenshot - {request.node.name}",
                        allure.attachment_type.PNG
                    )
        except Exception as e:
            print(f"Warning: Could not take screenshot: {e}")

# =====================
# Pytest hooks
# =====================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook để capture test result cho screenshot"""
    outcome = yield
    rep = outcome.get_result()
    item.rep_call = rep

# =====================
# Allure directory fixtures
# =====================
@pytest.fixture(scope="session")
def allure_results_dir():
    """Fixture trả về đường dẫn thư mục allure-results"""
    return "allure-results"

@pytest.fixture(scope="session")
def allure_report_dir():
    """Fixture trả về đường dẫn thư mục allure-report"""
    return "allure-report"

# =====================
# Pytest configuration
# =====================
def pytest_configure(config):
    """Cấu hình pytest khi khởi động"""
    # Tạo thư mục cần thiết
    os.makedirs("allure-results", exist_ok=True)
    os.makedirs("allure-report", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("videos", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Cấu hình Allure nếu không bị disable
    if not config.getoption("--no-allure"):
        # Add Allure metadata
        allure.dynamic.description_html("""
        <h3>Test Automation Framework</h3>
        <p>This test is part of the comprehensive test automation framework using Playwright, Pytest, and Allure.</p>
        """)
        
        # Add custom labels
        allure.dynamic.label("feature", "Test Automation Framework")
        allure.dynamic.label("story", "Automated Testing")
        allure.dynamic.label("framework", "pytest")
        allure.dynamic.label("language", "python")
    
    # Cấu hình performance monitoring nếu có
    if config.getoption("--optimize-performance") and performance_optimizer:
        performance_optimizer.start_monitoring()

def pytest_unconfigure(config):
    """Cleanup khi pytest kết thúc"""
    # Stop performance monitoring nếu có
    if config.getoption("--optimize-performance") and performance_optimizer:
        performance_optimizer.stop_monitoring()

# =====================
# Allure helper fixtures
# =====================
@pytest.fixture(scope="function")
def allure_step_logger():
    """Fixture để log Allure steps"""
    def log_step(step_name, step_data=None):
        if step_data:
            allure.attach(
                str(step_data),
                step_name,
                allure.attachment_type.TEXT
            )
        return step_data
    return log_step

@pytest.fixture(scope="function")
def allure_attach_screenshot(page):
    """Fixture để attach screenshot vào Allure"""
    def _attach_screenshot(description="Screenshot"):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = f"screenshots/allure_{timestamp}.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        page.screenshot(path=screenshot_path, full_page=True)
        
        with open(screenshot_path, "rb") as f:
            allure.attach(
                f.read(),
                f"{description} - {timestamp}",
                allure.attachment_type.PNG
            )
        return screenshot_path
    return _attach_screenshot