"""
Performance monitoring system for SimuServer
"""

import psutil
import threading
import time
from datetime import datetime
from typing import Dict, List, Any
from collections import deque

class PerformanceMonitor:
    """Monitors system performance metrics"""
    
    def __init__(self, update_interval: float = 1.0, history_size: int = 100):
        self.update_interval = update_interval
        self.history_size = history_size
        
        # Performance data storage
        self.cpu_history: deque = deque(maxlen=history_size)
        self.memory_history: deque = deque(maxlen=history_size)
        self.network_history: deque = deque(maxlen=history_size)
        
        # Request tracking
        self.request_count = 0
        self.requests_per_second = 0
        self.last_request_time = time.time()
        
        # Monitoring thread
        self.monitoring_thread = None
        self.is_monitoring = False
        
        # Initial network stats for delta calculation
        self.last_network_stats = psutil.net_io_counters()
    
    def start(self):
        """Start performance monitoring"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitoring_thread.start()
    
    def stop(self):
        """Stop performance monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=1.0)
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=None)
                
                # Memory usage
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                memory_used_mb = memory.used / (1024 * 1024)
                memory_available_mb = memory.available / (1024 * 1024)
                
                # Network I/O
                current_network = psutil.net_io_counters()
                network_sent_delta = current_network.bytes_sent - self.last_network_stats.bytes_sent
                network_recv_delta = current_network.bytes_recv - self.last_network_stats.bytes_recv
                self.last_network_stats = current_network
                
                # Calculate requests per second
                current_time = time.time()
                time_delta = current_time - self.last_request_time
                if time_delta >= 1.0:
                    self.requests_per_second = self.request_count / time_delta
                    self.request_count = 0
                    self.last_request_time = current_time
                
                # Store data with timestamp
                timestamp = datetime.now()
                
                self.cpu_history.append({
                    "timestamp": timestamp.isoformat(),
                    "value": cpu_percent
                })
                
                self.memory_history.append({
                    "timestamp": timestamp.isoformat(),
                    "percent": memory_percent,
                    "used_mb": memory_used_mb,
                    "available_mb": memory_available_mb
                })
                
                self.network_history.append({
                    "timestamp": timestamp.isoformat(),
                    "sent_bytes_delta": network_sent_delta,
                    "recv_bytes_delta": network_recv_delta
                })
                
            except Exception as e:
                print(f"Performance monitoring error: {e}")
            
            time.sleep(self.update_interval)
    
    def update_request_count(self):
        """Update request count for RPS calculation"""
        self.request_count += 1
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        try:
            # Current CPU
            cpu_percent = psutil.cpu_percent(interval=None)
            
            # Current Memory
            memory = psutil.virtual_memory()
            
            # Disk usage for data directory
            disk = psutil.disk_usage('/')
            
            return {
                "cpu": {
                    "percent": cpu_percent,
                    "count": psutil.cpu_count()
                },
                "memory": {
                    "percent": memory.percent,
                    "used_mb": round(memory.used / (1024 * 1024), 2),
                    "available_mb": round(memory.available / (1024 * 1024), 2),
                    "total_mb": round(memory.total / (1024 * 1024), 2)
                },
                "disk": {
                    "percent": disk.percent,
                    "used_gb": round(disk.used / (1024 * 1024 * 1024), 2),
                    "free_gb": round(disk.free / (1024 * 1024 * 1024), 2)
                },
                "network": {
                    "requests_per_second": round(self.requests_per_second, 2)
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_history_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get historical performance data"""
        return {
            "cpu": list(self.cpu_history),
            "memory": list(self.memory_history),
            "network": list(self.network_history)
        }
    
    def clear_history(self):
        """Clear all historical data"""
        self.cpu_history.clear()
        self.memory_history.clear()
        self.network_history.clear() 