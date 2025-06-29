#!/usr/bin/env python3
"""
Allure Runner Script - Chạy Allure mà không cần cài đặt global
"""

import os
import sys
import subprocess
import json
import urllib.request
import zipfile
import tarfile
import platform
from pathlib import Path

# Lớp hỗ trợ cài đặt và chạy Allure local cho project mà không cần cài đặt toàn cục
class AllureRunner:
    """Allure Runner class để cài đặt và chạy Allure local"""
    
    def __init__(self):
        # Thư mục project
        self.project_dir = Path(__file__).parent
        # Thư mục chứa allure-commandline
        self.allure_dir = self.project_dir / "allure-commandline"
        self.allure_bin = None
        self.allure_version = "2.24.0"
        
    def get_system_info(self):
        """Lấy thông tin hệ điều hành hiện tại"""
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        if system == "darwin":  # macOS
            return "macos"
        elif system == "windows":
            return "windows"
        elif system == "linux":
            return "linux"
        else:
            raise Exception(f"Unsupported system: {system}")
    
    def get_allure_url(self):
        """Lấy URL download Allure phù hợp hệ điều hành"""
        system = self.get_system_info()
        base_url = f"https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/{self.allure_version}"
        
        if system == "macos":
            return f"{base_url}/allure-commandline-{self.allure_version}.tgz"
        elif system == "windows":
            return f"{base_url}/allure-commandline-{self.allure_version}.zip"
        elif system == "linux":
            return f"{base_url}/allure-commandline-{self.allure_version}.tgz"
    
    def download_allure(self):
        """Download và cài đặt Allure vào thư mục project"""
        if self.allure_dir.exists():
            print(f"✅ Allure đã được cài đặt tại: {self.allure_dir}")
            return True
        
        print(f"📥 Đang download Allure {self.allure_version}...")
        url = self.get_allure_url()
        if not url:
            print("❌ Không thể lấy URL download")
            return False
            
        archive_name = url.split("/")[-1]
        archive_path = self.project_dir / archive_name
        
        try:
            # Download file nén
            urllib.request.urlretrieve(url, archive_path)
            print(f"✅ Download thành công: {archive_name}")
            
            # Giải nén file
            print("📦 Đang extract...")
            if archive_name.endswith(".zip"):
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(self.project_dir)
            else:  # .tgz
                with tarfile.open(archive_path, 'r:gz') as tar_ref:
                    tar_ref.extractall(self.project_dir)
            
            # Đổi tên thư mục extract thành allure-commandline
            extracted_dir = self.project_dir / f"allure-{self.allure_version}"
            if extracted_dir.exists():
                extracted_dir.rename(self.allure_dir)
            
            # Xác định đường dẫn file chạy allure
            system = self.get_system_info()
            if system == "windows":
                self.allure_bin = self.allure_dir / "bin" / "allure.bat"
            else:
                self.allure_bin = self.allure_dir / "bin" / "allure"
            
            # Set quyền thực thi cho file allure (Unix)
            if system != "windows":
                os.chmod(self.allure_bin, 0o755)
            
            # Xoá file nén sau khi giải nén
            archive_path.unlink()
            
            print(f"✅ Allure đã được cài đặt tại: {self.allure_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khi cài đặt Allure: {e}")
            if archive_path.exists():
                archive_path.unlink()
            return False
    
    def run_allure(self, command, args=None):
        """Chạy lệnh Allure với các tham số truyền vào"""
        if not self.allure_bin or not self.allure_bin.exists():
            if not self.download_allure():
                return False
        
        cmd = [str(self.allure_bin), command]
        if args:
            cmd.extend(args)
        
        print(f"🚀 Chạy: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Lỗi: {e}")
            if e.stderr:
                print(f"Stderr: {e.stderr}")
            return False
    
    def serve(self, results_dir="allure-results"):
        """Chạy allure serve để mở report dạng web server"""
        return self.run_allure("serve", [results_dir])
    
    def generate(self, results_dir="allure-results", output_dir="allure-report"):
        """Chạy allure generate để tạo HTML report"""
        return self.run_allure("generate", [results_dir, "--clean", "-o", output_dir])
    
    def open(self, report_dir="allure-report"):
        """Chạy allure open để mở report HTML đã generate"""
        return self.run_allure("open", [report_dir])

def main():
    """Hàm main để chạy script allure_runner.py từ command line"""
    runner = AllureRunner()
    
    if len(sys.argv) < 2:
        print("📋 Cách sử dụng:")
        print("  python allure_runner.py serve [results_dir]")
        print("  python allure_runner.py generate [results_dir] [output_dir]")
        print("  python allure_runner.py open [report_dir]")
        print("  python allure_runner.py install")
        return
    
    command = sys.argv[1]
    
    if command == "install":
        runner.download_allure()
    elif command == "serve":
        results_dir = sys.argv[2] if len(sys.argv) > 2 else "allure-results"
        runner.serve(results_dir)
    elif command == "generate":
        results_dir = sys.argv[2] if len(sys.argv) > 2 else "allure-results"
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "allure-report"
        runner.generate(results_dir, output_dir)
    elif command == "open":
        report_dir = sys.argv[2] if len(sys.argv) > 2 else "allure-report"
        runner.open(report_dir)
    else:
        print(f"❌ Command không hợp lệ: {command}")

if __name__ == "__main__":
    main() 