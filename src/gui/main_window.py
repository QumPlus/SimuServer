"""
Main GUI window for SimuServer
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import threading
import time
from pathlib import Path

from ..core.server_engine import ServerEngine
from .performance_tab import PerformanceTab
from .api_simulator_tab import APISimulatorTab
from .logs_tab import LogsTab
from .storage_tab import StorageTab
from .request_inspector_tab import RequestInspectorTab

class SimuServerGUI:
    """Main GUI application for SimuServer"""
    
    def __init__(self, config):
        self.config = config
        self.server_engine = None
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("SimuServer - Universal API Simulation Tool")
        self.root.geometry(config.get("gui.window_size", "1200x800"))
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        self._create_widgets()
        self._setup_server()
    
    def _create_widgets(self):
        """Create all GUI widgets"""
        
        # Header frame
        header_frame = ctk.CTkFrame(self.root)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # SimuServer title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="SimuServer", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=10)
        
        # Creator info
        creator_label = ctk.CTkLabel(
            header_frame, 
            text="Created by QumPlus", 
            font=ctk.CTkFont(size=12)
        )
        creator_label.grid(row=1, column=0, padx=20, pady=(0, 10))
        
        # Server status and controls
        status_frame = ctk.CTkFrame(header_frame)
        status_frame.grid(row=0, column=1, rowspan=2, sticky="e", padx=20, pady=10)
        
        self.status_label = ctk.CTkLabel(
            status_frame, 
            text="Server: Stopped", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.status_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 5))
        
        self.server_url_label = ctk.CTkLabel(
            status_frame, 
            text="", 
            font=ctk.CTkFont(size=12)
        )
        self.server_url_label.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 10))
        
        # Server control buttons
        self.start_button = ctk.CTkButton(
            status_frame,
            text="Start Server",
            command=self._start_server,
            width=100
        )
        self.start_button.grid(row=2, column=0, padx=(20, 5), pady=(0, 10))
        
        self.stop_button = ctk.CTkButton(
            status_frame,
            text="Stop Server",
            command=self._stop_server,
            state="disabled",
            width=100
        )
        self.stop_button.grid(row=2, column=1, padx=(5, 20), pady=(0, 10))
        
        # Main content with tabview
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        # Create tabs
        self._create_tabs()
        
        # Status bar
        self.status_bar = ctk.CTkLabel(
            self.root, 
            text="Ready", 
            height=30
        )
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
    
    def _create_tabs(self):
        """Create all tabs"""
        
        # API Simulator Tab
        api_tab = self.tabview.add("API Simulator")
        self.api_simulator_tab = APISimulatorTab(api_tab, self.config, self._log_message)
        
        # Request Inspector Tab
        inspector_tab = self.tabview.add("Request Inspector")
        self.request_inspector_tab = RequestInspectorTab(inspector_tab, self.config)
        
        # Performance Tab
        performance_tab = self.tabview.add("Performance")
        self.performance_tab = PerformanceTab(performance_tab, self.config)
        
        # Logs Tab
        logs_tab = self.tabview.add("Logs")
        self.logs_tab = LogsTab(logs_tab, self.config)
        
        # Storage Settings Tab
        storage_tab = self.tabview.add("Storage")
        self.storage_tab = StorageTab(storage_tab, self.config)
    
    def _setup_server(self):
        """Setup the server engine"""
        self.server_engine = ServerEngine(self.config, self._log_message)
        
        # Pass server engine to tabs that need it
        if hasattr(self, 'api_simulator_tab'):
            self.api_simulator_tab.set_server_engine(self.server_engine)
        if hasattr(self, 'request_inspector_tab'):
            self.request_inspector_tab.set_server_engine(self.server_engine)
        if hasattr(self, 'performance_tab'):
            self.performance_tab.set_server_engine(self.server_engine)
    
    def _start_server(self):
        """Start the server"""
        try:
            if self.server_engine.start_server():
                self.status_label.configure(text="Server: Running", text_color="green")
                host = self.config.get("server.host", "127.0.0.1")
                port = self.config.get("server.port", 8000)
                self.server_url_label.configure(text=f"http://{host}:{port}")
                
                self.start_button.configure(state="disabled")
                self.stop_button.configure(state="normal")
                
                # Start performance monitoring update
                self._start_performance_updates()
                
                self._log_message("✅ Server started successfully!")
            else:
                self._log_message("❌ Failed to start server")
        except Exception as e:
            self._log_message(f"❌ Error starting server: {str(e)}")
            messagebox.showerror("Error", f"Failed to start server: {str(e)}")
    
    def _stop_server(self):
        """Stop the server"""
        try:
            if self.server_engine.stop_server():
                self.status_label.configure(text="Server: Stopped", text_color="red")
                self.server_url_label.configure(text="")
                
                self.start_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
                
                # Stop performance monitoring update
                self._stop_performance_updates()
                
                self._log_message("🛑 Server stopped")
            else:
                self._log_message("❌ Failed to stop server")
        except Exception as e:
            self._log_message(f"❌ Error stopping server: {str(e)}")
    
    def _start_performance_updates(self):
        """Start periodic performance updates"""
        self.performance_update_running = True
        
        def update_loop():
            while self.performance_update_running:
                try:
                    if self.server_engine.is_running:
                        # Update performance tab
                        metrics = self.server_engine.get_performance_data()
                        self.performance_tab.update_metrics(metrics)
                        
                        # Update request inspector
                        requests = self.server_engine.get_request_history()
                        self.request_inspector_tab.update_requests(requests)
                    
                    time.sleep(1.0)
                except Exception as e:
                    print(f"Performance update error: {e}")
                    break
        
        self.performance_thread = threading.Thread(target=update_loop, daemon=True)
        self.performance_thread.start()
    
    def _stop_performance_updates(self):
        """Stop performance updates"""
        self.performance_update_running = False
    
    def _log_message(self, message: str):
        """Log a message to the status bar and logs tab"""
        # Update status bar
        self.status_bar.configure(text=message)
        
        # Add to logs tab
        if hasattr(self, 'logs_tab'):
            self.logs_tab.add_log_entry(message)
    
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()
        
        # Cleanup on exit
        if self.server_engine and self.server_engine.is_running:
            self.server_engine.stop_server()
    
    def on_closing(self):
        """Handle window closing"""
        if self.server_engine and self.server_engine.is_running:
            if messagebox.askokcancel("Quit", "Server is running. Stop server and quit?"):
                self.server_engine.stop_server()
                self.root.destroy()
        else:
            self.root.destroy() 