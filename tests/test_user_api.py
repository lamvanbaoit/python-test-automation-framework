# tests/test_user_api.py

import pytest
from api_clients.user_api_client import UserApiClient
from utils.helpers import get_test_user

@pytest.mark.api
@pytest.mark.smoke
def test_user_login_api():
    """Test API đăng nhập user"""
    api_client = UserApiClient()
    user = get_test_user()  # Lấy user test
    
    # Test login API
    response = api_client.login(user["username"], user["password"])
    
    # Kiểm tra response
    assert response.status_code == 200
    assert "token" in response.json()
    assert response.json()["success"] == True 