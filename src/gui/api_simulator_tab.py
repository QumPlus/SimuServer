"""
API Simulator tab for SimuServer GUI
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
import json
from pathlib import Path

from ..templates.template_manager import TemplateManager

class APISimulatorTab:
    """API Simulator tab for managing and loading API templates"""
    
    def __init__(self, parent, config, log_callback):
        self.parent = parent
        self.config = config
        self.log_callback = log_callback
        self.server_engine = None
        
        # Template manager
        self.template_manager = TemplateManager()
        
        # Configure grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        
        self._create_widgets()
        self._load_available_templates()
    
    def _create_widgets(self):
        """Create tab widgets"""
        
        # Header frame
        header_frame = ctk.CTkFrame(self.parent)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Template selection
        ctk.CTkLabel(header_frame, text="Select API Template:", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        
        self.template_var = ctk.StringVar()
        self.template_dropdown = ctk.CTkComboBox(
            header_frame,
            variable=self.template_var,
            command=self._on_template_selected,
            width=200
        )
        self.template_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Load template button
        self.load_button = ctk.CTkButton(
            header_frame,
            text="Load Template",
            command=self._load_selected_template,
            width=120
        )
        self.load_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Custom template button
        self.custom_button = ctk.CTkButton(
            header_frame,
            text="Load Custom",
            command=self._load_custom_template,
            width=120
        )
        self.custom_button.grid(row=0, column=3, padx=10, pady=10)
        
        # Main content frame
        content_frame = ctk.CTkFrame(self.parent)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Template info
        info_frame = ctk.CTkFrame(content_frame)
        info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        info_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(info_frame, text="Template Info:", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        
        self.template_info = ctk.CTkTextbox(info_frame, height=80)
        self.template_info.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        
        # Active templates frame
        active_frame = ctk.CTkFrame(content_frame)
        active_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        active_frame.grid_columnconfigure(0, weight=1)
        active_frame.grid_rowconfigure(1, weight=1)
        
        # Active templates header
        active_header = ctk.CTkFrame(active_frame)
        active_header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        active_header.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(active_header, text="Active Templates", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        
        # Clear all button
        self.clear_button = ctk.CTkButton(
            active_header,
            text="Clear All",
            command=self._clear_all_templates,
            width=100
        )
        self.clear_button.grid(row=0, column=1, padx=10, pady=5)
        
        # Active templates list
        self.active_list = ctk.CTkScrollableFrame(active_frame)
        self.active_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Configuration frame
        config_frame = ctk.CTkFrame(content_frame)
        config_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        config_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(config_frame, text="Simulation Settings:", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w"
        )
        
        # Delay setting
        ctk.CTkLabel(config_frame, text="Response Delay (ms):").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        
        self.delay_entry = ctk.CTkEntry(config_frame, width=100)
        self.delay_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.delay_entry.insert(0, str(self.config.get("simulation.default_delay_ms", 0)))
        
        # Error rate setting
        ctk.CTkLabel(config_frame, text="Error Rate (0.0-1.0):").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        
        self.error_rate_entry = ctk.CTkEntry(config_frame, width=100)
        self.error_rate_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.error_rate_entry.insert(0, str(self.config.get("simulation.error_rate", 0.0)))
        
        # Apply settings button
        self.apply_settings_button = ctk.CTkButton(
            config_frame,
            text="Apply Settings",
            command=self._apply_settings,
            width=120
        )
        self.apply_settings_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    
    def _load_available_templates(self):
        """Load available templates into dropdown"""
        templates = self.template_manager.get_available_templates()
        template_names = [name for name, _ in templates]
        
        if template_names:
            self.template_dropdown.configure(values=template_names)
            self.template_dropdown.set(template_names[0])
            self._on_template_selected(template_names[0])
        else:
            self.template_dropdown.configure(values=["No templates available"])
    
    def _on_template_selected(self, template_name):
        """Handle template selection"""
        template_data = self.template_manager.get_template(template_name)
        if template_data:
            info_text = f"Name: {template_data.get('name', 'Unknown')}\n"
            info_text += f"Description: {template_data.get('description', 'No description')}\n"
            info_text += f"Version: {template_data.get('version', '1.0')}\n"
            info_text += f"Routes: {len(template_data.get('routes', []))}"
            
            self.template_info.delete("1.0", tk.END)
            self.template_info.insert("1.0", info_text)
    
    def _load_selected_template(self):
        """Load the selected template"""
        template_name = self.template_var.get()
        if not template_name or template_name == "No templates available":
            messagebox.showwarning("Warning", "Please select a valid template")
            return
        
        if not self.server_engine:
            messagebox.showwarning("Warning", "Server engine not initialized")
            return
        
        template_data = self.template_manager.get_template(template_name)
        if template_data:
            self.server_engine.load_template(template_name, template_data)
            self._update_active_templates()
            self.log_callback(f"📋 Loaded template: {template_name}")
        else:
            messagebox.showerror("Error", f"Failed to load template: {template_name}")
    
    def _load_custom_template(self):
        """Load a custom template from file"""
        file_path = filedialog.askopenfilename(
            title="Select Template File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r') as f:
                template_data = json.load(f)
            
            template_name = template_data.get('name', Path(file_path).stem)
            
            if self.server_engine:
                self.server_engine.load_template(template_name, template_data)
                self._update_active_templates()
                self.log_callback(f"📂 Loaded custom template: {template_name}")
            else:
                messagebox.showwarning("Warning", "Server engine not initialized")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load custom template: {str(e)}")
    
    def _clear_all_templates(self):
        """Clear all active templates"""
        if messagebox.askyesno("Confirm", "Clear all active templates?"):
            # This would require server restart in a real implementation
            # For now, just clear the display
            for widget in self.active_list.winfo_children():
                widget.destroy()
            
            self.log_callback("🗑️ All templates cleared (restart server to apply)")
    
    def _update_active_templates(self):
        """Update the active templates display"""
        # Clear existing widgets
        for widget in self.active_list.winfo_children():
            widget.destroy()
        
        if self.server_engine:
            active_templates = self.server_engine.active_templates
            
            for i, template_name in enumerate(active_templates):
                template_frame = ctk.CTkFrame(self.active_list)
                template_frame.grid(row=i, column=0, sticky="ew", padx=5, pady=2)
                template_frame.grid_columnconfigure(0, weight=1)
                
                ctk.CTkLabel(template_frame, text=template_name, font=ctk.CTkFont(weight="bold")).grid(
                    row=0, column=0, padx=10, pady=5, sticky="w"
                )
                
                # Status indicator
                status_label = ctk.CTkLabel(template_frame, text="🟢 Active", text_color="green")
                status_label.grid(row=0, column=1, padx=10, pady=5)
    
    def _apply_settings(self):
        """Apply simulation settings"""
        try:
            delay = int(self.delay_entry.get())
            error_rate = float(self.error_rate_entry.get())
            
            if error_rate < 0.0 or error_rate > 1.0:
                raise ValueError("Error rate must be between 0.0 and 1.0")
            
            self.config.set("simulation.default_delay_ms", delay)
            self.config.set("simulation.error_rate", error_rate)
            
            self.log_callback(f"⚙️ Settings applied: {delay}ms delay, {error_rate} error rate")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid settings: {str(e)}")
    
    def set_server_engine(self, server_engine):
        """Set the server engine reference"""
        self.server_engine = server_engine 