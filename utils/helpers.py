# utils/helpers.py

def get_test_user():
    """Hàm trả về user test mẫu (dùng cho test login UI/API)"""
    # Sử dụng credentials đúng cho saucedemo.com
    return {"username": "standard_user", "password": "secret_sauce"} 