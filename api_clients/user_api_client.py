# api_clients/user_api_client.py

import requests
import json
from typing import Dict, Any

# Client cho các API liên quan đến user (REST API)
class UserApiClient:
    """API Client cho user operations"""
    
    def __init__(self, base_url: str = "https://httpbin.org"):
        # Sử dụng httpbin.org thay vì api.example.com để test
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'python-requests/2.32.4'
        })
    
    def login(self, username: str, password: str) -> requests.Response:
        """Login user với username và password"""
        # Sử dụng httpbin.org để test POST request
        payload = {"username": username, "password": password}
        response = self.session.post(f"{self.base_url}/post", json=payload)
        return response
    
    def get_user_info(self, user_id: int) -> requests.Response:
        """Lấy thông tin user theo ID"""
        response = self.session.get(f"{self.base_url}/get?user_id={user_id}")
        return response
    
    def create_user(self, user_data: Dict[str, Any]) -> requests.Response:
        """Tạo user mới"""
        response = self.session.post(f"{self.base_url}/post", json=user_data)
        return response
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> requests.Response:
        """Cập nhật thông tin user"""
        user_data['user_id'] = user_id
        response = self.session.put(f"{self.base_url}/put", json=user_data)
        return response
    
    def delete_user(self, user_id: int) -> requests.Response:
        """Xóa user"""
        response = self.session.delete(f"{self.base_url}/delete?user_id={user_id}")
        return response 