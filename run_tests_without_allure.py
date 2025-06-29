#!/usr/bin/env python3
"""
Script chạy test mà không cần Allure plugin để tránh lỗi compatibility
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path

def run_tests_without_allure():
    """Chạy test mà không cần Allure plugin"""
    
    # Tạo thư mục cần thiết
    os.makedirs("allure-results", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Command để chạy test mà không có Allure plugin
    cmd = [
        "pytest",
        "tests/",
        "--html=report.html",
        "--self-contained-html",
        "--no-allure",  # Disable Allure plugin
        "-v",
        "--tb=short"
    ]
    
    print("🚀 Chạy test mà không cần Allure plugin...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        # Chạy test
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # In output
        if result.stdout:
            print("=== STDOUT ===")
            print(result.stdout)
        
        if result.stderr:
            print("=== STDERR ===")
            print(result.stderr)
        
        print(f"Exit code: {result.returncode}")
        
        # Tạo file kết quả đơn giản cho Allure
        if result.returncode == 0:
            create_simple_allure_results()
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Lỗi khi chạy test: {e}")
        return False

def create_simple_allure_results():
    """Tạo file kết quả đơn giản cho Allure"""
    
    # Tạo file environment.json
    environment_data = {
        "browser": "chromium",
        "base_url": "https://www.saucedemo.com/",
        "environment": "test",
        "timestamp": datetime.now().isoformat()
    }
    
    env_file = Path("allure-results") / "environment.json"
    with open(env_file, 'w') as f:
        json.dump(environment_data, f, indent=2)
    
    print(f"✅ Đã tạo file environment: {env_file}")

def generate_allure_report():
    """Generate Allure report từ kết quả đã có"""
    
    print("📊 Generate Allure report...")
    
    # Kiểm tra xem có Allure CLI không
    try:
        result = subprocess.run(["allure", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            # Dùng Allure CLI
            cmd = ["allure", "generate", "allure-results", "--clean", "-o", "allure-report"]
            subprocess.run(cmd, check=True)
            print("✅ Allure report được tạo thành công!")
            return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    # Thử dùng allure_runner.py
    try:
        cmd = ["python", "allure_runner.py", "generate", "allure-results", "allure-report"]
        subprocess.run(cmd, check=True)
        print("✅ Allure report được tạo thành công với allure_runner.py!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi generate Allure report: {e}")
        return False

def open_allure_report():
    """Mở Allure report"""
    
    print("🌐 Mở Allure report...")
    
    # Thử dùng allure_runner.py
    try:
        cmd = ["python", "open_allure_report.py", "auto"]
        subprocess.run(cmd)
        return True
    except Exception as e:
        print(f"❌ Lỗi khi mở Allure report: {e}")
        return False

def main():
    """Main function"""
    print("🎯 Test Runner - Không cần Allure Plugin")
    print("=" * 50)
    
    # Chạy test
    success = run_tests_without_allure()
    
    if success:
        print("\n✅ Test chạy thành công!")
        
        # Generate Allure report
        if generate_allure_report():
            # Mở report
            open_allure_report()
    else:
        print("\n❌ Test thất bại!")
        sys.exit(1)

if __name__ == "__main__":
    main() 