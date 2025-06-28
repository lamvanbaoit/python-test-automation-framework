# 🎯 **Hướng dẫn mở Allure Report - Complete Guide**

## 🚀 **Cách mở report nhanh nhất**

### **1. Tự động detect và mở (Khuyến nghị)**
```bash
python open_allure_report.py auto
```

### **2. Serve mode (Real-time)**
```bash
python open_allure_report.py serve
```

### **3. Generate và mở HTML**
```bash
python open_allure_report.py generate
```

## 📋 **Tất cả các cách mở report**

### **Cách 1: Sử dụng Script Python**
```bash
# Tự động detect
python open_allure_report.py auto

# Serve mode
python open_allure_report.py serve allure-results 8080

# Generate HTML
python open_allure_report.py generate allure-results allure-report

# Mở report có sẵn
python open_allure_report.py open allure-report
```

### **Cách 2: Sử dụng NPM Scripts**
```bash
# Serve với global Allure
npm run allure:serve

# Serve với NPM Allure
npm run allure:serve:npm

# Serve với local Allure
npm run allure:serve:local

# Generate và mở
npm run allure:generate
npm run allure:open

# Tự động detect
npm run allure:open:auto
```

### **Cách 3: Sử dụng Allure trực tiếp**
```bash
# Global Allure
allure serve allure-results
allure generate allure-results --clean -o allure-report
allure open allure-report

# NPM Allure
npx allure serve allure-results
npx allure generate allure-results --clean -o allure-report
npx allure open allure-report

# Local Allure
python allure_runner.py serve allure-results
python allure_runner.py generate allure-results allure-report
python allure_runner.py open allure-report
```

### **Cách 4: Demo Script (Tự động hoàn toàn)**
```bash
python run_allure_demo.py
```

## 🎨 **Các mode mở report**

### **Serve Mode (Khuyến nghị cho development)**
- ✅ **Real-time updates** - tự động refresh khi có thay đổi
- ✅ **Không cần lưu file** - temporary directory
- ✅ **Tự động mở browser** tại `http://localhost:8080`
- ✅ **Phù hợp cho development** và testing

```bash
python open_allure_report.py serve
# Browser mở tại: http://localhost:8080
```

### **Generate Mode (Khuyến nghị cho sharing)**
- ✅ **Report được lưu** trong `allure-report/` directory
- ✅ **Có thể share** qua email, Slack, file hosting
- ✅ **Phù hợp cho sharing** với team
- ✅ **Static HTML** - không cần server

```bash
python open_allure_report.py generate
# Report được tạo tại: allure-report/index.html
```

### **Auto Mode (Thông minh)**
- ✅ **Tự động detect** có results hay report
- ✅ **Tự chọn mode** phù hợp
- ✅ **Hướng dẫn** nếu chưa có data

```bash
python open_allure_report.py auto
# Tự động chọn serve hoặc open
```

## 🔧 **Tùy chọn nâng cao**

### **Serve với port tùy chỉnh**
```bash
# Port 8081
python open_allure_report.py serve allure-results 8081
allure serve allure-results --port 8081
npx allure serve allure-results --port 8081
```

### **Generate với options**
```bash
# Generate với categories
allure generate allure-results --clean -o allure-report --categories categories.json

# Generate với environment
allure generate allure-results --clean -o allure-report --environment environment.properties
```

### **Mở report từ thư mục khác**
```bash
python open_allure_report.py serve /path/to/results
python open_allure_report.py generate /path/to/results /path/to/output
python open_allure_report.py open /path/to/report
```

## 🚨 **Troubleshooting - Khắc phục khi report không mở được**

### **Vấn đề: Report cứ load và không lên**

#### **Nguyên nhân 1: CORS Policy khi mở file HTML trực tiếp**
**Giải pháp: Sử dụng HTTP Server**

```bash
# Cách 1: Python HTTP Server
cd allure-report
python -m http.server 8080
open http://localhost:8080

# Cách 2: Allure Serve (Khuyến nghị)
npx allure serve allure-results

# Cách 3: Python Script
python open_allure_report.py serve allure-results
```

#### **Nguyên nhân 2: Port 8080 bị chiếm**
```bash
# Kiểm tra port đang sử dụng
lsof -i :8080

# Dùng port khác
python open_allure_report.py serve allure-results 8081
allure serve allure-results --port 8081
npx allure serve allure-results --port 8081
```

#### **Nguyên nhân 3: Allure chưa cài đặt đúng**
```bash
# Kiểm tra cài đặt
allure --version
npx allure --version

# Cài đặt lại nếu cần
brew install allure  # macOS
npm install --save-dev allure-commandline
python allure_runner.py install
```

#### **Nguyên nhân 4: Browser không mở tự động**
```bash
# Mở thủ công
open http://localhost:8080  # macOS
start http://localhost:8080  # Windows
xdg-open http://localhost:8080  # Linux

# Hoặc mở file HTML trực tiếp (sau khi dùng HTTP server)
open allure-report/index.html  # macOS
start allure-report/index.html  # Windows
xdg-open allure-report/index.html  # Linux
```

#### **Nguyên nhân 5: Report không hiển thị đúng**
```bash
# Clear cache và regenerate
rm -rf allure-results allure-report
pytest tests/ --alluredir=allure-results
allure generate allure-results --clean -o allure-report
```

### **Vấn đề: Browser báo lỗi CORS**

#### **Giải pháp cho Chrome:**
```bash
# Đóng Chrome hoàn toàn
pkill -f "Google Chrome"

# Mở Chrome với flag
open -a "Google Chrome" --args --allow-file-access-from-files allure-report/index.html

# Hoặc dùng HTTP server (Khuyến nghị)
cd allure-report && python -m http.server 8080
open http://localhost:8080
```

#### **Giải pháp cho Firefox:**
```bash
# Mở about:config trong Firefox
# Tìm: security.fileuri.strict_origin_policy
# Đặt thành false

# Hoặc dùng HTTP server (Khuyến nghị)
cd allure-report && python -m http.server 8080
open http://localhost:8080
```

### **Vấn đề: Server không khởi động**

#### **Kiểm tra và khởi động lại:**
```bash
# Kiểm tra process đang chạy
ps aux | grep allure
ps aux | grep python

# Kill process nếu cần
pkill -f allure
pkill -f "python.*http.server"

# Khởi động lại
python open_allure_report.py serve allure-results
```

## 📊 **Cấu trúc Report**

### **Overview Dashboard**
- 📊 **Statistics**: Pass/Fail/Skip counts
- 🚀 **Launches**: Multiple run statistics
- 🎯 **Behaviors**: Features & Stories
- ⚙️ **Executors**: Test environment info
- 📈 **History Trend**: Time-based trends
- 🌍 **Environment**: System information

### **Test Steps (Step-by-Step)**
- 🔍 **Detailed Steps**: Each action logged
- 📸 **Screenshots**: Auto-attached for each step
- 📋 **Test Data**: Data used in tests
- 🔗 **API Calls**: Request/response data
- ✅ **Assertions**: Expected vs actual values

### **Navigation**
- 📁 **Suites**: Test cases by suite
- 🎯 **Behaviors**: Grouped by features/stories
- 📦 **Packages**: Grouped by package names
- ⏰ **Timeline**: Chronological execution
- 🐛 **Categories**: Defect classification

## 🎯 **Workflow khuyến nghị**

### **Development Workflow**
```bash
# 1. Chạy test
pytest tests/test_login_ui_allure.py --alluredir=allure-results -v

# 2. Mở report với serve mode
python open_allure_report.py serve

# 3. Xem report tại http://localhost:8080
```

### **Sharing Workflow**
```bash
# 1. Chạy test
pytest tests/ --alluredir=allure-results -v

# 2. Generate HTML report
python open_allure_report.py generate

# 3. Share allure-report/ folder
```

### **CI/CD Workflow**
```bash
# 1. Chạy test trong CI
pytest tests/ --alluredir=allure-results -v

# 2. Generate report
allure generate allure-results --clean -o allure-report

# 3. Upload report artifact
```

## 🔍 **Kiểm tra nhanh**

### **Kiểm tra Allure cài đặt:**
```bash
# Global
allure --version

# NPM
npx allure --version

# Local
python allure_runner.py --version
```

### **Kiểm tra results có sẵn:**
```bash
# Kiểm tra thư mục
ls -la allure-results/
ls -la allure-report/

# Kiểm tra file HTML
file allure-report/index.html
```

### **Kiểm tra server đang chạy:**
```bash
# Kiểm tra port
lsof -i :8080
lsof -i :8081

# Test connection
curl -s http://localhost:8080 | head -5
```

## 🎉 **Kết luận**

Với script `open_allure_report.py`, việc mở Allure report trở nên đơn giản và linh hoạt:

- 🚀 **Một lệnh duy nhất** để mở report
- 🔍 **Tự động detect** loại cài đặt Allure
- 🎯 **Nhiều mode** phù hợp với nhu cầu khác nhau
- 🛠️ **Troubleshooting** tích hợp sẵn
- 📱 **Cross-platform** - hoạt động trên mọi OS

### **Lưu ý quan trọng:**
- **Luôn dùng HTTP server** thay vì mở file HTML trực tiếp
- **Serve mode** tốt nhất cho development
- **Generate mode** tốt nhất cho sharing
- **Auto mode** thông minh nhất cho người dùng mới 