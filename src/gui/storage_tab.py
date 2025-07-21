"""
Storage settings tab for SimuServer GUI
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import os
import shutil
from pathlib import Path
import sys

class StorageTab:
    """Storage settings tab for managing data directory and file operations"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        
        # Configure grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(2, weight=1)
        
        self._create_widgets()
        self._update_directory_info()
    
    def _create_widgets(self):
        """Create storage settings widgets"""
        
        # Header
        header_frame = ctk.CTkFrame(self.parent)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame, 
            text="Storage Settings", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        # Directory selection frame
        dir_frame = ctk.CTkFrame(self.parent)
        dir_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        dir_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(dir_frame, text="Data Directory:", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        
        self.directory_var = ctk.StringVar(value=self.config.get("storage.data_directory"))
        self.directory_entry = ctk.CTkEntry(
            dir_frame,
            textvariable=self.directory_var,
            state="readonly",
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.directory_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5))
        
        # Directory control buttons
        button_frame = ctk.CTkFrame(dir_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        self.browse_button = ctk.CTkButton(
            button_frame,
            text="Browse",
            command=self._browse_directory,
            width=100
        )
        self.browse_button.pack(side="left", padx=5)
        
        self.create_button = ctk.CTkButton(
            button_frame,
            text="Create Directory",
            command=self._create_directory,
            width=120
        )
        self.create_button.pack(side="left", padx=5)
        
        self.open_button = ctk.CTkButton(
            button_frame,
            text="Open in Explorer",
            command=self._open_directory,
            width=130
        )
        self.open_button.pack(side="left", padx=5)
        
        self.reset_button = ctk.CTkButton(
            button_frame,
            text="Reset to Default",
            command=self._reset_directory,
            width=120
        )
        self.reset_button.pack(side="right", padx=5)
        
        # Directory information frame
        info_frame = ctk.CTkFrame(self.parent)
        info_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)
        info_frame.grid_rowconfigure(1, weight=1)
        
        # Info header
        ctk.CTkLabel(
            info_frame, 
            text="Directory Information & Management", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Left column - Directory info
        left_info = ctk.CTkFrame(info_frame)
        left_info.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(0, 10))
        
        ctk.CTkLabel(left_info, text="Directory Status", font=ctk.CTkFont(size=14, weight="bold")).pack(
            anchor="w", padx=10, pady=(10, 5)
        )
        
        self.exists_label = ctk.CTkLabel(left_info, text="Exists: -")
        self.exists_label.pack(anchor="w", padx=20, pady=2)
        
        self.size_label = ctk.CTkLabel(left_info, text="Size: -")
        self.size_label.pack(anchor="w", padx=20, pady=2)
        
        self.files_count_label = ctk.CTkLabel(left_info, text="Files: -")
        self.files_count_label.pack(anchor="w", padx=20, pady=2)
        
        self.permissions_label = ctk.CTkLabel(left_info, text="Writable: -")
        self.permissions_label.pack(anchor="w", padx=20, pady=2)
        
        # Storage settings
        ctk.CTkLabel(left_info, text="Storage Settings", font=ctk.CTkFont(size=14, weight="bold")).pack(
            anchor="w", padx=10, pady=(20, 5)
        )
        
        # Max file size setting
        size_frame = ctk.CTkFrame(left_info)
        size_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(size_frame, text="Max File Size (MB):").pack(anchor="w", padx=10, pady=2)
        
        self.max_size_var = ctk.StringVar(value=str(self.config.get("storage.max_file_size_mb", 100)))
        self.max_size_entry = ctk.CTkEntry(size_frame, textvariable=self.max_size_var, width=100)
        self.max_size_entry.pack(anchor="w", padx=10, pady=2)
        
        # Auto-create setting
        self.auto_create_var = ctk.BooleanVar(value=self.config.get("storage.auto_create", True))
        self.auto_create_checkbox = ctk.CTkCheckBox(
            left_info,
            text="Auto-create directory if it doesn't exist",
            variable=self.auto_create_var,
            command=self._save_settings
        )
        self.auto_create_checkbox.pack(anchor="w", padx=20, pady=10)
        
        # Right column - File management
        right_info = ctk.CTkFrame(info_frame)
        right_info.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))
        
        ctk.CTkLabel(right_info, text="File Management", font=ctk.CTkFont(size=14, weight="bold")).pack(
            anchor="w", padx=10, pady=(10, 5)
        )
        
        # File list
        self.file_list = ctk.CTkScrollableFrame(right_info, height=200)
        self.file_list.pack(fill="both", expand=True, padx=10, pady=5)
        
        # File management buttons
        file_button_frame = ctk.CTkFrame(right_info)
        file_button_frame.pack(fill="x", padx=10, pady=10)
        
        self.refresh_files_button = ctk.CTkButton(
            file_button_frame,
            text="Refresh",
            command=self._refresh_files,
            width=80
        )
        self.refresh_files_button.pack(side="left", padx=5)
        
        self.clean_button = ctk.CTkButton(
            file_button_frame,
            text="Clean Temp Files",
            command=self._clean_temp_files,
            width=120
        )
        self.clean_button.pack(side="left", padx=5)
        
        self.backup_button = ctk.CTkButton(
            file_button_frame,
            text="Backup Data",
            command=self._backup_data,
            width=100
        )
        self.backup_button.pack(side="right", padx=5)
        
        # Settings buttons
        settings_frame = ctk.CTkFrame(info_frame)
        settings_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        self.save_settings_button = ctk.CTkButton(
            settings_frame,
            text="Save Settings",
            command=self._save_settings,
            width=120
        )
        self.save_settings_button.pack(side="left", padx=10, pady=10)
        
        self.update_info_button = ctk.CTkButton(
            settings_frame,
            text="Update Info",
            command=self._update_directory_info,
            width=100
        )
        self.update_info_button.pack(side="left", padx=10, pady=10)
    
    def _browse_directory(self):
        """Browse for a new data directory"""
        directory = filedialog.askdirectory(
            title="Select Data Directory",
            initialdir=self.directory_var.get()
        )
        
        if directory:
            self.directory_var.set(directory)
            self.config.set("storage.data_directory", directory)
            self._update_directory_info()
    
    def _create_directory(self):
        """Create the data directory"""
        directory = Path(self.directory_var.get())
        
        try:
            directory.mkdir(parents=True, exist_ok=True)
            self._update_directory_info()
            messagebox.showinfo("Success", f"Directory created: {directory}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create directory: {str(e)}")
    
    def _open_directory(self):
        """Open the data directory in file explorer"""
        directory = self.directory_var.get()
        
        if not os.path.exists(directory):
            messagebox.showwarning("Warning", "Directory does not exist")
            return
        
        try:
            if os.name == 'nt':  # Windows
                os.startfile(directory)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{directory}"' if sys.platform == 'darwin' else f'xdg-open "{directory}"')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open directory: {str(e)}")
    
    def _reset_directory(self):
        """Reset to default directory"""
        default_dir = str(Path.home() / "SimuServer_Data")
        self.directory_var.set(default_dir)
        self.config.set("storage.data_directory", default_dir)
        self._update_directory_info()
    
    def _update_directory_info(self):
        """Update directory information display"""
        directory = Path(self.directory_var.get())
        
        # Check if directory exists
        exists = directory.exists()
        self.exists_label.configure(
            text=f"Exists: {'Yes' if exists else 'No'}",
            text_color="green" if exists else "red"
        )
        
        if exists:
            try:
                # Calculate directory size
                total_size = sum(f.stat().st_size for f in directory.rglob('*') if f.is_file())
                size_str = self._format_bytes(total_size)
                self.size_label.configure(text=f"Size: {size_str}")
                
                # Count files
                file_count = len([f for f in directory.rglob('*') if f.is_file()])
                self.files_count_label.configure(text=f"Files: {file_count}")
                
                # Check permissions
                writable = os.access(directory, os.W_OK)
                self.permissions_label.configure(
                    text=f"Writable: {'Yes' if writable else 'No'}",
                    text_color="green" if writable else "red"
                )
                
            except Exception as e:
                self.size_label.configure(text="Size: Error")
                self.files_count_label.configure(text="Files: Error")
                self.permissions_label.configure(text="Writable: Error")
        else:
            self.size_label.configure(text="Size: -")
            self.files_count_label.configure(text="Files: -")
            self.permissions_label.configure(text="Writable: -")
        
        # Update file list
        self._refresh_files()
    
    def _refresh_files(self):
        """Refresh the file list"""
        # Clear existing widgets
        for widget in self.file_list.winfo_children():
            widget.destroy()
        
        directory = Path(self.directory_var.get())
        
        if not directory.exists():
            ctk.CTkLabel(self.file_list, text="Directory does not exist").pack(pady=10)
            return
        
        try:
            files = list(directory.rglob('*'))[:20]  # Limit to first 20 files
            
            if not files:
                ctk.CTkLabel(self.file_list, text="No files found").pack(pady=10)
                return
            
            for file_path in files:
                if file_path.is_file():
                    file_frame = ctk.CTkFrame(self.file_list)
                    file_frame.pack(fill="x", padx=5, pady=2)
                    
                    # File name
                    relative_path = file_path.relative_to(directory)
                    ctk.CTkLabel(
                        file_frame, 
                        text=str(relative_path), 
                        font=ctk.CTkFont(family="Consolas", size=10)
                    ).pack(side="left", padx=5, pady=2)
                    
                    # File size
                    size = self._format_bytes(file_path.stat().st_size)
                    ctk.CTkLabel(
                        file_frame, 
                        text=size, 
                        font=ctk.CTkFont(size=10)
                    ).pack(side="right", padx=5, pady=2)
            
            if len(list(directory.rglob('*'))) > 20:
                ctk.CTkLabel(
                    self.file_list, 
                    text="... (showing first 20 files)",
                    font=ctk.CTkFont(style="italic")
                ).pack(pady=5)
                
        except Exception as e:
            ctk.CTkLabel(self.file_list, text=f"Error reading files: {str(e)}").pack(pady=10)
    
    def _clean_temp_files(self):
        """Clean temporary files from the data directory"""
        directory = Path(self.directory_var.get())
        
        if not directory.exists():
            messagebox.showwarning("Warning", "Directory does not exist")
            return
        
        if messagebox.askyesno("Confirm", "Clean temporary files (*.tmp, *.temp, *.log)?"):
            try:
                deleted_count = 0
                for pattern in ['*.tmp', '*.temp', '*.log']:
                    for file_path in directory.rglob(pattern):
                        file_path.unlink()
                        deleted_count += 1
                
                messagebox.showinfo("Success", f"Deleted {deleted_count} temporary files")
                self._update_directory_info()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clean files: {str(e)}")
    
    def _backup_data(self):
        """Create a backup of the data directory"""
        source_dir = Path(self.directory_var.get())
        
        if not source_dir.exists():
            messagebox.showwarning("Warning", "Directory does not exist")
            return
        
        backup_path = filedialog.asksaveasfilename(
            title="Save Backup As",
            defaultextension=".zip",
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
        )
        
        if backup_path:
            try:
                # Create backup (simplified - would need proper zip implementation)
                messagebox.showinfo("Info", "Backup functionality would be implemented here")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create backup: {str(e)}")
    
    def _save_settings(self):
        """Save storage settings"""
        try:
            max_size = int(self.max_size_var.get())
            self.config.set("storage.max_file_size_mb", max_size)
            self.config.set("storage.auto_create", self.auto_create_var.get())
            
            messagebox.showinfo("Success", "Settings saved successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid max file size value")
    
    def _format_bytes(self, bytes_value):
        """Format bytes in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} TB" 