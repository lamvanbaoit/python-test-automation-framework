# api_clients/user_api_client.py

import requests
from config.settings import API_BASE_URL

# Client cho các API liên quan đến user (REST API)
class UserApiClient:
    def __init__(self, base_url=API_BASE_URL):
        # Khởi tạo với base_url của API
        self.base_url = base_url

    def get_user(self, user_id):
        # Gọi API lấy thông tin user theo user_id
        response = requests.get(f"{self.base_url}/users/{user_id}")
        return response

    def login(self, username, password):
        # Gọi API đăng nhập với username và password
        response = requests.post(f"{self.base_url}/login", json={"username": username, "password": password})
        return response 