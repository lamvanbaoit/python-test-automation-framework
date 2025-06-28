#!/usr/bin/env python3
"""
Script mở Allure Report - Hỗ trợ nhiều cách mở report
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_allure_installation():
    """Kiểm tra Allure đã cài chưa"""
    # Thử allure global
    try:
        result = subprocess.run(["allure", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            return "global"
    except FileNotFoundError:
        pass
    
    # Thử npx allure
    try:
        result = subprocess.run(["npx", "allure", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            return "npm"
    except FileNotFoundError:
        pass
    
    # Thử allure_runner.py
    if os.path.exists("allure_runner.py"):
        try:
            result = subprocess.run(["python", "allure_runner.py", "serve"], capture_output=True, text=True)
            if result.returncode == 0:
                return "local"
        except:
            pass
    
    return None

def open_report_serve(results_dir="allure-results", port=8080):
    """Mở report với serve mode"""
    allure_type = check_allure_installation()
    
    if not allure_type:
        print("❌ Allure chưa được cài đặt!")
        print("📦 Cài đặt Allure:")
        print("   1. Global: brew install allure (macOS)")
        print("   2. NPM: npm install --save-dev allure-commandline")
        print("   3. Local: python allure_runner.py install")
        return False
    
    print(f"🌐 Mở Allure report với {allure_type}...")
    print(f"📱 Browser sẽ mở tại: http://localhost:{port}")
    print("⏹️  Dừng server: Ctrl+C")
    
    try:
        if allure_type == "global":
            subprocess.run(["allure", "serve", results_dir, "--port", str(port)])
        elif allure_type == "npm":
            subprocess.run(["npx", "allure", "serve", results_dir, "--port", str(port)])
        else:  # local
            subprocess.run(["python", "allure_runner.py", "serve", results_dir])
        return True
    except KeyboardInterrupt:
        print("\n👋 Đã dừng server")
        return True
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def open_report_generate(results_dir="allure-results", output_dir="allure-report"):
    """Generate và mở HTML report"""
    allure_type = check_allure_installation()
    
    if not allure_type:
        print("❌ Allure chưa được cài đặt!")
        return False
    
    print(f"📊 Generate HTML report với {allure_type}...")
    
    # Generate report
    try:
        if allure_type == "global":
            subprocess.run(["allure", "generate", results_dir, "--clean", "-o", output_dir], check=True)
        elif allure_type == "npm":
            subprocess.run(["npx", "allure", "generate", results_dir, "--clean", "-o", output_dir], check=True)
        else:  # local
            subprocess.run(["python", "allure_runner.py", "generate", results_dir, output_dir], check=True)
        
        print(f"✅ Report được tạo tại: {output_dir}/")
        
        # Mở report
        report_path = Path(output_dir) / "index.html"
        if report_path.exists():
            print(f"🌐 Mở report: {report_path}")
            webbrowser.open(f"file://{report_path.absolute()}")
            return True
        else:
            print(f"❌ Không tìm thấy file: {report_path}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi generate report: {e}")
        return False

def open_report_direct(report_dir="allure-report"):
    """Mở report trực tiếp từ thư mục có sẵn"""
    report_path = Path(report_dir) / "index.html"
    
    if not report_path.exists():
        print(f"❌ Không tìm thấy report tại: {report_path}")
        print("💡 Hãy chạy generate report trước:")
        print("   python open_allure_report.py generate")
        return False
    
    print(f"🌐 Mở report trực tiếp: {report_path}")
    webbrowser.open(f"file://{report_path.absolute()}")
    return True

def main():
    """Main function"""
    print("🎯 Allure Report Opener")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("📋 Cách sử dụng:")
        print("  python open_allure_report.py serve [results_dir] [port]")
        print("  python open_allure_report.py generate [results_dir] [output_dir]")
        print("  python open_allure_report.py open [report_dir]")
        print("  python open_allure_report.py auto")
        print("\n📝 Ví dụ:")
        print("  python open_allure_report.py serve allure-results 8080")
        print("  python open_allure_report.py generate allure-results allure-report")
        print("  python open_allure_report.py open allure-report")
        print("  python open_allure_report.py auto")
        return
    
    command = sys.argv[1]
    
    if command == "serve":
        results_dir = sys.argv[2] if len(sys.argv) > 2 else "allure-results"
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        open_report_serve(results_dir, port)
        
    elif command == "generate":
        results_dir = sys.argv[2] if len(sys.argv) > 2 else "allure-results"
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "allure-report"
        open_report_generate(results_dir, output_dir)
        
    elif command == "open":
        report_dir = sys.argv[2] if len(sys.argv) > 2 else "allure-report"
        open_report_direct(report_dir)
        
    elif command == "auto":
        # Tự động detect và mở report
        print("🔍 Tự động detect và mở report...")
        
        # Kiểm tra có results không
        if os.path.exists("allure-results"):
            print("📁 Tìm thấy allure-results, mở với serve mode...")
            open_report_serve("allure-results", 8080)
        elif os.path.exists("allure-report"):
            print("📁 Tìm thấy allure-report, mở trực tiếp...")
            open_report_direct("allure-report")
        else:
            print("❌ Không tìm thấy allure-results hoặc allure-report")
            print("💡 Hãy chạy test trước:")
            print("   pytest tests/ --alluredir=allure-results")
            
    else:
        print(f"❌ Command không hợp lệ: {command}")

if __name__ == "__main__":
    main() 