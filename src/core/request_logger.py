"""
Request logging system for SimuServer
"""

import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import deque

class RequestLogger:
    """Logs and manages HTTP request/response data"""
    
    def __init__(self, max_entries: int = 1000):
        self.max_entries = max_entries
        self.requests: deque = deque(maxlen=max_entries)
        self.total_requests = 0
    
    def log_request(self, method: str, url: str, headers: Dict[str, str], 
                   status_code: int, response_time: float, timestamp: datetime,
                   request_body: Optional[str] = None, response_body: Optional[str] = None):
        """Log a request/response pair"""
        
        request_data = {
            "id": self.total_requests + 1,
            "method": method,
            "url": url,
            "headers": headers,
            "status_code": status_code,
            "response_time_ms": round(response_time * 1000, 2),
            "timestamp": timestamp.isoformat(),
            "request_body": request_body,
            "response_body": response_body
        }
        
        self.requests.append(request_data)
        self.total_requests += 1
    
    def get_recent_requests(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get recent requests, optionally limited"""
        requests_list = list(self.requests)
        if limit:
            return requests_list[-limit:]
        return requests_list
    
    def get_total_requests(self) -> int:
        """Get total number of requests processed"""
        return self.total_requests
    
    def get_requests_by_method(self, method: str) -> List[Dict[str, Any]]:
        """Get requests filtered by HTTP method"""
        return [req for req in self.requests if req["method"].upper() == method.upper()]
    
    def get_requests_by_status(self, status_code: int) -> List[Dict[str, Any]]:
        """Get requests filtered by status code"""
        return [req for req in self.requests if req["status_code"] == status_code]
    
    def get_average_response_time(self) -> float:
        """Get average response time in milliseconds"""
        if not self.requests:
            return 0.0
        
        total_time = sum(req["response_time_ms"] for req in self.requests)
        return total_time / len(self.requests)
    
    def clear_logs(self):
        """Clear all logged requests"""
        self.requests.clear()
        self.total_requests = 0 