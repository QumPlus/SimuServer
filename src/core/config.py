"""
Configuration management for SimuServer
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Configuration manager for SimuServer"""
    
    def __init__(self, config_file: str = "simuserver_config.json"):
        self.config_file = Path(config_file)
        self.data = self._load_default_config()
        self.load()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            "server": {
                "host": "127.0.0.1",
                "port": 8000,
                "auto_start": False,
                "enable_websockets": True
            },
            "storage": {
                "data_directory": str(Path.home() / "SimuServer_Data"),
                "auto_create": True,
                "max_file_size_mb": 100
            },
            "performance": {
                "update_interval": 1.0,
                "history_size": 100
            },
            "gui": {
                "theme": "dark",
                "window_size": "1200x800",
                "remember_position": True
            },
            "logging": {
                "level": "INFO",
                "max_entries": 1000,
                "auto_scroll": True
            },
            "simulation": {
                "default_delay_ms": 0,
                "error_rate": 0.0,
                "enable_cors": True
            }
        }
    
    def load(self) -> None:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    file_data = json.load(f)
                    self.data.update(file_data)
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
    
    def save(self) -> None:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation"""
        keys = key.split('.')
        data = self.data
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        data[keys[-1]] = value
        self.save()
    
    def get_data_directory(self) -> Path:
        """Get the configured data directory"""
        path = Path(self.get("storage.data_directory"))
        if self.get("storage.auto_create") and not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        return path 