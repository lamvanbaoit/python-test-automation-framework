# utils/allure_helpers.py

import allure
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Lớp hỗ trợ tạo Allure report với các step chi tiết, giúp ghi lại từng hành động, dữ liệu, trạng thái trong quá trình test
class AllureReporter:
    """Helper class để tạo Allure report với step-by-step chi tiết"""
    
    @staticmethod
    def navigate_to(url: str):
        """Step: Điều hướng tới một URL cụ thể"""
        allure.attach(
            f"Navigating to: {url}",
            "Navigation Step",
            allure.attachment_type.TEXT
        )
        return url
    
    @staticmethod
    def login_step(username: str, password: str = "***"):
        """Step: Thực hiện login với username và password"""
        allure.attach(
            f"Username: {username}\nPassword: {password}",
            "Login Credentials",
            allure.attachment_type.TEXT
        )
        return {"username": username, "password": password}
    
    @staticmethod
    def fill_field_step(field_name: str, value: str):
        """Step: Điền dữ liệu vào một trường trên form"""
        allure.attach(
            f"Field: {field_name}\nValue: {value}",
            "Field Input",
            allure.attachment_type.TEXT
        )
        return {"field": field_name, "value": value}
    
    @staticmethod
    def click_element_step(element_name: str, selector: str = ""):
        """Step: Click vào một phần tử trên trang"""
        allure.attach(
            f"Element: {element_name}\nSelector: {selector}",
            "Click Action",
            allure.attachment_type.TEXT
        )
        return {"element": element_name, "selector": selector}
    
    @staticmethod
    def validate_element_step(element_name: str, expected_state: str):
        """Step: Kiểm tra trạng thái của một phần tử (hiển thị, enable, ... )"""
        allure.attach(
            f"Element: {element_name}\nExpected: {expected_state}",
            "Validation",
            allure.attachment_type.TEXT
        )
        return {"element": element_name, "expected": expected_state}
    
    @staticmethod
    def take_screenshot_step(page, description: str = "Screenshot"):
        """Step: Chụp màn hình và attach vào Allure report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = f"screenshots/allure_{timestamp}.png"
        # Đảm bảo thư mục tồn tại
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        # Chụp screenshot
        page.screenshot(path=screenshot_path, full_page=True)
        # Attach vào Allure
        with open(screenshot_path, "rb") as f:
            allure.attach(
                f.read(),
                f"{description} - {timestamp}",
                allure.attachment_type.PNG
            )
        return screenshot_path
    
    @staticmethod
    def api_request_step(method: str, endpoint: str, data: Optional[Dict] = None):
        """Step: Ghi lại thông tin request API"""
        request_info = {
            "method": method,
            "endpoint": endpoint,
            "data": data
        }
        allure.attach(
            json.dumps(request_info, indent=2),
            "API Request",
            allure.attachment_type.JSON
        )
        return request_info
    
    @staticmethod
    def api_response_step(status_code: int, response_data: Optional[Dict] = None):
        """Step: Ghi lại thông tin response API"""
        response_info = {
            "status_code": status_code,
            "data": response_data
        }
        allure.attach(
            json.dumps(response_info, indent=2),
            "API Response",
            allure.attachment_type.JSON
        )
        return response_info
    
    @staticmethod
    def wait_for_element_step(element_name: str, timeout: int = 5000):
        """Step: Chờ đợi một phần tử xuất hiện trên trang"""
        allure.attach(
            f"Element: {element_name}\nTimeout: {timeout}ms",
            "Wait Action",
            allure.attachment_type.TEXT
        )
        return {"element": element_name, "timeout": timeout}
    
    @staticmethod
    def assert_step(condition: str, expected: Any, actual: Any):
        """Step: Ghi lại thông tin so sánh/kiểm tra (assert)"""
        assertion_info = {
            "condition": condition,
            "expected": expected,
            "actual": actual
        }
        allure.attach(
            json.dumps(assertion_info, indent=2),
            "Assertion",
            allure.attachment_type.JSON
        )
        return assertion_info
    
    @staticmethod
    def test_data_step(data_type: str, data: Dict):
        """Step: Ghi lại dữ liệu test sử dụng trong testcase"""
        allure.attach(
            json.dumps(data, indent=2),
            f"Test Data - {data_type}",
            allure.attachment_type.JSON
        )
        return data
    
    @staticmethod
    def environment_step(browser: str, base_url: str, environment: str = "dev"):
        """Step: Ghi lại thông tin môi trường test"""
        env_info = {
            "browser": browser,
            "base_url": base_url,
            "environment": environment,
            "timestamp": datetime.now().isoformat()
        }
        allure.attach(
            json.dumps(env_info, indent=2),
            "Environment",
            allure.attachment_type.JSON
        )
        return env_info
    
    @staticmethod
    def add_description(description: str):
        """Thêm mô tả cho test case"""
        allure.description(description)
    
    @staticmethod
    def add_severity(severity: str):
        """Thêm mức độ nghiêm trọng cho test case"""
        allure.severity(severity)
    
    @staticmethod
    def add_feature(feature: str):
        """Thêm feature cho test case"""
        allure.feature(feature)
    
    @staticmethod
    def add_story(story: str):
        """Thêm story cho test case"""
        allure.story(story)
    
    @staticmethod
    def add_issue(issue_id: str):
        """Thêm issue link cho test case"""
        allure.issue(issue_id)
    
    @staticmethod
    def add_test_case(test_case_id: str):
        """Thêm test case ID cho test case"""
        allure.testcase(test_case_id)

# Decorators tiện ích cho Allure

def allure_step(step_name: str):
    """Decorator để tạo step với tên tùy chỉnh cho function"""
    def decorator(func):
        @allure.step(step_name)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def allure_attach_screenshot(page, description: str = "Screenshot"):
    """Decorator để tự động attach screenshot vào Allure report khi chạy function"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                AllureReporter.take_screenshot_step(page, description)
                return result
            except Exception as e:
                AllureReporter.take_screenshot_step(page, f"Error - {description}")
                raise e
        return wrapper
    return decorator 