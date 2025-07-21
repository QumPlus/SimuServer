"""
Logs tab for SimuServer GUI
"""

import tkinter as tk
import customtkinter as ctk
from datetime import datetime
from typing import List

class LogsTab:
    """Logs tab for displaying server and application logs"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.log_entries: List[str] = []
        self.max_entries = config.get("logging.max_entries", 1000)
        self.auto_scroll = config.get("logging.auto_scroll", True)
        
        # Configure grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create log display widgets"""
        
        # Header frame
        header_frame = ctk.CTkFrame(self.parent)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            header_frame, 
            text="Server Logs", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, padx=10, pady=10)
        
        # Control buttons
        button_frame = ctk.CTkFrame(header_frame)
        button_frame.grid(row=0, column=1, sticky="e", padx=10, pady=10)
        
        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear Logs",
            command=self._clear_logs,
            width=100
        )
        self.clear_button.pack(side="left", padx=5)
        
        self.save_button = ctk.CTkButton(
            button_frame,
            text="Save to File",
            command=self._save_logs,
            width=100
        )
        self.save_button.pack(side="left", padx=5)
        
        self.auto_scroll_var = ctk.BooleanVar(value=self.auto_scroll)
        self.auto_scroll_checkbox = ctk.CTkCheckBox(
            button_frame,
            text="Auto-scroll",
            variable=self.auto_scroll_var,
            command=self._toggle_auto_scroll
        )
        self.auto_scroll_checkbox.pack(side="left", padx=10)
        
        # Log display frame
        log_frame = ctk.CTkFrame(self.parent)
        log_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(0, weight=1)
        
        # Text widget for logs
        self.log_text = ctk.CTkTextbox(
            log_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="word"
        )
        self.log_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Status frame
        status_frame = ctk.CTkFrame(self.parent)
        status_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        status_frame.grid_columnconfigure(1, weight=1)
        
        self.entry_count_label = ctk.CTkLabel(status_frame, text="Entries: 0")
        self.entry_count_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.filter_entry = ctk.CTkEntry(
            status_frame,
            placeholder_text="Filter logs...",
            width=200
        )
        self.filter_entry.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        self.filter_entry.bind("<KeyRelease>", self._filter_logs)
        
        # Add initial welcome message
        self.add_log_entry("🚀 SimuServer logging started")
        self.add_log_entry("ℹ️ Ready to start server simulation")
    
    def add_log_entry(self, message: str):
        """Add a new log entry"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        # Add to internal list
        self.log_entries.append(log_entry)
        
        # Limit entries
        if len(self.log_entries) > self.max_entries:
            self.log_entries = self.log_entries[-self.max_entries:]
            self._refresh_display()
        else:
            # Just append to display
            self.log_text.insert("end", log_entry + "\n")
            
            # Auto-scroll if enabled
            if self.auto_scroll:
                self.log_text.see("end")
        
        # Update entry count
        self._update_entry_count()
    
    def _refresh_display(self):
        """Refresh the entire log display"""
        filter_text = self.filter_entry.get().lower()
        
        # Clear display
        self.log_text.delete("1.0", "end")
        
        # Add filtered entries
        for entry in self.log_entries:
            if not filter_text or filter_text in entry.lower():
                self.log_text.insert("end", entry + "\n")
        
        # Auto-scroll if enabled
        if self.auto_scroll:
            self.log_text.see("end")
    
    def _filter_logs(self, event=None):
        """Filter logs based on search text"""
        self._refresh_display()
    
    def _clear_logs(self):
        """Clear all log entries"""
        self.log_entries.clear()
        self.log_text.delete("1.0", "end")
        self._update_entry_count()
        
        # Add cleared message
        self.add_log_entry("🗑️ Logs cleared")
    
    def _save_logs(self):
        """Save logs to file"""
        try:
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                title="Save Logs",
                defaultextension=".log",
                filetypes=[
                    ("Log files", "*.log"),
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("\n".join(self.log_entries))
                
                self.add_log_entry(f"💾 Logs saved to {filename}")
                
        except Exception as e:
            self.add_log_entry(f"❌ Error saving logs: {str(e)}")
    
    def _toggle_auto_scroll(self):
        """Toggle auto-scroll setting"""
        self.auto_scroll = self.auto_scroll_var.get()
        self.config.set("logging.auto_scroll", self.auto_scroll)
    
    def _update_entry_count(self):
        """Update the entry count display"""
        count = len(self.log_entries)
        self.entry_count_label.configure(text=f"Entries: {count}")
    
    def get_logs(self) -> List[str]:
        """Get all log entries"""
        return self.log_entries.copy()
    
    def clear_logs(self):
        """Public method to clear logs"""
        self._clear_logs() 