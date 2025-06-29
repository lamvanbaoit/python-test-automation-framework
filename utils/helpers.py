# utils/helpers.py
from faker import Faker

# Khởi tạo Faker để tạo dữ liệu ngẫu nhiên
fake = Faker()

def get_test_user():
    """Hàm trả về user test mẫu (dùng cho test login UI/API)"""
    # SauceDemo test credentials - standard user
    return {"username": "standard_user", "password": "secret_sauce"}

def get_random_user():
    """Hàm trả về user ngẫu nhiên cho testing"""
    return {
        "username": fake.user_name(),
        "password": fake.password(),
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name()
    }

def get_test_users():
    """Hàm trả về danh sách các test users có sẵn cho SauceDemo"""
    return [
        {"username": "standard_user", "password": "secret_sauce"},
        {"username": "locked_out_user", "password": "secret_sauce"},
        {"username": "problem_user", "password": "secret_sauce"},
        {"username": "performance_glitch_user", "password": "secret_sauce"},
        {"username": "error_user", "password": "secret_sauce"},
        {"username": "visual_user", "password": "secret_sauce"}
    ] 