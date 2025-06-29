# ALLURE REPORT GUIDE

## 1. Cài đặt Allure CLI
- macOS: `brew install allure`
- Ubuntu: `sudo apt-get install -y allure`
- Windows: [Download Allure CLI](https://docs.qameta.io/allure/#_installing_a_commandline)

## 2. Chạy test với Allure
```bash
pytest tests/ --alluredir=allure-results --headless -v
```

## 3. Generate Allure report
```bash
allure generate allure-results --clean -o allure-report
```

## 4. Mở Allure report
```bash
allure open allure-report
```
- **KHÔNG mở file allure-report/index.html trực tiếp bằng file:// trên browser!**
- Luôn dùng lệnh `allure open allure-report` để xem report đầy đủ.

## 5. Lưu ý version
- pytest >=7.0.0,<8.0.0
- pytest-asyncio==0.21.1
- allure-pytest>=2.13.2

## 6. Troubleshooting
- Nếu report chỉ hiện Loading...: bạn đã mở file trực tiếp, hãy dùng lệnh `allure open allure-report`.
- Nếu lỗi plugin: kiểm tra lại version pytest, pytest-asyncio, allure-pytest.
- Nếu cần, xoá allure-results/, allure-report/ và chạy lại.

## 7. Tham khảo thêm
- Xem README.md, QUICK_START.md, OPEN_REPORT_GUIDE.md, MASS_TESTING_GUIDE.md 