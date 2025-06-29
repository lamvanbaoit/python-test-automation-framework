# utils/common_functions.py

import os
import json
import random
import string
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

# Lớp chứa các hàm tiện ích dùng chung cho test automation
class CommonFunctions:
    """Các hàm tiện ích dùng chung cho test automation"""
    
    @staticmethod
    def generate_random_string(length: int = 8) -> str:
        """Tạo chuỗi ngẫu nhiên gồm chữ và số"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_random_email() -> str:
        """Tạo email ngẫu nhiên"""
        username = CommonFunctions.generate_random_string(8)
        domain = random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'test.com'])
        return f"{username}@{domain}"
    
    @staticmethod
    def generate_random_phone() -> str:
        """Tạo số điện thoại ngẫu nhiên"""
        return f"0{random.randint(100000000, 999999999)}"
    
    @staticmethod
    def generate_test_data(data_type: str, **kwargs) -> Dict[str, Any]:
        """Tạo dữ liệu test mẫu theo loại (user, order, product, ...)"""
        if data_type == "user":
            return {
                "username": f"testuser_{CommonFunctions.generate_random_string(4)}",
                "email": CommonFunctions.generate_random_email(),
                "password": "Test@123",
                "phone": CommonFunctions.generate_random_phone()
            }
        elif data_type == "order":
            return {
                "order_id": f"ORD_{CommonFunctions.generate_random_string(6)}",
                "amount": random.randint(1000, 100000),
                "currency": "VND",
                "status": random.choice(["pending", "completed", "cancelled"])
            }
        elif data_type == "product":
            return {
                "name": f"Product_{CommonFunctions.generate_random_string(5)}",
                "price": random.randint(10000, 500000),
                "category": random.choice(["electronics", "clothing", "books", "food"])
            }
        else:
            return {}
    
    @staticmethod
    def save_screenshot_with_metadata(page, name: str = "", metadata: Optional[Dict] = None) -> str:
        """Chụp screenshot và lưu kèm metadata (nếu có)"""
        if not name:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name = f"screenshot_{timestamp}.png"
        
        path = os.path.join("screenshots", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Chụp screenshot
        page.screenshot(path=path, full_page=True)
        
        # Lưu metadata nếu có
        if metadata:
            metadata_path = path.replace('.png', '_metadata.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Screenshot saved: {path}")
        return path
    
    @staticmethod
    def wait_for_page_load(page, timeout: int = 10000) -> bool:
        """Chờ trang load xong (networkidle)"""
        try:
            page.wait_for_load_state("networkidle", timeout=timeout)
            return True
        except Exception as e:
            logging.warning(f"Page load timeout: {e}")
            return False
    
    @staticmethod
    def retry_action(action_func, max_retries: int = 3, delay: float = 1.0):
        """Thực hiện một action với số lần thử lại (retry) nếu gặp lỗi"""
        for attempt in range(max_retries):
            try:
                return action_func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                logging.warning(f"Action failed (attempt {attempt + 1}): {e}")
                import time
                time.sleep(delay)
    
    @staticmethod
    def validate_response(response, expected_status: int = 200, expected_fields: Optional[List[str]] = None):
        """Kiểm tra response trả về từ API (status code, các trường bắt buộc)"""
        assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}"
        
        if expected_fields:
            response_data = response.json()
            for field in expected_fields:
                assert field in response_data, f"Field '{field}' not found in response"
    
    @staticmethod
    def create_test_user_data(count: int = 1) -> List[Dict]:
        """Tạo danh sách user test data mẫu"""
        users = []
        for i in range(count):
            user = CommonFunctions.generate_test_data("user")
            user["id"] = i + 1
            users.append(user)
        return users
    
    @staticmethod
    def log_test_info(test_name: str, data: Optional[Dict] = None):
        """Ghi log thông tin test (tên, dữ liệu, ...)"""
        logging.info(f"=== Test: {test_name} ===")
        if data:
            for key, value in data.items():
                logging.info(f"  {key}: {value}")
        logging.info("=" * 50)
    
    @staticmethod
    def get_file_path(relative_path: str) -> str:
        """Lấy đường dẫn tuyệt đối của file từ đường dẫn tương đối"""
        return os.path.abspath(relative_path)
    
    @staticmethod
    def ensure_directory_exists(directory: str):
        """Đảm bảo thư mục tồn tại, nếu chưa có thì tạo mới"""
        os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def read_json_file(file_path: str) -> Dict:
        """Đọc file JSON và trả về dict, nếu lỗi trả về dict rỗng"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error reading JSON file {file_path}: {e}")
            return {}
    
    @staticmethod
    def write_json_file(file_path: str, data: Dict):
        """Ghi dict vào file JSON"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logging.info(f"Data written to {file_path}")
        except Exception as e:
            logging.error(f"Error writing JSON file {file_path}: {e}")

# Các hàm tiện ích nhanh cho test

def get_random_user() -> Dict[str, str]:
    """Lấy user ngẫu nhiên (tương thích với code cũ)"""
    return CommonFunctions.generate_test_data("user")

def get_test_users(count: int = 5) -> List[Dict[str, str]]:
    """Lấy danh sách user test mẫu"""
    return CommonFunctions.create_test_user_data(count)

def take_screenshot_with_info(page, test_name: str, info: str = ""):
    """Chụp screenshot kèm thông tin test (tên, timestamp, mô tả)"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name = f"{test_name}_{timestamp}.png"
    metadata = {
        "test_name": test_name,
        "timestamp": timestamp,
        "info": info
    }
    return CommonFunctions.save_screenshot_with_metadata(page, name, metadata) 