# MASS TESTING GUIDE

## 1. Mục tiêu
- Hỗ trợ chạy 1000+ test case tự động, tối ưu performance, artifact, báo cáo, CI/CD.

## 2. Chạy mass testing local
```bash
pytest tests/ --mass-test --test-suite=regression_suite --headless -n auto --alluredir=allure-results --html=report.html --self-contained-html -v
```
- Có thể tuỳ chỉnh số lượng test, suite, browser, worker.

## 3. CI/CD mass testing
- Đã tích hợp workflow `.github/workflows/mass-testing.yml`:
  - Tự động generate test data, chạy song song, tối ưu performance
  - Sinh Allure report, HTML report, upload artifact, performance
  - Cleanup file tạm, cache

## 4. Artifact & Performance
- Artifact: allure-report/, allure-results/, screenshots/, test.log, report.html
- Performance: test_suites/reports/, test_data/dynamic/
- Có thể download artifact từ GitHub Actions

## 5. Lưu ý version
- pytest >=7.0.0,<8.0.0
- pytest-asyncio==0.21.1
- allure-pytest>=2.13.2

## 6. Best practice
- Luôn chạy headless, song song trên CI
- Dọn dẹp file tạm, cache sau mỗi run
- Theo dõi performance, tối ưu worker

## 7. Tham khảo thêm
- Xem README.md, QUICK_START.md, ALLURE_GUIDE.md, OPEN_REPORT_GUIDE.md 