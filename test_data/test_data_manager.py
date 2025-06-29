#!/usr/bin/env python3
"""
Test Data Manager - Quản lý test data cho 1000 test cases
"""

import json
import os
import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import logging

@dataclass
class UserData:
    """Data class cho user test data"""
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    phone: str
    role: str = "user"
    is_active: bool = True

@dataclass
class ProductData:
    """Data class cho product test data"""
    name: str
    price: float
    category: str
    description: str
    sku: str
    stock: int = 100

@dataclass
class OrderData:
    """Data class cho order test data"""
    order_id: str
    user_id: str
    products: List[Dict]
    total_amount: float
    status: str = "pending"
    created_at: str = ""

class TestDataManager:
    """Quản lý test data cho 1000 test cases"""
    
    def __init__(self, data_dir: str = "test_data"):
        self.data_dir = data_dir
        self.logger = logging.getLogger(__name__)
        self._ensure_data_dir()
        self._load_static_data()
    
    def _ensure_data_dir(self):
        """Đảm bảo thư mục test data tồn tại"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(f"{self.data_dir}/static", exist_ok=True)
        os.makedirs(f"{self.data_dir}/dynamic", exist_ok=True)
        os.makedirs(f"{self.data_dir}/templates", exist_ok=True)
    
    def _load_static_data(self):
        """Load static test data từ file"""
        self.static_data = {
            "users": self._load_json("static/users.json", []),
            "products": self._load_json("static/products.json", []),
            "orders": self._load_json("static/orders.json", []),
            "configs": self._load_json("static/configs.json", {})
        }
    
    def _load_json(self, filename: str, default_value: Any) -> Any:
        """Load JSON file với default value"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"Error loading {filename}: {e}")
        return default_value
    
    def _save_json(self, filename: str, data: Any):
        """Save data vào JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving {filename}: {e}")
    
    def get_user(self, user_type: str = "standard") -> UserData:
        """Lấy user data theo type"""
        if user_type == "standard":
            return UserData(
                username="standard_user",
                password="secret_sauce",
                email="standard@test.com",
                first_name="Standard",
                last_name="User",
                phone="0123456789"
            )
        elif user_type == "locked":
            return UserData(
                username="locked_out_user",
                password="secret_sauce",
                email="locked@test.com",
                first_name="Locked",
                last_name="User",
                phone="0123456788"
            )
        elif user_type == "problem":
            return UserData(
                username="problem_user",
                password="secret_sauce",
                email="problem@test.com",
                first_name="Problem",
                last_name="User",
                phone="0123456787"
            )
        else:
            # Generate random user
            return self._generate_random_user()
    
    def _generate_random_user(self) -> UserData:
        """Generate random user data"""
        username = f"testuser_{self._random_string(6)}"
        return UserData(
            username=username,
            password="Test@123",
            email=f"{username}@test.com",
            first_name=f"Test{self._random_string(4)}",
            last_name=f"User{self._random_string(4)}",
            phone=f"0{random.randint(100000000, 999999999)}"
        )
    
    def get_product(self, category: Optional[str] = None) -> ProductData:
        """Lấy product data"""
        if category:
            products = [p for p in self.static_data["products"] if p.get("category") == category]
            if products:
                product = random.choice(products)
                return ProductData(**product)
        
        # Return random product
        if self.static_data["products"]:
            product = random.choice(self.static_data["products"])
            return ProductData(**product)
        
        # Generate random product
        return self._generate_random_product()
    
    def _generate_random_product(self) -> ProductData:
        """Generate random product data"""
        categories = ["electronics", "clothing", "books", "food", "sports"]
        return ProductData(
            name=f"Product_{self._random_string(6)}",
            price=random.uniform(10.0, 1000.0),
            category=random.choice(categories),
            description=f"Test product description {self._random_string(10)}",
            sku=f"SKU_{self._random_string(8)}",
            stock=random.randint(0, 1000)
        )
    
    def get_order(self, user_id: Optional[str] = None, products: Optional[List[Dict]] = None) -> OrderData:
        """Lấy order data"""
        if user_id is None:
            user_id = f"user_{self._random_string(6)}"
        
        if products is None:
            products = [{"product_id": f"prod_{i}", "quantity": random.randint(1, 5)} 
                       for i in range(random.randint(1, 3))]
        
        total_amount = sum(p.get("price", 0) * p.get("quantity", 1) for p in products)
        
        return OrderData(
            order_id=f"ORD_{self._random_string(8)}",
            user_id=user_id,
            products=products,
            total_amount=total_amount,
            created_at=datetime.now().isoformat()
        )
    
    def _random_string(self, length: int) -> str:
        """Generate random string"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def create_test_suite_data(self, suite_name: str, test_count: int) -> Dict:
        """Tạo test data cho một test suite"""
        suite_data = {
            "suite_name": suite_name,
            "created_at": datetime.now().isoformat(),
            "users": [],
            "products": [],
            "orders": []
        }
        
        # Generate users
        for i in range(min(test_count // 10, 50)):  # Max 50 users
            suite_data["users"].append(asdict(self._generate_random_user()))
        
        # Generate products
        for i in range(min(test_count // 20, 100)):  # Max 100 products
            suite_data["products"].append(asdict(self._generate_random_product()))
        
        # Generate orders
        for i in range(min(test_count // 5, 200)):  # Max 200 orders
            suite_data["orders"].append(asdict(self.get_order()))
        
        # Save suite data
        filename = f"dynamic/suite_{suite_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self._save_json(filename, suite_data)
        
        return suite_data
    
    def get_data_for_test(self, test_name: str, data_type: str = "user") -> Any:
        """Lấy data cho một test cụ thể"""
        cache_key = f"{test_name}_{data_type}"
        
        # Check cache first
        cache_file = f"dynamic/cache_{cache_key}.json"
        cached_data = self._load_json(cache_file, None)
        
        if cached_data:
            return cached_data
        
        # Generate new data
        if data_type == "user":
            data = asdict(self._generate_random_user())
        elif data_type == "product":
            data = asdict(self._generate_random_product())
        elif data_type == "order":
            data = asdict(self.get_order())
        else:
            data = {}
        
        # Cache the data
        self._save_json(cache_file, data)
        return data
    
    def cleanup_test_data(self, older_than_days: int = 7):
        """Cleanup old test data"""
        cutoff_date = datetime.now() - timedelta(days=older_than_days)
        
        for filename in os.listdir(f"{self.data_dir}/dynamic"):
            if filename.startswith("cache_") or filename.startswith("suite_"):
                filepath = os.path.join(f"{self.data_dir}/dynamic", filename)
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                
                if file_time < cutoff_date:
                    try:
                        os.remove(filepath)
                        self.logger.info(f"Cleaned up old test data: {filename}")
                    except Exception as e:
                        self.logger.error(f"Error cleaning up {filename}: {e}")

# Global instance
test_data_manager = TestDataManager() 