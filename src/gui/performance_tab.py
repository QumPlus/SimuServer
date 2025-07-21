"""
Performance monitoring tab for SimuServer GUI
"""

import tkinter as tk
import customtkinter as ctk
import time
from datetime import datetime

class PerformanceTab:
    """Performance monitoring tab showing system metrics"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.server_engine = None
        
        # Configure grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(2, weight=1)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create performance monitoring widgets"""
        
        # Header
        header_frame = ctk.CTkFrame(self.parent)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame, 
            text="System Performance Monitoring", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        # CPU Frame
        cpu_frame = ctk.CTkFrame(self.parent)
        cpu_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)
        cpu_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(cpu_frame, text="CPU Usage", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, pady=(10, 5)
        )
        
        self.cpu_progress = ctk.CTkProgressBar(cpu_frame, width=200)
        self.cpu_progress.grid(row=1, column=0, padx=20, pady=5)
        self.cpu_progress.set(0)
        
        self.cpu_label = ctk.CTkLabel(cpu_frame, text="0.0%")
        self.cpu_label.grid(row=2, column=0, pady=(5, 10))
        
        # Memory Frame
        memory_frame = ctk.CTkFrame(self.parent)
        memory_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=5)
        memory_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(memory_frame, text="Memory Usage", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, pady=(10, 5)
        )
        
        self.memory_progress = ctk.CTkProgressBar(memory_frame, width=200)
        self.memory_progress.grid(row=1, column=0, padx=20, pady=5)
        self.memory_progress.set(0)
        
        self.memory_label = ctk.CTkLabel(memory_frame, text="0.0%")
        self.memory_label.grid(row=2, column=0, pady=(5, 10))
        
        # Detailed metrics frame
        metrics_frame = ctk.CTkFrame(self.parent)
        metrics_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(5, 10))
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
        metrics_frame.grid_rowconfigure(1, weight=1)
        
        # Metrics header
        ctk.CTkLabel(
            metrics_frame, 
            text="Detailed Metrics", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Left metrics column
        left_metrics = ctk.CTkScrollableFrame(metrics_frame)
        left_metrics.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(0, 10))
        
        # CPU Details
        ctk.CTkLabel(left_metrics, text="CPU Information", font=ctk.CTkFont(size=14, weight="bold")).pack(
            anchor="w", padx=10, pady=(10, 5)
        )
        
        self.cpu_count_label = ctk.CTkLabel(left_metrics, text="Cores: -")
        self.cpu_count_label.pack(anchor="w", padx=20, pady=2)
        
        self.cpu_percent_label = ctk.CTkLabel(left_metrics, text="Usage: -%")
        self.cpu_percent_label.pack(anchor="w", padx=20, pady=2)
        
        # Memory Details
        ctk.CTkLabel(left_metrics, text="Memory Information", font=ctk.CTkFont(size=14, weight="bold")).pack(
            anchor="w", padx=10, pady=(20, 5)
        )
        
        self.memory_total_label = ctk.CTkLabel(left_metrics, text="Total: - MB")
        self.memory_total_label.pack(anchor="w", padx=20, pady=2)
        
        self.memory_used_label = ctk.CTkLabel(left_metrics, text="Used: - MB")
        self.memory_used_label.pack(anchor="w", padx=20, pady=2)
        
        self.memory_available_label = ctk.CTkLabel(left_metrics, text="Available: - MB")
        self.memory_available_label.pack(anchor="w", padx=20, pady=2)
        
        # Right metrics column
        right_metrics = ctk.CTkScrollableFrame(metrics_frame)
        right_metrics.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))
        
        # Network/Server Details
        ctk.CTkLabel(right_metrics, text="Server Information", font=ctk.CTkFont(size=14, weight="bold")).pack(
            anchor="w", padx=10, pady=(10, 5)
        )
        
        self.requests_per_second_label = ctk.CTkLabel(right_metrics, text="Requests/sec: 0")
        self.requests_per_second_label.pack(anchor="w", padx=20, pady=2)
        
        self.total_requests_label = ctk.CTkLabel(right_metrics, text="Total Requests: 0")
        self.total_requests_label.pack(anchor="w", padx=20, pady=2)
        
        self.uptime_label = ctk.CTkLabel(right_metrics, text="Uptime: 0s")
        self.uptime_label.pack(anchor="w", padx=20, pady=2)
        
        self.websocket_connections_label = ctk.CTkLabel(right_metrics, text="WebSocket Connections: 0")
        self.websocket_connections_label.pack(anchor="w", padx=20, pady=2)
        
        # Disk Information
        ctk.CTkLabel(right_metrics, text="Disk Information", font=ctk.CTkFont(size=14, weight="bold")).pack(
            anchor="w", padx=10, pady=(20, 5)
        )
        
        self.disk_usage_label = ctk.CTkLabel(right_metrics, text="Usage: -%")
        self.disk_usage_label.pack(anchor="w", padx=20, pady=2)
        
        self.disk_free_label = ctk.CTkLabel(right_metrics, text="Free: - GB")
        self.disk_free_label.pack(anchor="w", padx=20, pady=2)
        
        self.disk_used_label = ctk.CTkLabel(right_metrics, text="Used: - GB")
        self.disk_used_label.pack(anchor="w", padx=20, pady=2)
        
        # Control buttons
        control_frame = ctk.CTkFrame(metrics_frame)
        control_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        self.refresh_button = ctk.CTkButton(
            control_frame,
            text="Refresh Now",
            command=self._manual_refresh,
            width=120
        )
        self.refresh_button.pack(side="left", padx=10, pady=10)
        
        self.clear_history_button = ctk.CTkButton(
            control_frame,
            text="Clear History",
            command=self._clear_history,
            width=120
        )
        self.clear_history_button.pack(side="left", padx=10, pady=10)
        
        # Last updated label
        self.last_updated_label = ctk.CTkLabel(control_frame, text="Last updated: Never")
        self.last_updated_label.pack(side="right", padx=10, pady=10)
    
    def update_metrics(self, metrics):
        """Update the performance metrics display"""
        if not metrics or "error" in metrics:
            return
        
        try:
            # Update CPU
            cpu_percent = metrics.get("cpu", {}).get("percent", 0)
            self.cpu_progress.set(cpu_percent / 100)
            self.cpu_label.configure(text=f"{cpu_percent:.1f}%")
            
            cpu_count = metrics.get("cpu", {}).get("count", 0)
            self.cpu_count_label.configure(text=f"Cores: {cpu_count}")
            self.cpu_percent_label.configure(text=f"Usage: {cpu_percent:.1f}%")
            
            # Update Memory
            memory_percent = metrics.get("memory", {}).get("percent", 0)
            self.memory_progress.set(memory_percent / 100)
            self.memory_label.configure(text=f"{memory_percent:.1f}%")
            
            memory_total = metrics.get("memory", {}).get("total_mb", 0)
            memory_used = metrics.get("memory", {}).get("used_mb", 0)
            memory_available = metrics.get("memory", {}).get("available_mb", 0)
            
            self.memory_total_label.configure(text=f"Total: {memory_total:.0f} MB")
            self.memory_used_label.configure(text=f"Used: {memory_used:.0f} MB")
            self.memory_available_label.configure(text=f"Available: {memory_available:.0f} MB")
            
            # Update Network/Server info
            rps = metrics.get("network", {}).get("requests_per_second", 0)
            self.requests_per_second_label.configure(text=f"Requests/sec: {rps}")
            
            # Get additional server info if available
            if self.server_engine:
                total_requests = self.server_engine.request_logger.get_total_requests()
                self.total_requests_label.configure(text=f"Total Requests: {total_requests}")
                
                # Calculate uptime
                if self.server_engine.start_time:
                    uptime = time.time() - self.server_engine.start_time
                    uptime_str = self._format_uptime(uptime)
                    self.uptime_label.configure(text=f"Uptime: {uptime_str}")
                
                # WebSocket connections
                ws_count = len(self.server_engine.websocket_connections)
                self.websocket_connections_label.configure(text=f"WebSocket Connections: {ws_count}")
            
            # Update Disk info
            disk_percent = metrics.get("disk", {}).get("percent", 0)
            disk_free = metrics.get("disk", {}).get("free_gb", 0)
            disk_used = metrics.get("disk", {}).get("used_gb", 0)
            
            self.disk_usage_label.configure(text=f"Usage: {disk_percent:.1f}%")
            self.disk_free_label.configure(text=f"Free: {disk_free:.1f} GB")
            self.disk_used_label.configure(text=f"Used: {disk_used:.1f} GB")
            
            # Update timestamp
            self.last_updated_label.configure(text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
            
        except Exception as e:
            print(f"Error updating metrics: {e}")
    
    def _format_uptime(self, seconds):
        """Format uptime in a readable format"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes:.0f}m {secs:.0f}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours:.0f}h {minutes:.0f}m"
    
    def _manual_refresh(self):
        """Manually refresh metrics"""
        if self.server_engine:
            metrics = self.server_engine.get_performance_data()
            self.update_metrics(metrics)
    
    def _clear_history(self):
        """Clear performance history"""
        if self.server_engine and self.server_engine.performance_monitor:
            self.server_engine.performance_monitor.clear_history()
    
    def set_server_engine(self, server_engine):
        """Set the server engine reference"""
        self.server_engine = server_engine 