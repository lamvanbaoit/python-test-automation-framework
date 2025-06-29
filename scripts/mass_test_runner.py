#!/usr/bin/env python3
"""
Mass Test Runner - Chạy 1000 test cases một cách tối ưu
"""

import os
import sys
import time
import json
import subprocess
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import logging
from datetime import datetime
import argparse

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_data.test_data_manager import test_data_manager
from utils.test_suite_manager import test_suite_manager
from utils.performance_optimizer import performance_optimizer

@dataclass
class TestRunConfig:
    """Configuration cho test run"""
    suite_name: str
    test_count: int
    parallel_workers: int
    browsers: List[str]
    headless: bool = True
    retry_failed: bool = True
    generate_report: bool = True
    cleanup_after: bool = True

class MassTestRunner:
    """Runner cho 1000 test cases"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        self.results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "total_time": 0,
            "start_time": "",
            "end_time": ""
        }
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('mass_test_runner.log'),
                logging.StreamHandler()
            ]
        )
    
    def create_test_suite(self, suite_name: str, test_count: int = 1000) -> TestRunConfig:
        """Tạo test suite mới"""
        self.logger.info(f"Creating test suite: {suite_name} with {test_count} tests")
        
        # Create suite in test suite manager
        suite = test_suite_manager.create_suite(suite_name, f"Mass test suite with {test_count} tests", test_count)
        
        # Generate test data
        test_data_manager.create_test_suite_data(suite_name, test_count)
        
        # Calculate optimal configuration
        workers = performance_optimizer.calculate_optimal_workers(test_count)
        
        config = TestRunConfig(
            suite_name=suite_name,
            test_count=test_count,
            parallel_workers=workers,
            browsers=["chromium", "firefox", "webkit"],
            headless=True,
            retry_failed=True,
            generate_report=True,
            cleanup_after=True
        )
        
        return config
    
    def generate_test_files(self, config: TestRunConfig):
        """Generate test files cho suite"""
        self.logger.info(f"Generating test files for suite: {config.suite_name}")
        
        # Calculate test distribution
        test_types = ["ui", "api", "grpc", "integration"]
        test_counts = {
            "ui": int(config.test_count * 0.4),      # 40% UI tests
            "api": int(config.test_count * 0.3),     # 30% API tests
            "grpc": int(config.test_count * 0.2),    # 20% gRPC tests
            "integration": int(config.test_count * 0.1)  # 10% Integration tests
        }
        
        for test_type, count in test_counts.items():
            if count > 0:
                test_suite_manager.generate_test_files(config.suite_name, [test_type])
                self.logger.info(f"Generated {count} {test_type} tests")
    
    def run_tests(self, config: TestRunConfig) -> Dict[str, Any]:
        """Chạy tests với configuration"""
        self.logger.info(f"Starting test execution for suite: {config.suite_name}")
        
        start_time = datetime.now()
        self.results["start_time"] = start_time.isoformat()
        
        # Create execution plan
        execution_plan = performance_optimizer.create_execution_plan({
            "test_count": config.test_count,
            "test_files": self._get_test_files()
        })
        
        self.logger.info(f"Execution plan: {json.dumps(execution_plan, indent=2)}")
        
        # Run tests with pytest
        pytest_args = self._build_pytest_args(config, execution_plan)
        
        try:
            result = subprocess.run(pytest_args, capture_output=True, text=True, timeout=3600)  # 1 hour timeout
            
            # Parse results
            self._parse_pytest_output(result.stdout, result.stderr)
            
        except subprocess.TimeoutExpired:
            self.logger.error("Test execution timed out after 1 hour")
            self.results["failed"] = config.test_count
        except Exception as e:
            self.logger.error(f"Error running tests: {e}")
            self.results["failed"] = config.test_count
        
        end_time = datetime.now()
        self.results["end_time"] = end_time.isoformat()
        self.results["total_time"] = (end_time - start_time).total_seconds()
        
        # Update suite statistics
        test_suite_manager.update_suite_stats(
            config.suite_name,
            self.results["passed"],
            self.results["failed"],
            self.results["skipped"],
            self.results["total_time"]
        )
        
        return self.results
    
    def _build_pytest_args(self, config: TestRunConfig, execution_plan: Dict[str, Any]) -> List[str]:
        """Build pytest arguments"""
        args = [
            "pytest",
            "-v",
            "--tb=short",
            f"-n={config.parallel_workers}",
            "--dist=loadfile",
            "--alluredir=allure-results",
            "--html=report.html",
            "--self-contained-html",
            "--capture=no",
            "--disable-warnings"
        ]
        
        # Add markers
        args.extend([
            "-m", f"{config.suite_name}",
            "tests/"
        ])
        
        # Add browser options
        if config.headless:
            args.extend(["--headless"])
        
        # Add retry options
        if config.retry_failed:
            args.extend(["--reruns", "2", "--reruns-delay", "1"])
        
        return args
    
    def _get_test_files(self) -> List[str]:
        """Lấy danh sách test files"""
        test_files = []
        test_dirs = ["tests/ui", "tests/api", "tests/grpc", "tests/integration"]
        
        for test_dir in test_dirs:
            if os.path.exists(test_dir):
                for file in os.listdir(test_dir):
                    if file.endswith(".py") and file.startswith("test_"):
                        test_files.append(os.path.join(test_dir, file))
        
        return test_files
    
    def _parse_pytest_output(self, stdout: str, stderr: str):
        """Parse pytest output để lấy kết quả"""
        # Simple parsing - in real implementation, use pytest hooks
        lines = stdout.split('\n')
        
        for line in lines:
            if "passed" in line.lower():
                self.results["passed"] += 1
            elif "failed" in line.lower():
                self.results["failed"] += 1
            elif "skipped" in line.lower():
                self.results["skipped"] += 1
    
    def generate_reports(self, config: TestRunConfig):
        """Generate reports sau khi chạy test"""
        if not config.generate_report:
            return
        
        self.logger.info("Generating test reports...")
        
        # Generate Allure report
        try:
            subprocess.run([
                "./allure-commandline/bin/allure", "generate", 
                "allure-results", "-o", "allure-report", "--clean"
            ], check=True)
            self.logger.info("Allure report generated successfully")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error generating Allure report: {e}")
        
        # Generate performance report
        performance_report = performance_optimizer.get_performance_report([])
        
        report_file = f"test_suites/reports/performance_{config.suite_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(performance_report, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Performance report saved to {report_file}")
        except Exception as e:
            self.logger.error(f"Error saving performance report: {e}")
    
    def cleanup(self, config: TestRunConfig):
        """Cleanup sau khi chạy test"""
        if not config.cleanup_after:
            return
        
        self.logger.info("Cleaning up resources...")
        
        # Cleanup test data
        test_data_manager.cleanup_test_data(older_than_days=1)
        
        # Cleanup performance optimizer
        performance_optimizer.cleanup_resources()
        
        # Cleanup temporary files
        temp_dirs = ["__pycache__", ".pytest_cache"]
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                    self.logger.info(f"Cleaned up {temp_dir}")
                except Exception as e:
                    self.logger.warning(f"Error cleaning up {temp_dir}: {e}")
    
    def run_mass_test(self, suite_name: str, test_count: int = 1000) -> Dict[str, Any]:
        """Main method để chạy mass test"""
        self.logger.info(f"Starting mass test run: {suite_name} with {test_count} tests")
        
        try:
            # Create test suite
            config = self.create_test_suite(suite_name, test_count)
            
            # Generate test files
            self.generate_test_files(config)
            
            # Run tests
            results = self.run_tests(config)
            
            # Generate reports
            self.generate_reports(config)
            
            # Cleanup
            self.cleanup(config)
            
            self.logger.info(f"Mass test run completed: {results}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in mass test run: {e}")
            return {"error": str(e)}

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Mass Test Runner for 1000 test cases")
    parser.add_argument("--suite", required=True, help="Test suite name")
    parser.add_argument("--count", type=int, default=1000, help="Number of tests to run")
    parser.add_argument("--workers", type=int, help="Number of parallel workers")
    parser.add_argument("--headless", action="store_true", default=True, help="Run in headless mode")
    
    args = parser.parse_args()
    
    runner = MassTestRunner()
    results = runner.run_mass_test(args.suite, args.count)
    
    print(f"Test Results: {json.dumps(results, indent=2)}")

if __name__ == "__main__":
    main() 