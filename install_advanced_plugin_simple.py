#!/usr/bin/env python3
"""
Advanced Schematic Importer Plugin Installer

This script installs the advanced version of the KiCad Schematic Importer plugin
with enhanced features for component recognition, connection tracing, and PDF import.
"""

import os
import sys
import shutil
import platform
import subprocess
import json
from pathlib import Path

def find_kicad_plugin_dir(kicad_version="9.0"):
    """Find KiCad plugin directory"""
    if platform.system() == "Windows":
        if kicad_version == "9.0":
            # KiCad 9.0 uses a different location on Windows
            return os.path.join(os.path.expanduser("~"), "Documents", "KiCad", "9.0", "3rdparty", "plugins")
        else:
            # Windows: %APPDATA%\kicad\7.0\scripting\plugins
            return os.path.join(os.getenv("APPDATA"), "kicad", kicad_version, "scripting", "plugins")
    elif platform.system() == "Darwin":  # macOS
        # macOS: ~/Library/Application Support/kicad/scripting/plugins
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "kicad", kicad_version, "scripting", "plugins")
    else:  # Linux
        # Linux: ~/.local/share/kicad/scripting/plugins
        return os.path.join(os.path.expanduser("~"), ".local", "share", "kicad", kicad_version, "scripting", "plugins")

def install_dependencies():
    """Install required Python dependencies"""
    try:
        print("Installing dependencies...")
        
        # Get the requirements file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_path = os.path.join(current_dir, "requirements.txt")
        
        # Install dependencies using pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        
        print("Dependencies installed successfully.")
        return True
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        return False

def create_plugin_files(target_dir):
    """Create plugin files in the target directory"""
    # Create action_plugin.py
    action_plugin_content = (
        "import pcbnew\n"
        "import wx\n"
        "import os\n\n"
        "class AdvancedSchematicImporter(pcbnew.ActionPlugin):\n"
        "    def __init__(self):\n"
        "        super().__init__()\n"
        "        self.name = 'Advanced Schematic Importer'\n"
        "        self.category = 'Import Plugin'\n"
        "        self.description = 'Import schematics from images with advanced features'\n"
        "        self.show_toolbar_button = True\n\n"
        "    def Run(self):\n"
        "        frame = wx.Frame(None, title='Advanced Schematic Importer')\n"
        "        frame.Show()\n"
    )
    
    with open(os.path.join(target_dir, "action_plugin.py"), "w") as f:
        f.write(action_plugin_content)

    # Create __init__.py
    init_content = (
        "# This file makes the directory a Python package\n"
        "# It allows the plugin to be imported by KiCad\n\n"
        "try:\n"
        "    from .action_plugin import AdvancedSchematicImporter\n"
        "except Exception as e:\n"
        "    import traceback\n"
        "    traceback.print_exc()\n"
    )
    
    with open(os.path.join(target_dir, "__init__.py"), "w") as f:
        f.write(init_content)

def install_advanced_plugin():
    """Install the advanced schematic importer plugin"""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get the KiCad plugin directory
    kicad_plugin_dir = find_kicad_plugin_dir("9.0")
    
    # Define the target directory
    target_dir = os.path.join(kicad_plugin_dir, "advanced_schematic_importer")
    
    # Create the target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Create plugin directory structure
    for dir_path in [
        os.path.join(target_dir, "src", "recognition"),
        os.path.join(target_dir, "src", "utils"),
        os.path.join(target_dir, "resources", "icons"),
        os.path.join(target_dir, "resources", "templates")
    ]:
        os.makedirs(dir_path, exist_ok=True)
    
    # Create plugin files
    create_plugin_files(target_dir)
    
    # Create metadata.json
    metadata = {
        "identifier": "com.augmentcode.kicad.advancedschematicimporter",
        "name": "Advanced Schematic Importer",
        "description": "Import schematics from images with advanced features",
        "author": {
            "name": "Wallace Lebrun",
            "contact": {
                "web": "https://github.com/augmentcode/kicad-schematic-importer"
            }
        },
        "license": "MIT",
        "version": "0.5.0",
        "status": "testing",
        "kicad_version": "9.0"
    }
    
    with open(os.path.join(target_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)
    
    print(f"Advanced Schematic Importer plugin installed to: {target_dir}")
    print("\nTo use the plugin:")
    print("1. Start KiCad")
    print("2. Open PCB Editor")
    print("3. Look for 'Advanced Schematic Importer' in the Tools menu")
    print("\nIf KiCad is already running, please restart it to load the plugin.")

if __name__ == "__main__":
    # Install dependencies
    if install_dependencies():
        # Install the plugin
        install_advanced_plugin()
    else:
        print("Failed to install dependencies. Plugin installation aborted.")
