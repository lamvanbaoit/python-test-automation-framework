#!/usr/bin/env python3
"""
Test Suite Manager - Quản lý test suites cho 1000 test cases
"""

import os
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import logging
from datetime import datetime

@dataclass
class TestSuite:
    """Data class cho test suite"""
    name: str
    description: str
    test_count: int
    execution_time: float = 0.0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    created_at: str = ""
    last_run: str = ""

@dataclass
class TestExecution:
    """Data class cho test execution"""
    suite_name: str
    test_name: str
    status: str  # passed, failed, skipped
    duration: float
    error_message: str = ""
    screenshot_path: str = ""
    log_path: str = ""

class TestSuiteManager:
    """Quản lý test suites cho 1000 test cases"""
    
    def __init__(self, suites_dir: str = "test_suites"):
        self.suites_dir = suites_dir
        self.logger = logging.getLogger(__name__)
        self._ensure_suites_dir()
        self.suites = self._load_suites()
    
    def _ensure_suites_dir(self):
        """Đảm bảo thư mục test suites tồn tại"""
        os.makedirs(self.suites_dir, exist_ok=True)
        os.makedirs(f"{self.suites_dir}/reports", exist_ok=True)
        os.makedirs(f"{self.suites_dir}/configs", exist_ok=True)
    
    def _load_suites(self) -> Dict[str, TestSuite]:
        """Load test suites từ file"""
        suites = {}
        config_file = f"{self.suites_dir}/configs/suites.json"
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for suite_data in data.get("suites", []):
                        suite = TestSuite(**suite_data)
                        suites[suite.name] = suite
        except Exception as e:
            self.logger.error(f"Error loading suites: {e}")
        
        return suites
    
    def _save_suites(self):
        """Save test suites vào file"""
        config_file = f"{self.suites_dir}/configs/suites.json"
        try:
            data = {"suites": [asdict(suite) for suite in self.suites.values()]}
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving suites: {e}")
    
    def create_suite(self, name: str, description: str, test_count: int = 0) -> TestSuite:
        """Tạo test suite mới"""
        suite = TestSuite(
            name=name,
            description=description,
            test_count=test_count,
            created_at=datetime.now().isoformat()
        )
        
        self.suites[name] = suite
        self._save_suites()
        self.logger.info(f"Created test suite: {name}")
        
        return suite
    
    def get_suite(self, name: str) -> Optional[TestSuite]:
        """Lấy test suite theo tên"""
        return self.suites.get(name)
    
    def list_suites(self) -> List[TestSuite]:
        """Liệt kê tất cả test suites"""
        return list(self.suites.values())
    
    def update_suite_stats(self, name: str, passed: int, failed: int, skipped: int, duration: float):
        """Cập nhật thống kê test suite"""
        if name in self.suites:
            suite = self.suites[name]
            suite.passed = passed
            suite.failed = failed
            suite.skipped = skipped
            suite.execution_time = duration
            suite.last_run = datetime.now().isoformat()
            self._save_suites()
    
    def get_suite_execution_plan(self, suite_name: str) -> Dict[str, Any]:
        """Tạo execution plan cho test suite"""
        suite = self.get_suite(suite_name)
        if not suite:
            return {}
        
        # Phân chia test cases theo loại
        plan = {
            "suite_name": suite_name,
            "total_tests": suite.test_count,
            "execution_groups": {
                "smoke": {"tests": [], "parallel": 1},
                "regression": {"tests": [], "parallel": 4},
                "ui": {"tests": [], "parallel": 2},
                "api": {"tests": [], "parallel": 8},
                "grpc": {"tests": [], "parallel": 4},
                "integration": {"tests": [], "parallel": 2}
            },
            "estimated_duration": suite.test_count * 30,  # 30s per test
            "resources": {
                "browsers": ["chromium", "firefox", "webkit"],
                "workers": 8,
                "memory": "4GB",
                "cpu": "4 cores"
            }
        }
        
        return plan
    
    def generate_test_files(self, suite_name: str, test_types: List[str]):
        """Generate test files cho suite"""
        suite = self.get_suite(suite_name)
        if not suite:
            return
        
        for test_type in test_types:
            self._generate_test_file(suite_name, test_type)
    
    def _generate_test_file(self, suite_name: str, test_type: str):
        """Generate test file cho một loại test"""
        test_dir = f"tests/{test_type}"
        os.makedirs(test_dir, exist_ok=True)
        
        filename = f"{test_dir}/test_{suite_name}_{test_type}.py"
        
        template = self._get_test_template(test_type, suite_name)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(template)
            self.logger.info(f"Generated test file: {filename}")
        except Exception as e:
            self.logger.error(f"Error generating test file {filename}: {e}")
    
    def _get_test_template(self, test_type: str, suite_name: str) -> str:
        """Lấy template cho test file"""
        if test_type == "ui":
            return f'''# Generated UI tests for {suite_name}
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from test_data.test_data_manager import test_data_manager

@pytest.mark.ui
@pytest.mark.{suite_name}
class Test{suite_name.title()}UI:
    
    def test_login_flow(self, page):
        """Test login flow"""
        user = test_data_manager.get_user("standard")
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(user.username, user.password)
        assert login_page.is_logged_in()
    
    def test_inventory_page(self, page):
        """Test inventory page"""
        inventory_page = InventoryPage(page)
        inventory_page.goto()
        assert inventory_page.is_inventory_page_loaded()
'''
        
        elif test_type == "api":
            return f'''# Generated API tests for {suite_name}
import pytest
from api_clients.user_api_client import UserApiClient
from test_data.test_data_manager import test_data_manager

@pytest.mark.api
@pytest.mark.{suite_name}
class Test{suite_name.title()}API:
    
    def test_user_login_api(self):
        """Test user login API"""
        api_client = UserApiClient()
        user = test_data_manager.get_user("standard")
        response = api_client.login(user.username, user.password)
        assert response.status_code == 200
'''
        
        else:
            return f'''# Generated {test_type} tests for {suite_name}
import pytest

@pytest.mark.{test_type}
@pytest.mark.{suite_name}
class Test{suite_name.title()}{test_type.upper()}:
    
    def test_sample(self):
        """Sample test"""
        assert True
'''
    
    def create_execution_report(self, suite_name: str, executions: List[TestExecution]) -> Dict[str, Any]:
        """Tạo execution report cho test suite"""
        report = {
            "suite_name": suite_name,
            "execution_time": datetime.now().isoformat(),
            "summary": {
                "total": len(executions),
                "passed": len([e for e in executions if e.status == "passed"]),
                "failed": len([e for e in executions if e.status == "failed"]),
                "skipped": len([e for e in executions if e.status == "skipped"])
            },
            "executions": [asdict(execution) for execution in executions],
            "duration": sum(e.duration for e in executions),
            "success_rate": len([e for e in executions if e.status == "passed"]) / len(executions) * 100 if executions else 0
        }
        
        # Save report
        report_file = f"{self.suites_dir}/reports/{suite_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving report: {e}")
        
        return report
    
    def get_performance_metrics(self, suite_name: str) -> Dict[str, Any]:
        """Lấy performance metrics cho test suite"""
        suite = self.get_suite(suite_name)
        if not suite:
            return {}
        
        return {
            "suite_name": suite_name,
            "total_tests": suite.test_count,
            "avg_execution_time": suite.execution_time / suite.test_count if suite.test_count > 0 else 0,
            "success_rate": suite.passed / suite.test_count * 100 if suite.test_count > 0 else 0,
            "last_run": suite.last_run,
            "created_at": suite.created_at
        }

# Global instance
test_suite_manager = TestSuiteManager() 