#!/usr/bin/env python3
"""
SimuServer - Universal API Simulation Tool
Created by: QumPlus
A lightweight, modern server simulator for testing and development
"""

import sys
import os
import threading
import customtkinter as ctk
from pathlib import Path

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from gui.main_window import SimuServerGUI
from core.config import Config

def main():
    """Main entry point for SimuServer"""
    # Set appearance mode and theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Initialize configuration
    config = Config()
    
    # Create and run the GUI
    app = SimuServerGUI(config)
    app.run()

if __name__ == "__main__":
    main() 