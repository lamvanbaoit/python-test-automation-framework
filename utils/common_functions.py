# utils/common_functions.py

import os
import json
import random
import string
import logging
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from functools import lru_cache, wraps

# Lớp chứa các hàm tiện ích dùng chung cho test automation
class CommonFunctions:
    """Các hàm tiện ích dùng chung cho test automation với performance optimization"""
    
    # Cache cho test data
    _test_data_cache = {}
    _cache_expiry = {}
    _cache_ttl = 3600  # 1 hour default TTL
    
    @staticmethod
    def cache_result(ttl_seconds: int = 3600):
        """Decorator để cache kết quả của function"""
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key
                cache_key = f"{func.__name__}_{hash(str(args) + str(sorted(kwargs.items())))}"
                
                # Check if cached result exists and is still valid
                if cache_key in CommonFunctions._test_data_cache:
                    if time.time() < CommonFunctions._cache_expiry.get(cache_key, 0):
                        logging.debug(f"Cache hit for {func.__name__}")
                        return CommonFunctions._test_data_cache[cache_key]
                    else:
                        # Remove expired cache
                        del CommonFunctions._test_data_cache[cache_key]
                        del CommonFunctions._cache_expiry[cache_key]
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                CommonFunctions._test_data_cache[cache_key] = result
                CommonFunctions._cache_expiry[cache_key] = time.time() + ttl_seconds
                
                logging.debug(f"Cached result for {func.__name__}")
                return result
            return wrapper
        return decorator
    
    @staticmethod
    def clear_cache():
        """Clear tất cả cached data"""
        CommonFunctions._test_data_cache.clear()
        CommonFunctions._cache_expiry.clear()
        logging.info("Cache cleared")
    
    @staticmethod
    def get_cache_stats() -> Dict[str, Any]:
        """Lấy thống kê cache"""
        current_time = time.time()
        valid_entries = sum(1 for expiry in CommonFunctions._cache_expiry.values() if current_time < expiry)
        expired_entries = len(CommonFunctions._cache_expiry) - valid_entries
        
        return {
            "total_entries": len(CommonFunctions._test_data_cache),
            "valid_entries": valid_entries,
            "expired_entries": expired_entries,
            "cache_size": len(CommonFunctions._test_data_cache)
        }
    
    @staticmethod
    @cache_result(ttl_seconds=1800)  # Cache for 30 minutes
    def generate_random_string(length: int = 8) -> str:
        """Tạo chuỗi ngẫu nhiên gồm chữ và số với caching"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    @cache_result(ttl_seconds=1800)
    def generate_random_email() -> str:
        """Tạo email ngẫu nhiên với caching"""
        username = CommonFunctions.generate_random_string(8)
        domain = random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'test.com'])
        return f"{username}@{domain}"
    
    @staticmethod
    @cache_result(ttl_seconds=1800)
    def generate_random_phone() -> str:
        """Tạo số điện thoại ngẫu nhiên với caching"""
        return f"0{random.randint(100000000, 999999999)}"
    
    @staticmethod
    @cache_result(ttl_seconds=900)  # Cache for 15 minutes
    def generate_test_data(data_type: str, **kwargs) -> Dict[str, Any]:
        """Tạo dữ liệu test mẫu theo loại với enhanced caching"""
        if data_type == "user":
            return {
                "username": f"testuser_{CommonFunctions.generate_random_string(4)}",
                "email": CommonFunctions.generate_random_email(),
                "password": "Test@123",
                "phone": CommonFunctions.generate_random_phone(),
                "first_name": f"Test{CommonFunctions.generate_random_string(4)}",
                "last_name": f"User{CommonFunctions.generate_random_string(4)}",
                "created_at": datetime.now().isoformat()
            }
        elif data_type == "order":
            return {
                "order_id": f"ORD_{CommonFunctions.generate_random_string(6)}",
                "amount": random.randint(1000, 100000),
                "currency": "VND",
                "status": random.choice(["pending", "completed", "cancelled"]),
                "created_at": datetime.now().isoformat(),
                "items": [
                    {
                        "product_id": f"PROD_{CommonFunctions.generate_random_string(4)}",
                        "quantity": random.randint(1, 5),
                        "price": random.randint(10000, 50000)
                    }
                    for _ in range(random.randint(1, 3))
                ]
            }
        elif data_type == "product":
            return {
                "name": f"Product_{CommonFunctions.generate_random_string(5)}",
                "price": random.randint(10000, 500000),
                "category": random.choice(["electronics", "clothing", "books", "food", "sports"]),
                "sku": f"SKU_{CommonFunctions.generate_random_string(8)}",
                "stock": random.randint(0, 1000),
                "description": f"Test product description {CommonFunctions.generate_random_string(10)}"
            }
        else:
            return {}
    
    @staticmethod
    def save_screenshot_with_metadata(page, name: str = "", metadata: Optional[Dict] = None, optimize: bool = True) -> str:
        """Chụp screenshot và lưu kèm metadata với optimization"""
        if not name:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name = f"screenshot_{timestamp}.png"
        
        path = os.path.join("screenshots", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Optimize screenshot for mass testing
        if optimize:
            # Take smaller screenshots for better performance
            page.screenshot(path=path, full_page=False)
        else:
            page.screenshot(path=path, full_page=True)
        
        # Lưu metadata nếu có
        if metadata:
            metadata_path = path.replace('.png', '_metadata.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Screenshot saved: {path}")
        return path
    
    @staticmethod
    def wait_for_page_load(page, timeout: int = 10000, strategy: str = "networkidle") -> bool:
        """Chờ trang load xong với multiple strategies"""
        try:
            if strategy == "networkidle":
                page.wait_for_load_state("networkidle", timeout=timeout)
            elif strategy == "domcontentloaded":
                page.wait_for_load_state("domcontentloaded", timeout=timeout)
            elif strategy == "load":
                page.wait_for_load_state("load", timeout=timeout)
            else:
                page.wait_for_load_state("networkidle", timeout=timeout)
            return True
        except Exception as e:
            logging.warning(f"Page load timeout ({strategy}): {e}")
            return False
    
    @staticmethod
    def retry_action(action_func: Callable, max_retries: int = 3, delay: float = 1.0, backoff_factor: float = 2.0):
        """Thực hiện một action với enhanced retry mechanism"""
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                return action_func()
            except Exception as e:
                last_exception = e
                if attempt < max_retries - 1:
                    sleep_time = delay * (backoff_factor ** attempt)
                    logging.warning(f"Action failed (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {sleep_time:.2f}s")
                    time.sleep(sleep_time)
                else:
                    logging.error(f"Action failed after {max_retries} attempts: {e}")
        
        if last_exception:
            raise last_exception
        else:
            raise Exception("Action failed with unknown error")
    
    @staticmethod
    def validate_response(response, expected_status: int = 200, expected_fields: Optional[List[str]] = None, 
                         validate_schema: bool = False, schema: Optional[Dict] = None):
        """Kiểm tra response trả về từ API với enhanced validation"""
        # Validate status code
        assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}"
        
        # Validate response format
        try:
            response_data = response.json()
        except Exception as e:
            raise AssertionError(f"Response is not valid JSON: {e}")
        
        # Validate required fields
        if expected_fields:
            for field in expected_fields:
                assert field in response_data, f"Field '{field}' not found in response"
        
        # Validate schema if provided
        if validate_schema and schema:
            # Simple schema validation - in production, use jsonschema library
            for key, expected_type in schema.items():
                if key in response_data:
                    assert isinstance(response_data[key], expected_type), \
                        f"Field '{key}' should be {expected_type.__name__}, got {type(response_data[key]).__name__}"
    
    @staticmethod
    @cache_result(ttl_seconds=1800)
    def create_test_user_data(count: int = 1) -> List[Dict]:
        """Tạo danh sách user test data mẫu với caching"""
        users = []
        for i in range(count):
            user = CommonFunctions.generate_test_data("user")
            user["id"] = i + 1
            users.append(user)
        return users
    
    @staticmethod
    def log_test_info(test_name: str, data: Optional[Dict] = None, level: str = "INFO"):
        """Ghi log thông tin test với multiple levels"""
        log_message = f"=== Test: {test_name} ==="
        
        if data:
            for key, value in data.items():
                log_message += f"\n  {key}: {value}"
        
        log_message += "\n" + "=" * 50
        
        if level.upper() == "DEBUG":
            logging.debug(log_message)
        elif level.upper() == "WARNING":
            logging.warning(log_message)
        elif level.upper() == "ERROR":
            logging.error(log_message)
        else:
            logging.info(log_message)
    
    @staticmethod
    def get_file_path(relative_path: str) -> str:
        """Lấy đường dẫn tuyệt đối của file từ đường dẫn tương đối"""
        return os.path.abspath(relative_path)
    
    @staticmethod
    def ensure_directory_exists(directory: str):
        """Đảm bảo thư mục tồn tại, nếu chưa có thì tạo mới"""
        os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    @cache_result(ttl_seconds=300)  # Cache for 5 minutes
    def read_json_file(file_path: str) -> Dict:
        """Đọc file JSON và trả về dict với caching"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error reading JSON file {file_path}: {e}")
            return {}
    
    @staticmethod
    def write_json_file(file_path: str, data: Dict, pretty: bool = True):
        """Ghi dict vào file JSON với optimization"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(data, f, ensure_ascii=False)
            logging.info(f"Data written to {file_path}")
        except Exception as e:
            logging.error(f"Error writing JSON file {file_path}: {e}")
    
    @staticmethod
    def generate_test_suite_data(suite_name: str, test_count: int) -> Dict[str, Any]:
        """Generate comprehensive test suite data"""
        return {
            "suite_name": suite_name,
            "test_count": test_count,
            "created_at": datetime.now().isoformat(),
            "users": CommonFunctions.create_test_user_data(min(test_count // 10, 50)),
            "products": [CommonFunctions.generate_test_data("product") for _ in range(min(test_count // 20, 100))],
            "orders": [CommonFunctions.generate_test_data("order") for _ in range(min(test_count // 5, 200))],
            "metadata": {
                "framework": "Playwright + Pytest",
                "version": "1.0.0",
                "generator": "CommonFunctions"
            }
        }
    
    @staticmethod
    def cleanup_old_files(directory: str, older_than_days: int = 7):
        """Cleanup old files trong directory"""
        cutoff_time = datetime.now() - timedelta(days=older_than_days)
        cleaned_count = 0
        
        try:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                    if file_time < cutoff_time:
                        os.remove(filepath)
                        cleaned_count += 1
                        logging.info(f"Cleaned up old file: {filename}")
        except Exception as e:
            logging.error(f"Error cleaning up directory {directory}: {e}")
        
        return cleaned_count

# Các hàm tiện ích nhanh cho test với caching

@lru_cache(maxsize=128)
def get_random_user() -> Dict[str, str]:
    """Lấy user ngẫu nhiên với LRU cache"""
    return CommonFunctions.generate_test_data("user")

@lru_cache(maxsize=64)
def get_test_users(count: int = 5) -> List[Dict[str, str]]:
    """Lấy danh sách user test mẫu với LRU cache"""
    return CommonFunctions.create_test_user_data(count)

def take_screenshot_with_info(page, test_name: str, info: str = "", optimize: bool = True):
    """Chụp screenshot kèm thông tin test với optimization"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name = f"{test_name}_{timestamp}.png"
    metadata = {
        "test_name": test_name,
        "timestamp": timestamp,
        "info": info,
        "optimized": optimize
    }
    return CommonFunctions.save_screenshot_with_metadata(page, name, metadata, optimize) 