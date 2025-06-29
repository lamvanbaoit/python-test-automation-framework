# tests/test_user_api.py

from utils.helpers import get_test_user

# Test kiểm thử API đăng nhập user

def test_user_login_api(api_client):
    user = get_test_user()  # Lấy user test
    response = api_client.login(user["username"], user["password"])
    # Kiểm tra status code trả về là 200 (thành công)
    assert response.status_code == 200
    # Kiểm tra response có chứa token
    assert "token" in response.json() 