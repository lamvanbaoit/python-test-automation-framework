# tests/test_user_api.py

from utils.helpers import get_test_user

def test_user_login_api(api_client):
    user = get_test_user()
    response = api_client.login(user["username"], user["password"])
    assert response.status_code == 200
    assert "token" in response.json() 