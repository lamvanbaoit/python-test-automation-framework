#!/usr/bin/env python3
"""
Script hoàn chỉnh để chạy test và xuất Allure report
Khắc phục lỗi Allure plugin compatibility
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path

def run_tests():
    """Chạy tất cả test cases"""
    
    print("🧪 Chạy test cases...")
    print("=" * 50)
    
    # Tạo thư mục cần thiết
    os.makedirs("allure-results", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Command để chạy test
    cmd = [
        "pytest",
        "tests/",
        "--html=report.html",
        "--self-contained-html",
        "--no-allure",  # Disable Allure plugin để tránh lỗi
        "-v",
        "--tb=short"
    ]
    
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        # Chạy test
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        end_time = time.time()
        
        # In output
        if result.stdout:
            print("=== TEST RESULTS ===")
            print(result.stdout)
        
        if result.stderr:
            print("=== ERRORS ===")
            print(result.stderr)
        
        duration = end_time - start_time
        print(f"⏱️  Thời gian chạy: {duration:.2f} giây")
        print(f"📊 Exit code: {result.returncode}")
        
        return result.returncode == 0, duration
        
    except Exception as e:
        print(f"❌ Lỗi khi chạy test: {e}")
        return False, 0

def generate_allure_report():
    """Generate Allure report"""
    
    print("\n📊 Generate Allure report...")
    print("=" * 50)
    
    try:
        # Dùng allure_runner.py để generate report
        cmd = ["python", "allure_runner.py", "generate", "allure-results", "allure-report"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Allure report được tạo thành công!")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ Lỗi khi generate Allure report")
            if result.stderr:
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def open_allure_report():
    """Mở Allure report"""
    
    print("\n🌐 Mở Allure report...")
    print("=" * 50)
    
    try:
        # Kiểm tra file report có tồn tại không
        report_path = Path("allure-report") / "index.html"
        if not report_path.exists():
            print("❌ Không tìm thấy Allure report!")
            return False
        
        # Mở report
        cmd = ["python", "open_allure_report.py", "open", "allure-report"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Allure report đã được mở!")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ Lỗi khi mở Allure report")
            if result.stderr:
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def show_summary():
    """Hiển thị tóm tắt kết quả"""
    
    print("\n📋 TÓM TẮT KẾT QUẢ")
    print("=" * 50)
    
    # Kiểm tra các file report
    files_to_check = [
        ("HTML Report", "report.html"),
        ("Allure Report", "allure-report/index.html"),
        ("Allure Results", "allure-results/"),
        ("Screenshots", "screenshots/"),
        ("Test Log", "test.log")
    ]
    
    for name, path in files_to_check:
        if os.path.exists(path):
            if os.path.isdir(path):
                count = len(os.listdir(path))
                print(f"✅ {name}: {path} ({count} files)")
            else:
                size = os.path.getsize(path)
                print(f"✅ {name}: {path} ({size} bytes)")
        else:
            print(f"❌ {name}: {path} (không tồn tại)")
    
    print("\n🎯 Cách xem report:")
    print("1. HTML Report: Mở file report.html trong browser")
    print("2. Allure Report: Đã được mở tự động")
    print("3. Screenshots: Xem trong thư mục screenshots/")
    print("4. Test Log: Xem file test.log")

def main():
    """Main function"""
    print("🎯 Test Automation Framework - Runner")
    print("Khắc phục lỗi Allure plugin compatibility")
    print("=" * 60)
    
    # Chạy test
    success, duration = run_tests()
    
    if success:
        print(f"\n✅ Test chạy thành công trong {duration:.2f} giây!")
        
        # Generate Allure report
        if generate_allure_report():
            # Mở report
            open_allure_report()
        
        # Hiển thị tóm tắt
        show_summary()
        
    else:
        print(f"\n❌ Test thất bại sau {duration:.2f} giây!")
        
        # Vẫn thử generate report nếu có thể
        if generate_allure_report():
            open_allure_report()
        
        show_summary()
        sys.exit(1)

if __name__ == "__main__":
    main() 