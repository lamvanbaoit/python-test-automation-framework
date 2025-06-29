# QUICK START

## 1. Cài đặt
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
- **Lưu ý version:**
  - pytest >=7.0.0,<8.0.0
  - pytest-asyncio==0.21.1
  - allure-pytest>=2.13.2

## 2. Chạy test
```bash
pytest tests/ --alluredir=allure-results --html=report.html --self-contained-html -v --headless
```

## 3. Xuất và mở Allure report
```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```
- **Không mở file allure-report/index.html trực tiếp bằng file://**
- Nếu chưa có Allure CLI: `brew install allure` hoặc `sudo apt-get install -y allure`

## 4. Dọn dẹp file tạm
- Đã ignore: __pycache__/, *.pyc, allure-results/, allure-report/, screenshots/, test.log, report.html, videos/

## 5. Tham khảo thêm
- Xem README.md, ALLURE_GUIDE.md, OPEN_REPORT_GUIDE.md, MASS_TESTING_GUIDE.md