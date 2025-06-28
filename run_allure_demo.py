#!/usr/bin/env python3
"""
Demo script để chạy test với Allure Framework
Tạo report step-by-step như ZaloPay
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def run_command(command, description):
    """Chạy command và hiển thị output"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"📝 Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print("Output:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print("Stdout:")
            print(e.stdout)
        if e.stderr:
            print("Stderr:")
            print(e.stderr)
        return False

def check_allure_installation():
    """Kiểm tra Allure đã cài chưa"""
    print("🔍 Kiểm tra Allure Framework...")
    
    # Thử allure global
    if run_command("allure --version", "Check global Allure"):
        return "global"
    
    # Thử npx allure
    if run_command("npx allure --version", "Check NPM Allure"):
        return "npm"
    
    # Thử allure_runner.py
    if os.path.exists("allure_runner.py"):
        if run_command("python allure_runner.py install", "Install local Allure"):
            return "local"
    
    return None

def main():
    """Main function để chạy demo Allure"""
    print("🎯 Allure Framework Demo - Step-by-Step Reporting như ZaloPay")
    print("=" * 80)
    
    # Kiểm tra Allure installation
    allure_type = check_allure_installation()
    
    if not allure_type:
        print("❌ Allure chưa được cài đặt!")
        print("📦 Cài đặt Allure:")
        print("   1. Global: brew install allure (macOS)")
        print("   2. NPM: npm install --save-dev allure-commandline")
        print("   3. Local: python allure_runner.py install")
        return
    
    print(f"✅ Allure đã được cài đặt: {allure_type}")
    
    # Tạo thư mục allure-results nếu chưa có
    os.makedirs("allure-results", exist_ok=True)
    
    # Chạy test với Allure
    print("\n🚀 Bắt đầu chạy test với Allure Framework...")
    
    # Chạy test Allure
    test_command = "pytest tests/test_login_ui_allure.py --alluredir=allure-results -v"
    if not run_command(test_command, "Chạy test với Allure"):
        print("❌ Test failed! Kiểm tra lỗi ở trên.")
        return
    
    # Tạo environment.properties
    print("\n📋 Tạo environment info...")
    env_content = f"""Browser=Chromium
BaseURL=https://www.saucedemo.com/
Headless=False
Platform={os.name}
PythonVersion={sys.version}
Timestamp={datetime.now().isoformat()}
Framework=Playwright + Pytest + Allure
AllureType={allure_type}
"""
    
    with open("allure-results/environment.properties", "w") as f:
        f.write(env_content)
    
    print("✅ Environment info created!")
    
    # Generate HTML report
    print("\n📊 Tạo HTML report...")
    
    if allure_type == "global":
        generate_command = "allure generate allure-results --clean -o allure-report"
    elif allure_type == "npm":
        generate_command = "npx allure generate allure-results --clean -o allure-report"
    else:  # local
        generate_command = "python allure_runner.py generate allure-results allure-report"
    
    if not run_command(generate_command, "Generate HTML report"):
        print("❌ Failed to generate report!")
        return
    
    # Mở report
    print("\n🌐 Mở Allure report...")
    print("📖 Report được tạo tại: allure-report/index.html")
    print("🔗 Mở browser để xem report...")
    
    # Mở report trong browser
    if sys.platform == "darwin":  # macOS
        run_command("open allure-report/index.html", "Open report in browser")
    elif sys.platform == "win32":  # Windows
        run_command("start allure-report/index.html", "Open report in browser")
    else:  # Linux
        run_command("xdg-open allure-report/index.html", "Open report in browser")
    
    # Serve report (optional)
    print("\n🌍 Serve report với Allure server...")
    print("📝 Để xem report với server:")
    
    if allure_type == "global":
        print("   allure serve allure-results")
    elif allure_type == "npm":
        print("   npx allure serve allure-results")
    else:  # local
        print("   python allure_runner.py serve allure-results")
    
    print("📝 Để dừng server: Ctrl+C")
    
    serve_choice = input("\n🤔 Bạn có muốn serve report với Allure server không? (y/n): ")
    if serve_choice.lower() in ['y', 'yes']:
        print("🚀 Starting Allure server...")
        print("📱 Mở browser tại: http://localhost:8080")
        print("⏹️  Dừng server: Ctrl+C")
        
        if allure_type == "global":
            run_command("allure serve allure-results", "Serve Allure report")
        elif allure_type == "npm":
            run_command("npx allure serve allure-results", "Serve Allure report")
        else:  # local
            run_command("python allure_runner.py serve allure-results", "Serve Allure report")
    
    print("\n🎉 Demo hoàn thành!")
    print("📁 Files được tạo:")
    print("   - allure-results/: Test results")
    print("   - allure-report/: HTML report")
    print("   - screenshots/: Screenshots")
    print("   - test.log: Test logs")
    print(f"   - Allure Type: {allure_type}")

if __name__ == "__main__":
    main() 