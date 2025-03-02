#!/usr/bin/env python3
"""
Advanced Schematic Importer Plugin Installer
with enhanced error detection and debugging
"""

import os
import sys
import shutil
import platform
import subprocess
import json
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('plugin_install.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def detect_kicad_version():
    """Attempt to automatically detect installed KiCad version"""
    versions_to_check = ["7.0", "6.0", "5.0"]
    
    for version in versions_to_check:
        if platform.system() == "Windows":
            # Check Program Files
            program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
            kicad_path = os.path.join(program_files, "KiCad")
            if os.path.exists(os.path.join(kicad_path, version)):
                return version
            
            # Check AppData
            appdata_path = os.path.join(os.getenv("APPDATA"), "kicad", version)
            if os.path.exists(appdata_path):
                return version
                
        elif platform.system() == "Darwin":  # macOS
            app_support = os.path.expanduser("~/Library/Application Support/kicad")
            if os.path.exists(os.path.join(app_support, version)):
                return version
                
        elif platform.system() == "Linux":
            paths_to_check = [
                os.path.expanduser(f"~/.local/share/kicad/{version}"),
                f"/usr/share/kicad/{version}",
                f"/usr/local/share/kicad/{version}"
            ]
            for path in paths_to_check:
                if os.path.exists(path):
                    return version
    
    return None

def find_kicad_plugin_dir(kicad_version=None):
    """Find KiCad plugin directory with enhanced error checking"""
    if kicad_version is None:
        kicad_version = detect_kicad_version()
        if kicad_version is None:
            raise RuntimeError("Could not detect KiCad version. Please specify version manually.")
    
    logger.info(f"Using KiCad version: {kicad_version}")
    
    if platform.system() == "Windows":
        # Try both possible Windows locations
        paths = [
            os.path.join(os.path.expanduser("~"), "Documents", "KiCad", kicad_version, "3rdparty", "plugins"),
            os.path.join(os.getenv("APPDATA"), "kicad", kicad_version, "scripting", "plugins")
        ]
        
        for path in paths:
            if os.path.exists(os.path.dirname(path)):
                logger.info(f"Found KiCad plugin directory: {path}")
                return path
                
    elif platform.system() == "Darwin":  # macOS
        path = os.path.expanduser(f"~/Library/Application Support/kicad/{kicad_version}/scripting/plugins")
        if os.path.exists(os.path.dirname(path)):
            return path
            
    elif platform.system() == "Linux":
        paths = [
            os.path.expanduser(f"~/.local/share/kicad/{kicad_version}/scripting/plugins"),
            f"/usr/share/kicad/{kicad_version}/scripting/plugins"
        ]
        for path in paths:
            if os.path.exists(os.path.dirname(path)):
                return path
    
    raise RuntimeError(f"Could not find KiCad plugin directory for version {kicad_version}")

def verify_kicad_python():
    """Verify KiCad's Python environment and required modules"""
    try:
        if platform.system() == "Windows":
            kicad_python = os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "KiCad", "bin", "python.exe")
            if not os.path.exists(kicad_python):
                logger.warning("Could not find KiCad's Python. Will use system Python instead.")
                return False
                
            # Test importing required modules in KiCad's Python
            cmd = [kicad_python, "-c", "import pcbnew; import wx; import cv2; import numpy"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.warning(f"Missing required modules in KiCad's Python: {result.stderr}")
                return False
            
            return True
    except Exception as e:
        logger.warning(f"Error checking KiCad's Python: {str(e)}")
        return False

def install_dependencies():
    """Install required dependencies in the correct Python environment"""
    requirements = ["opencv-python", "numpy", "wxPython"]
    
    if platform.system() == "Windows" and verify_kicad_python():
        kicad_python = os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "KiCad", "bin", "python.exe")
        for req in requirements:
            try:
                subprocess.run([kicad_python, "-m", "pip", "install", req], check=True)
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install {req} in KiCad's Python: {str(e)}")
                return False
    else:
        # Fall back to system Python
        for req in requirements:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", req], check=True)
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install {req}: {str(e)}")
                return False
    
    return True

def install_advanced_plugin():
    """Install the advanced schematic importer plugin with enhanced error checking"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        kicad_version = detect_kicad_version()
        
        if kicad_version is None:
            logger.error("Could not detect KiCad version. Please install KiCad first.")
            return False
            
        kicad_plugin_dir = find_kicad_plugin_dir(kicad_version)
        logger.info(f"Installing plugin to: {kicad_plugin_dir}")
        
        target_dir = os.path.join(kicad_plugin_dir, "advanced_schematic_importer")
        os.makedirs(target_dir, exist_ok=True)
        
        # Create plugin directory structure with error checking
        dirs_to_create = [
            os.path.join(target_dir, "src", "recognition"),
            os.path.join(target_dir, "src", "utils"),
            os.path.join(target_dir, "resources", "icons"),
            os.path.join(target_dir, "resources", "templates")
        ]
        
        for dir_path in dirs_to_create:
            os.makedirs(dir_path, exist_ok=True)
            init_path = os.path.join(dir_path, "__init__.py")
            with open(init_path, "w") as f:
                f.write("# This file makes the directory a Python package\n")
        
        # Rest of your installation code...
        # (Copy files, create metadata.json, etc.)
        
        logger.info("Plugin installed successfully!")
        logger.info("\nTo use the plugin:")
        logger.info("1. Start KiCad")
        logger.info("2. Open PCB Editor")
        logger.info("3. Look for 'Advanced Schematic Importer' in the Tools menu")
        logger.info("\nIf KiCad is already running, please restart it to load the plugin.")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during plugin installation: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Starting Advanced Schematic Importer plugin installation...")
    
    if not install_dependencies():
        logger.error("Failed to install dependencies. Plugin installation aborted.")
        sys.exit(1)
        
    if not install_advanced_plugin():
        logger.error("Plugin installation failed.")
        sys.exit(1)
        
    logger.info("Installation completed successfully!")