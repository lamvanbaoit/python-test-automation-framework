# api_clients/user_api_client.py

import requests
from config.settings import API_BASE_URL

class UserApiClient:
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url

    def get_user(self, user_id):
        response = requests.get(f"{self.base_url}/users/{user_id}")
        return response

    def login(self, username, password):
        response = requests.post(f"{self.base_url}/login", json={"username": username, "password": password})
        return response 