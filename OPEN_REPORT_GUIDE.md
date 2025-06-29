# OPEN ALLURE REPORT GUIDE

## 1. Mở Allure report đúng cách
```bash
allure open allure-report
```
- **KHÔNG mở file allure-report/index.html trực tiếp bằng file:// trên browser!**
- Luôn dùng lệnh `allure open allure-report` để xem report đầy đủ.

## 2. Cài đặt Allure CLI
- macOS: `brew install allure`
- Ubuntu: `sudo apt-get install -y allure`
- Windows: [Download Allure CLI](https://docs.qameta.io/allure/#_installing_a_commandline)

## 3. Troubleshooting
- Nếu report chỉ hiện Loading...: bạn đã mở file trực tiếp, hãy dùng lệnh `allure open allure-report`.
- Nếu lỗi plugin: kiểm tra lại version pytest, pytest-asyncio, allure-pytest.

## 4. Tham khảo thêm
- Xem README.md, QUICK_START.md, ALLURE_GUIDE.md, MASS_TESTING_GUIDE.md 