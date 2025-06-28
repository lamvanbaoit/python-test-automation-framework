# 🚀 Quick Start Guide - Python Test Automation Framework

## ⚡ Chạy nhanh trong 5 phút

### 1. Setup môi trường
```bash
# Kích hoạt virtual environment
source .venv/bin/activate

# Cài đặt dependencies (nếu chưa cài)
pip install -r requirements.txt

# Cài đặt Playwright browsers
playwright install
```

### 2. Chạy test đầu tiên
```bash
# Chạy test cơ bản
pytest tests/test_login_ui.py -v

# Chạy test với Allure
pytest tests/test_login_ui_allure.py --alluredir=allure-results -v
```

### 3. Mở Allure Report
```bash
# Cách nhanh nhất
python open_allure_report.py auto

# Hoặc serve mode
python open_allure_report.py serve

# Hoặc generate HTML
python open_allure_report.py generate
```

## 🎯 Các lệnh thường dùng

### Chạy test
```bash
# Tất cả test
pytest

# Test cụ thể
pytest tests/test_login_ui.py

# Test với browser khác
pytest --test-browser=firefox

# Test song song
pytest -n auto
```

### Mở report
```bash
# Auto detect
python open_allure_report.py auto

# Serve mode (development)
python open_allure_report.py serve

# Generate HTML (sharing)
python open_allure_report.py generate
```

### Demo hoàn chỉnh
```bash
# Chạy demo tự động
python run_allure_demo.py
```

## 📁 Cấu trúc project

```
Playwright/
├── tests/                 # Test cases
├── pages/                 # Page Objects
├── utils/                 # Helper functions
├── api_clients/           # API & gRPC clients
├── config/               # Configuration
├── allure-results/       # Allure results
├── allure-report/        # Allure HTML report
└── screenshots/          # Screenshots khi fail
```

## 🔧 Troubleshooting nhanh

### Report không mở được
```bash
# Dùng HTTP server
cd allure-report && python -m http.server 8080
open http://localhost:8080
```

### Test fail do credentials
- Đây là expected behavior (dùng test data giả)
- Xem screenshots trong `screenshots/`
- Xem log trong `test.log`

### Allure chưa cài
```bash
# Cài đặt tự động
python allure_runner.py install

# Hoặc cài thủ công
brew install allure  # macOS
```

## 📚 Documentation đầy đủ

- **README.md** - Hướng dẫn chi tiết framework
- **OPEN_REPORT_GUIDE.md** - Cách mở Allure report
- **ALLURE_GUIDE.md** - Hướng dẫn Allure Framework
- **package.json** - NPM scripts

## 🎉 Kết quả mong đợi

✅ **Test execution** với 15 test cases  
✅ **Allure report** với step-by-step execution  
✅ **Screenshots** tự động khi fail  
✅ **Logging** chi tiết trong test.log  
✅ **Multi-browser** support  
✅ **Parallel execution** ready  

## 🚀 Next Steps

1. **Xem Allure report** để hiểu test execution
2. **Thêm test cases** mới trong `tests/`
3. **Tạo page objects** mới trong `pages/`
4. **Cấu hình CI/CD** với GitHub Actions
5. **Tích hợp với JIRA** cho issue tracking

---

**Need help?** Xem troubleshooting trong [OPEN_REPORT_GUIDE.md](OPEN_REPORT_GUIDE.md) hoặc [README.md](README.md) 