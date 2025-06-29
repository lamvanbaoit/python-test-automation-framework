# config/settings.py

import os
import sys
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class TestConfig:
    """Configuration cho test execution"""
    # Base URLs
    base_url: str = "https://www.saucedemo.com"
    api_base_url: str = "https://api.example.com"
    grpc_server: str = "localhost:50051"
    
    # Browser settings
    default_browser: str = "chromium"
    headless: bool = True
    slow_mo: int = 0
    
    # Timeout settings
    default_timeout: int = 30000
    navigation_timeout: int = 30000
    element_timeout: int = 10000
    
    # Mass testing settings
    mass_test_mode: bool = False
    max_workers: int = 8
    test_timeout: int = 300  # 5 minutes per test
    retry_count: int = 2
    
    # Performance settings
    disable_images: bool = False
    disable_css: bool = False
    disable_javascript: bool = False
    cache_enabled: bool = True
    
    # Reporting settings
    allure_results_dir: str = "allure-results"
    screenshots_dir: str = "screenshots"
    videos_dir: str = "videos"
    logs_dir: str = "logs"
    
    # Test data settings
    test_data_dir: str = "test_data"
    static_data_dir: str = "test_data/static"
    dynamic_data_dir: str = "test_data/dynamic"
    
    # CI/CD settings
    ci_mode: bool = False
    parallel_execution: bool = True
    artifact_retention_days: int = 7

@dataclass
class DatabaseConfig:
    """Configuration cho database connections"""
    host: str = "localhost"
    port: int = 5432
    database: str = "test_db"
    username: str = "test_user"
    password: str = "test_pass"
    
    # Connection pool settings
    max_connections: int = 10
    min_connections: int = 2
    connection_timeout: int = 30

@dataclass
class APIConfig:
    """Configuration cho API testing"""
    base_url: str = "https://api.example.com"
    timeout: int = 30
    retry_count: int = 3
    auth_token: Optional[str] = None
    
    # Rate limiting
    requests_per_second: int = 100
    burst_limit: int = 50
    
    # Headers
    default_headers: Dict[str, str] = field(default_factory=lambda: {
        "Content-Type": "application/json",
        "User-Agent": "Test-Automation-Framework"
    })

@dataclass
class gRPCConfig:
    """Configuration cho gRPC testing"""
    server_host: str = "localhost"
    server_port: int = 50051
    timeout: int = 30
    max_message_size: int = 4194304  # 4MB
    
    # Connection settings
    keep_alive_time: int = 30
    keep_alive_timeout: int = 5
    keep_alive_permit_without_calls: bool = True

@dataclass
class AllureConfig:
    """Configuration cho Allure reporting"""
    results_dir: str = "allure-results"
    report_dir: str = "allure-report"
    commandline_path: str = "./allure-commandline/bin/allure"
    
    # Report settings
    clean_results: bool = True
    generate_report: bool = True
    open_report: bool = False
    
    # Environment info
    environment_properties: Dict[str, str] = field(default_factory=lambda: {
        "Framework": "Playwright + Pytest + Allure",
        "Language": "Python",
        "CI": "false"
    })

class Settings:
    """Main settings class quản lý tất cả configurations"""
    
    def __init__(self):
        self.test = TestConfig()
        self.database = DatabaseConfig()
        self.api = APIConfig()
        self.grpc = gRPCConfig()
        self.allure = AllureConfig()
        
        # Load environment variables
        self._load_environment_variables()
        
        # Create directories
        self._create_directories()
    
    def _load_environment_variables(self):
        """Load configuration từ environment variables"""
        # Test configuration
        self.test.base_url = os.getenv("TEST_BASE_URL", self.test.base_url)
        self.test.api_base_url = os.getenv("API_BASE_URL", self.test.api_base_url)
        self.test.grpc_server = os.getenv("GRPC_SERVER", self.test.grpc_server)
        self.test.headless = os.getenv("HEADLESS", "true").lower() == "true"
        self.test.mass_test_mode = os.getenv("MASS_TEST_MODE", "false").lower() == "true"
        self.test.max_workers = int(os.getenv("MAX_WORKERS", str(self.test.max_workers)))
        
        # CI/CD detection
        self.test.ci_mode = any([
            os.getenv('CI') == 'true',
            os.getenv('GITHUB_ACTIONS') == 'true',
            os.getenv('TRAVIS') == 'true',
            os.getenv('CIRCLECI') == 'true'
        ])
        
        # Database configuration
        self.database.host = os.getenv("DB_HOST", self.database.host)
        self.database.port = int(os.getenv("DB_PORT", str(self.database.port)))
        self.database.database = os.getenv("DB_NAME", self.database.database)
        self.database.username = os.getenv("DB_USER", self.database.username)
        self.database.password = os.getenv("DB_PASSWORD", self.database.password)
        
        # API configuration
        self.api.base_url = os.getenv("API_BASE_URL", self.api.base_url)
        self.api.auth_token = os.getenv("API_AUTH_TOKEN", self.api.auth_token)
        
        # gRPC configuration
        self.grpc.server_host = os.getenv("GRPC_HOST", self.grpc.server_host)
        self.grpc.server_port = int(os.getenv("GRPC_PORT", str(self.grpc.server_port)))
    
    def _create_directories(self):
        """Tạo các thư mục cần thiết"""
        directories = [
            self.test.allure_results_dir,
            self.test.screenshots_dir,
            self.test.videos_dir,
            self.test.logs_dir,
            self.test.test_data_dir,
            self.test.static_data_dir,
            self.test.dynamic_data_dir
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def get_mass_testing_config(self) -> Dict[str, Any]:
        """Lấy configuration cho mass testing"""
        return {
            "browser": {
                "headless": self.test.headless,
                "slow_mo": self.test.slow_mo,
                "args": self._get_browser_args()
            },
            "performance": {
                "disable_images": self.test.disable_images,
                "disable_css": self.test.disable_css,
                "disable_javascript": self.test.disable_javascript,
                "cache_enabled": self.test.cache_enabled
            },
            "execution": {
                "max_workers": self.test.max_workers,
                "test_timeout": self.test.test_timeout,
                "retry_count": self.test.retry_count,
                "parallel": self.test.parallel_execution
            },
            "reporting": {
                "allure_results_dir": self.test.allure_results_dir,
                "screenshots_dir": self.test.screenshots_dir,
                "videos_dir": self.test.videos_dir
            }
        }
    
    def _get_browser_args(self) -> list:
        """Lấy browser arguments cho mass testing"""
        args = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-web-security"
        ]
        
        if self.test.mass_test_mode:
            args.extend([
                "--disable-images",
                "--disable-javascript",
                "--disable-plugins",
                "--disable-extensions",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding"
            ])
        
        return args
    
    def get_environment_info(self) -> Dict[str, str]:
        """Lấy thông tin môi trường cho Allure report"""
        return {
            "Framework": "Playwright + Pytest + Allure",
            "Language": "Python",
            "BaseURL": self.test.base_url,
            "Browser": self.test.default_browser,
            "Headless": str(self.test.headless),
            "MassTestMode": str(self.test.mass_test_mode),
            "MaxWorkers": str(self.test.max_workers),
            "CI": str(self.test.ci_mode),
            "Platform": os.name,
            "PythonVersion": sys.version
        }
    
    def update_for_mass_testing(self):
        """Cập nhật settings cho mass testing"""
        self.test.mass_test_mode = True
        self.test.headless = True
        self.test.disable_images = True
        self.test.disable_css = True
        self.test.cache_enabled = True
        self.test.max_workers = min(self.test.max_workers, 8)
        self.test.test_timeout = 300
        self.test.retry_count = 2

# Global settings instance
settings = Settings()

# Legacy compatibility
BASE_URL = settings.test.base_url
API_BASE_URL = settings.test.api_base_url
GRPC_SERVER = settings.test.grpc_server 
