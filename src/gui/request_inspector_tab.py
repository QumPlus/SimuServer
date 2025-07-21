"""
Request Inspector tab for SimuServer GUI
"""

import tkinter as tk
import customtkinter as ctk
import json
from datetime import datetime
from typing import List, Dict, Any

class RequestInspectorTab:
    """Request Inspector tab for viewing and analyzing API requests/responses"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.server_engine = None
        self.requests_data: List[Dict[str, Any]] = []
        self.selected_request = None
        
        # Configure grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create request inspector widgets"""
        
        # Header frame
        header_frame = ctk.CTkFrame(self.parent)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            header_frame, 
            text="Request Inspector", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, padx=10, pady=10)
        
        # Control buttons
        button_frame = ctk.CTkFrame(header_frame)
        button_frame.grid(row=0, column=1, sticky="e", padx=10, pady=10)
        
        self.refresh_button = ctk.CTkButton(
            button_frame,
            text="Refresh",
            command=self._refresh_requests,
            width=80
        )
        self.refresh_button.pack(side="left", padx=5)
        
        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self._clear_requests,
            width=80
        )
        self.clear_button.pack(side="left", padx=5)
        
        self.export_button = ctk.CTkButton(
            button_frame,
            text="Export",
            command=self._export_requests,
            width=80
        )
        self.export_button.pack(side="left", padx=5)
        
        # Main content frame with splitter
        content_frame = ctk.CTkFrame(self.parent)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel - Request list
        left_panel = ctk.CTkFrame(content_frame)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(1, weight=1)
        
        # Request list header
        list_header = ctk.CTkFrame(left_panel)
        list_header.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        list_header.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(list_header, text="Recent Requests", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        
        # Filter frame
        filter_frame = ctk.CTkFrame(list_header)
        filter_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        filter_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(filter_frame, text="Filter:").grid(row=0, column=0, padx=5, pady=2)
        
        self.filter_var = ctk.StringVar()
        self.filter_entry = ctk.CTkEntry(filter_frame, textvariable=self.filter_var, placeholder_text="Method, URL, Status...")
        self.filter_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.filter_entry.bind("<KeyRelease>", self._filter_requests)
        
        # Method filter
        method_frame = ctk.CTkFrame(filter_frame)
        method_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=2)
        
        self.method_var = ctk.StringVar(value="All")
        self.method_dropdown = ctk.CTkComboBox(
            method_frame,
            variable=self.method_var,
            values=["All", "GET", "POST", "PUT", "DELETE", "PATCH"],
            command=self._filter_requests,
            width=80
        )
        self.method_dropdown.pack(side="left", padx=2)
        
        self.status_var = ctk.StringVar(value="All")
        self.status_dropdown = ctk.CTkComboBox(
            method_frame,
            variable=self.status_var,
            values=["All", "2xx", "3xx", "4xx", "5xx"],
            command=self._filter_requests,
            width=80
        )
        self.status_dropdown.pack(side="left", padx=2)
        
        # Request list
        self.request_list = ctk.CTkScrollableFrame(left_panel)
        self.request_list.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Right panel - Request details
        right_panel = ctk.CTkFrame(content_frame)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)
        
        # Details header
        details_header = ctk.CTkFrame(right_panel)
        details_header.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        self.details_title = ctk.CTkLabel(
            details_header, 
            text="Request Details", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.details_title.pack(padx=10, pady=5)
        
        # Details content with tabs
        self.details_tabview = ctk.CTkTabview(right_panel)
        self.details_tabview.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Overview tab
        overview_tab = self.details_tabview.add("Overview")
        self.overview_text = ctk.CTkTextbox(overview_tab, font=ctk.CTkFont(family="Consolas", size=11))
        self.overview_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Headers tab
        headers_tab = self.details_tabview.add("Headers")
        self.headers_text = ctk.CTkTextbox(headers_tab, font=ctk.CTkFont(family="Consolas", size=11))
        self.headers_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Body tab
        body_tab = self.details_tabview.add("Body")
        self.body_text = ctk.CTkTextbox(body_tab, font=ctk.CTkFont(family="Consolas", size=11))
        self.body_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Response tab
        response_tab = self.details_tabview.add("Response")
        self.response_text = ctk.CTkTextbox(response_tab, font=ctk.CTkFont(family="Consolas", size=11))
        self.response_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Status frame
        status_frame = ctk.CTkFrame(self.parent)
        status_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        status_frame.grid_columnconfigure(1, weight=1)
        
        self.request_count_label = ctk.CTkLabel(status_frame, text="Requests: 0")
        self.request_count_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.selected_info_label = ctk.CTkLabel(status_frame, text="No request selected")
        self.selected_info_label.grid(row=0, column=1, padx=10, pady=5, sticky="e")
    
    def update_requests(self, requests: List[Dict[str, Any]]):
        """Update the requests list"""
        self.requests_data = requests
        self._display_requests()
        self._update_request_count()
    
    def _display_requests(self):
        """Display requests in the list"""
        # Clear existing widgets
        for widget in self.request_list.winfo_children():
            widget.destroy()
        
        # Apply filters
        filtered_requests = self._get_filtered_requests()
        
        # Display requests
        for i, request in enumerate(filtered_requests[-50:]):  # Show last 50
            self._create_request_item(i, request)
    
    def _get_filtered_requests(self) -> List[Dict[str, Any]]:
        """Get filtered requests based on current filters"""
        requests = self.requests_data
        
        # Filter by search text
        filter_text = self.filter_var.get().lower()
        if filter_text:
            requests = [
                req for req in requests
                if (filter_text in req.get("method", "").lower() or
                    filter_text in req.get("url", "").lower() or
                    filter_text in str(req.get("status_code", "")))
            ]
        
        # Filter by method
        method_filter = self.method_var.get()
        if method_filter != "All":
            requests = [req for req in requests if req.get("method", "").upper() == method_filter]
        
        # Filter by status
        status_filter = self.status_var.get()
        if status_filter != "All":
            if status_filter == "2xx":
                requests = [req for req in requests if 200 <= req.get("status_code", 0) < 300]
            elif status_filter == "3xx":
                requests = [req for req in requests if 300 <= req.get("status_code", 0) < 400]
            elif status_filter == "4xx":
                requests = [req for req in requests if 400 <= req.get("status_code", 0) < 500]
            elif status_filter == "5xx":
                requests = [req for req in requests if 500 <= req.get("status_code", 0) < 600]
        
        return requests
    
    def _create_request_item(self, index: int, request: Dict[str, Any]):
        """Create a request item widget"""
        item_frame = ctk.CTkFrame(self.request_list)
        item_frame.pack(fill="x", padx=2, pady=2)
        item_frame.grid_columnconfigure(1, weight=1)
        
        # Status color
        status_code = request.get("status_code", 0)
        if 200 <= status_code < 300:
            status_color = "green"
        elif 300 <= status_code < 400:
            status_color = "orange"
        elif 400 <= status_code < 500:
            status_color = "red"
        elif 500 <= status_code < 600:
            status_color = "darkred"
        else:
            status_color = "gray"
        
        # Method and status
        method_status = f"{request.get('method', 'GET')} {status_code}"
        ctk.CTkLabel(
            item_frame, 
            text=method_status, 
            font=ctk.CTkFont(weight="bold"),
            text_color=status_color,
            width=80
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        # URL (truncated)
        url = request.get("url", "")
        if len(url) > 40:
            url = url[:37] + "..."
        
        url_label = ctk.CTkLabel(
            item_frame, 
            text=url, 
            font=ctk.CTkFont(family="Consolas", size=10)
        )
        url_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Response time
        response_time = request.get("response_time_ms", 0)
        time_label = ctk.CTkLabel(
            item_frame, 
            text=f"{response_time}ms",
            font=ctk.CTkFont(size=10)
        )
        time_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        
        # Timestamp
        timestamp = request.get("timestamp", "")
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime("%H:%M:%S")
            except:
                time_str = timestamp[-8:]  # Last 8 chars
        else:
            time_str = ""
        
        time_label = ctk.CTkLabel(
            item_frame, 
            text=time_str,
            font=ctk.CTkFont(size=10)
        )
        time_label.grid(row=1, column=0, columnspan=3, padx=5, pady=(0, 5), sticky="e")
        
        # Click handler
        def on_click(event, req=request):
            self._select_request(req)
        
        # Bind click events
        item_frame.bind("<Button-1>", on_click)
        for child in item_frame.winfo_children():
            child.bind("<Button-1>", on_click)
    
    def _select_request(self, request: Dict[str, Any]):
        """Select and display request details"""
        self.selected_request = request
        self._display_request_details(request)
        
        # Update selected info
        method = request.get("method", "GET")
        url = request.get("url", "")
        status = request.get("status_code", 0)
        self.selected_info_label.configure(text=f"Selected: {method} {url} - {status}")
    
    def _display_request_details(self, request: Dict[str, Any]):
        """Display detailed request information"""
        # Overview tab
        overview = self._format_request_overview(request)
        self.overview_text.delete("1.0", "end")
        self.overview_text.insert("1.0", overview)
        
        # Headers tab
        headers = self._format_headers(request.get("headers", {}))
        self.headers_text.delete("1.0", "end")
        self.headers_text.insert("1.0", headers)
        
        # Body tab (if available)
        body = request.get("request_body", "No request body")
        self.body_text.delete("1.0", "end")
        self.body_text.insert("1.0", body or "No request body")
        
        # Response tab (if available)
        response = request.get("response_body", "No response body")
        self.response_text.delete("1.0", "end")
        self.response_text.insert("1.0", response or "No response body")
    
    def _format_request_overview(self, request: Dict[str, Any]) -> str:
        """Format request overview"""
        overview = f"Request ID: {request.get('id', 'N/A')}\n"
        overview += f"Method: {request.get('method', 'GET')}\n"
        overview += f"URL: {request.get('url', 'N/A')}\n"
        overview += f"Status Code: {request.get('status_code', 'N/A')}\n"
        overview += f"Response Time: {request.get('response_time_ms', 0)}ms\n"
        overview += f"Timestamp: {request.get('timestamp', 'N/A')}\n"
        
        return overview
    
    def _format_headers(self, headers: Dict[str, str]) -> str:
        """Format headers for display"""
        if not headers:
            return "No headers"
        
        formatted = ""
        for key, value in headers.items():
            formatted += f"{key}: {value}\n"
        
        return formatted
    
    def _filter_requests(self, event=None):
        """Apply filters and refresh display"""
        self._display_requests()
    
    def _refresh_requests(self):
        """Refresh requests from server"""
        if self.server_engine:
            requests = self.server_engine.get_request_history()
            self.update_requests(requests)
    
    def _clear_requests(self):
        """Clear all requests"""
        if self.server_engine and self.server_engine.request_logger:
            self.server_engine.request_logger.clear_logs()
        
        self.requests_data.clear()
        self._display_requests()
        self._update_request_count()
        
        # Clear details
        for textbox in [self.overview_text, self.headers_text, self.body_text, self.response_text]:
            textbox.delete("1.0", "end")
        
        self.selected_info_label.configure(text="No request selected")
    
    def _export_requests(self):
        """Export requests to file"""
        if not self.requests_data:
            tk.messagebox.showwarning("Warning", "No requests to export")
            return
        
        try:
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                title="Export Requests",
                defaultextension=".json",
                filetypes=[
                    ("JSON files", "*.json"),
                    ("CSV files", "*.csv"),
                    ("All files", "*.*")
                ]
            )
            
            if filename:
                if filename.endswith('.json'):
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(self.requests_data, f, indent=2)
                elif filename.endswith('.csv'):
                    # Would implement CSV export here
                    pass
                
                tk.messagebox.showinfo("Success", f"Requests exported to {filename}")
                
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to export requests: {str(e)}")
    
    def _update_request_count(self):
        """Update request count display"""
        count = len(self.requests_data)
        filtered_count = len(self._get_filtered_requests())
        
        if count == filtered_count:
            self.request_count_label.configure(text=f"Requests: {count}")
        else:
            self.request_count_label.configure(text=f"Requests: {filtered_count} / {count}")
    
    def set_server_engine(self, server_engine):
        """Set the server engine reference"""
        self.server_engine = server_engine 