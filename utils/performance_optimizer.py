#!/usr/bin/env python3
"""
Performance Optimizer - Tối ưu performance cho 1000 test cases
"""

import os
import time
import psutil
import threading
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import platform

def safe_float(val, default=0.0):
    try:
        return float(val)
    except Exception:
        return default

@dataclass
class PerformanceMetrics:
    """Data class cho performance metrics"""
    cpu_usage: float
    memory_usage: float
    disk_io: float
    network_io: float
    execution_time: float
    test_count: int
    parallel_workers: int

    def to_dict(self):
        return {
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "disk_io": self.disk_io,
            "network_io": self.network_io,
            "execution_time": self.execution_time,
            "test_count": self.test_count,
            "parallel_workers": self.parallel_workers
        }

class PerformanceOptimizer:
    """Tối ưu performance cho 1000 test cases"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics_history = []
        self.optimization_config = self._load_optimization_config()
    
    def _load_optimization_config(self) -> Dict[str, Any]:
        """Load optimization configuration"""
        cpu_count = psutil.cpu_count()
        return {
            "max_workers": min(cpu_count or 4, 8),  # Max 8 workers
            "memory_limit": 0.8,  # 80% memory usage limit
            "cpu_limit": 0.9,     # 90% CPU usage limit
            "browser_pool_size": 3,  # Max 3 browsers per worker
            "test_timeout": 300,   # 5 minutes per test
            "retry_count": 2,      # Retry failed tests
            "parallel_strategy": "dynamic"  # dynamic, fixed, adaptive
        }
    
    @staticmethod
    def get_system_resources():
        # Lấy thông tin tài nguyên hệ thống, an toàn cho mọi OS
        try:
            cpu_freq = None
            try:
                cpu_freq_obj = psutil.cpu_freq()
                if cpu_freq_obj:
                    cpu_freq = cpu_freq_obj.current
            except Exception:
                cpu_freq = None
            return {
                "cpu_count": safe_float(psutil.cpu_count(logical=True)),
                "memory_total": safe_float(psutil.virtual_memory().total),
                "memory_available": safe_float(psutil.virtual_memory().available),
                "cpu_percent": safe_float(psutil.cpu_percent(interval=0.1)),
                "cpu_freq": safe_float(cpu_freq),
                "platform": platform.platform(),
            }
        except Exception as e:
            return {"error": str(e)}
    
    def calculate_optimal_workers(self, test_count: int) -> int:
        """Tính toán số lượng workers tối ưu"""
        system_resources = self.get_system_resources()
        cpu_workers = int(safe_float(system_resources.get("cpu_count"), 2) * 0.8)
        memory_workers = int(safe_float(system_resources.get("memory_available"), 2) * 2)  # 2GB per worker
        test_workers = min(test_count // 10, 20)  # Max 20 workers
        optimal_workers = min(cpu_workers, memory_workers, test_workers, self.optimization_config["max_workers"])
        self.logger.info(f"Optimal workers: {optimal_workers} (CPU: {cpu_workers}, Memory: {memory_workers}, Tests: {test_workers})")
        return max(1, optimal_workers)
    
    def optimize_test_distribution(self, test_files: List[str], test_count: int) -> Dict[str, List[str]]:
        """Tối ưu phân phối test files"""
        workers = self.calculate_optimal_workers(test_count)
        test_groups = {"ui": [], "api": [], "grpc": [], "integration": []}
        for test_file in test_files:
            if "ui" in test_file.lower():
                test_groups["ui"].append(test_file)
            elif "api" in test_file.lower():
                test_groups["api"].append(test_file)
            elif "grpc" in test_file.lower():
                test_groups["grpc"].append(test_file)
            else:
                test_groups["integration"].append(test_file)
        distribution = {}
        worker_id = 0
        for test_type, files in test_groups.items():
            if files:
                files_per_worker = max(1, len(files) // workers)
                for i in range(0, len(files), files_per_worker):
                    worker_key = f"worker_{worker_id}"
                    distribution[worker_key] = {
                        "type": test_type,
                        "files": files[i:i + files_per_worker],
                        "estimated_time": len(files[i:i + files_per_worker]) * 30
                    }
                    worker_id = (worker_id + 1) % workers
        return distribution
    
    def monitor_performance(self, duration: int = 60) -> List[PerformanceMetrics]:
        """Monitor performance trong quá trình chạy test"""
        metrics = []
        start_time = time.time()
        def collect_metrics():
            while time.time() - start_time < duration:
                system_resources = self.get_system_resources()
                memory_total = safe_float(system_resources.get("memory_total"), 1.0)
                memory_available = safe_float(system_resources.get("memory_available"), 0.0)
                memory_usage = memory_available / memory_total if memory_total > 0 else 0.0
                metric = PerformanceMetrics(
                    cpu_usage=safe_float(system_resources.get("cpu_percent"), 0.0),
                    memory_usage=memory_usage,
                    disk_io=0.0,
                    network_io=0.0,
                    execution_time=time.time() - start_time,
                    test_count=0,
                    parallel_workers=self.calculate_optimal_workers(1000)
                )
                metrics.append(metric)
                time.sleep(5)
        monitor_thread = threading.Thread(target=collect_metrics)
        monitor_thread.daemon = True
        monitor_thread.start()
        return metrics
    
    def optimize_browser_pool(self, worker_count: int) -> Dict[str, Any]:
        max_browsers = worker_count * self.optimization_config["browser_pool_size"]
        browser_config = {
            "chromium": {"instances": max_browsers // 3, "memory_limit": "512MB", "cpu_limit": 0.5},
            "firefox": {"instances": max_browsers // 3, "memory_limit": "768MB", "cpu_limit": 0.6},
            "webkit": {"instances": max_browsers // 3, "memory_limit": "256MB", "cpu_limit": 0.4}
        }
        return browser_config
    
    def create_execution_plan(self, test_suite: Dict[str, Any]) -> Dict[str, Any]:
        test_count = test_suite.get("test_count", 1000)
        test_files = test_suite.get("test_files", [])
        workers = self.calculate_optimal_workers(test_count)
        distribution = self.optimize_test_distribution(test_files, test_count)
        browser_config = self.optimize_browser_pool(workers)
        plan = {
            "execution_strategy": "parallel",
            "workers": workers,
            "test_distribution": distribution,
            "browser_config": browser_config,
            "estimated_duration": test_count * 30 / workers if workers > 0 else 0,
            "resource_requirements": {
                "memory": f"{workers * 2}GB",
                "cpu": f"{workers} cores",
                "disk": "10GB"
            },
            "optimization_settings": {
                "headless": True,
                "disable_images": True,
                "disable_javascript": False,
                "disable_css": False,
                "timeout": self.optimization_config["test_timeout"]
            }
        }
        return plan
    
    def cleanup_resources(self):
        """Cleanup resources sau khi chạy test"""
        # Kill zombie browser processes
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and any(browser in proc.info['name'].lower() 
                                           for browser in ['chrome', 'firefox', 'webkit']):
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Clear temporary files
        temp_dirs = ['screenshots', 'allure-results', '__pycache__']
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                    self.logger.info(f"Cleaned up {temp_dir}")
                except Exception as e:
                    self.logger.warning(f"Error cleaning up {temp_dir}: {e}")
    
    def get_performance_report(self, metrics_list):
        system_resources = self.get_system_resources()
        cpu_percent = safe_float(system_resources.get("cpu_percent", 0.0))
        memory_total = safe_float(system_resources.get("memory_total", 1.0))
        memory_available = safe_float(system_resources.get("memory_available", 0.0))
        memory_usage = 1 - (memory_available / memory_total) if memory_total > 0 else 0.0
        metric = PerformanceMetrics(
            cpu_usage=cpu_percent,
            memory_usage=memory_usage,
            disk_io=0.0,
            network_io=0.0,
            execution_time=0.0,
            test_count=0,
            parallel_workers=0,
        )
        return metric.to_dict()
    
    def _generate_recommendations(self, avg_cpu: float, avg_memory: float) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        if avg_cpu > 80:
            recommendations.append("Consider reducing parallel workers to lower CPU usage")
        
        if avg_memory > 80:
            recommendations.append("Consider reducing browser instances or increasing memory")
        
        if avg_cpu < 50 and avg_memory < 60:
            recommendations.append("Consider increasing parallel workers for better resource utilization")
        
        if not recommendations:
            recommendations.append("Current resource usage is optimal")
        
        return recommendations

# Global instance
performance_optimizer = PerformanceOptimizer() 