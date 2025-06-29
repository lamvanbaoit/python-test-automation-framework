#!/usr/bin/env python3
"""
Development Tools Script - Tự động format, lint, type check code
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Chạy command và hiển thị kết quả"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} thành công")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} thất bại:")
        print(f"Error: {e.stderr}")
        return False

def format_code():
    """Format code với black"""
    return run_command("black .", "Format code với Black")

def lint_code():
    """Lint code với flake8"""
    return run_command("flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics", "Lint code với Flake8 (errors)")
    run_command("flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics", "Lint code với Flake8 (warnings)")

def type_check():
    """Type check với mypy"""
    return run_command("mypy . --ignore-missing-imports", "Type check với MyPy")

def run_tests():
    """Chạy test nhanh"""
    return run_command("pytest tests/ -v --tb=short", "Chạy tests")

def run_smoke_tests():
    """Chạy smoke tests"""
    return run_command("pytest tests/ -m smoke -v", "Chạy smoke tests")

def run_allure_tests():
    """Chạy tests với Allure"""
    return run_command("pytest tests/ --alluredir=allure-results -v", "Chạy tests với Allure")

def open_allure_report():
    """Mở Allure report"""
    return run_command("allure serve allure-results", "Mở Allure report")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("🔧 Development Tools")
        print("=" * 50)
        print("Cách sử dụng:")
        print("  python scripts/dev_tools.py format     # Format code")
        print("  python scripts/dev_tools.py lint       # Lint code")
        print("  python scripts/dev_tools.py type       # Type check")
        print("  python scripts/dev_tools.py test       # Chạy tests")
        print("  python scripts/dev_tools.py smoke      # Chạy smoke tests")
        print("  python scripts/dev_tools.py allure     # Chạy tests với Allure")
        print("  python scripts/dev_tools.py report     # Mở Allure report")
        print("  python scripts/dev_tools.py all        # Chạy tất cả (format, lint, type, test)")
        return

    command = sys.argv[1]
    
    if command == "format":
        format_code()
    elif command == "lint":
        lint_code()
    elif command == "type":
        type_check()
    elif command == "test":
        run_tests()
    elif command == "smoke":
        run_smoke_tests()
    elif command == "allure":
        run_allure_tests()
    elif command == "report":
        open_allure_report()
    elif command == "all":
        print("🚀 Chạy tất cả development tools...")
        success = True
        success &= format_code()
        success &= lint_code()
        success &= type_check()
        success &= run_tests()
        
        if success:
            print("🎉 Tất cả checks đã pass!")
        else:
            print("⚠️  Một số checks đã fail. Vui lòng kiểm tra và sửa lỗi.")
            sys.exit(1)
    else:
        print(f"❌ Command không hợp lệ: {command}")

if __name__ == "__main__":
    main() 