# tests/test_user_api.py

import pytest
from api_clients.user_api_client import UserApiClient
from utils.helpers import get_test_user

@pytest.mark.api
@pytest.mark.smoke
def test_user_login_api():
    """Test API login user"""
    api_client = UserApiClient()
    user = get_test_user()
    response = api_client.login(user["username"], user["password"])
    
    # Kiểm tra response status
    assert response.status_code == 200
    
    # Kiểm tra response có chứa data được gửi
    response_data = response.json()
    assert "data" in response_data
    assert "json" in response_data
    
    # Kiểm tra username và password được gửi đúng
    sent_data = response_data["json"]
    assert sent_data["username"] == user["username"]
    assert sent_data["password"] == user["password"] 