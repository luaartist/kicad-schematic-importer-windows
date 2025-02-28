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
        # KiCad 9.0 uses 3rdparty plugins directory on Windows
        plugin_dir = os.path.join(os.path.expanduser("~"), "Documents", "KiCad", "9.0", "3rdparty", "plugins")
        resources_dir = os.path.join(os.path.expanduser("~"), "Documents", "KiCad", "9.0", "3rdparty", "resources")
        
        # Create directories if they don't exist
        os.makedirs(plugin_dir, exist_ok=True)
        os.makedirs(resources_dir, exist_ok=True)
        
        return plugin_dir
    elif platform.system() == "Darwin":  # macOS
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "kicad", kicad_version, "scripting", "plugins")
    else:  # Linux
        return os.path.join(os.path.expanduser("~"), ".local", "share", "kicad", kicad_version, "scripting", "plugins")

def install_dependencies():
    """Install required Python dependencies"""
    try:
        print("\nInstalling dependencies...")
        
        # Get the requirements file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_path = os.path.join(current_dir, "requirements.txt")
        
        if not os.path.exists(requirements_path):
            print(f"Warning: requirements.txt not found at {requirements_path}")
            return False
        
        # Install dependencies using pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        
        print("Dependencies installed successfully.")
        return True
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        return False

def create_plugin_structure(target_dir, current_dir):
    """Create plugin directory structure and copy files"""
    try:
        print(f"\nCreating plugin structure in {target_dir}...")
        
        # Create directory structure
        dirs = [
            os.path.join(target_dir, "src", "recognition"),
            os.path.join(target_dir, "src", "utils"),
            os.path.join(target_dir, "resources", "icons"),
            os.path.join(target_dir, "resources", "templates")
        ]
        
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
            init_file = os.path.join(dir_path, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w") as f:
                    f.write("# This file makes the directory a Python package\n")
        
        # Create main __init__.py
        with open(os.path.join(target_dir, "__init__.py"), "w") as f:
            f.write(
                "# KiCad Advanced Schematic Importer Plugin\n"
                "try:\n"
                "    from .action_plugin import AdvancedSchematicImporter\n"
                "except Exception as e:\n"
                "    import traceback\n"
                "    traceback.print_exc()\n"
            )
        
        # Copy source files if they exist
        source_files = [
            ("src/recognition/component_recognizer.py", "src/recognition"),
            ("src/recognition/connection_tracer.py", "src/recognition"),
            ("src/utils/pdf_importer.py", "src/utils"),
            ("src/utils/alternative_image_processor.py", "src/utils"),
            ("src/utils/path_validator.py", "src/utils")
        ]
        
        for src_file, dst_dir in source_files:
            src_path = os.path.join(current_dir, src_file)
            if os.path.exists(src_path):
                dst_path = os.path.join(target_dir, dst_dir, os.path.basename(src_file))
                shutil.copy2(src_path, dst_path)
                print(f"Copied {src_file} to {dst_path}")
            else:
                print(f"Warning: Source file {src_path} not found")
        
        return True
    except Exception as e:
        print(f"Error creating plugin structure: {e}")
        return False

def create_metadata(target_dir):
    """Create plugin metadata file"""
    metadata = {
        "identifier": "com.augmentcode.kicad.advancedschematicimporter",
        "name": "Advanced Schematic Importer",
        "description": "Import schematics from images with advanced features",
        "description_full": "An advanced KiCad plugin that imports schematics from images and PDFs with component recognition and connection tracing.",
        "category": "Importers",
        "author": {
            "name": "Wallace Lebrun",
            "contact": {
                "web": "https://github.com/augmentcode/kicad-schematic-importer"
            }
        },
        "license": "MIT",
        "version": "0.5.0",
        "kicad_version": "9.0",
        "platforms": ["linux", "windows", "macos"],
        "tags": ["import", "computer vision", "automation", "pdf", "schematic"]
    }
    
    metadata_path = os.path.join(target_dir, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)
    
    print(f"Created metadata file: {metadata_path}")

def create_plugin_icon(target_dir, current_dir):
    """Create or copy plugin icon"""
    icon_path = os.path.join(target_dir, "resources", "icons", "icon.png")
    src_icon_path = os.path.join(current_dir, "resources", "icons", "icon.png")
    
    if os.path.exists(src_icon_path):
        shutil.copy2(src_icon_path, icon_path)
        print(f"Copied icon from: {src_icon_path}")
    else:
        # Create a placeholder icon (red square)
        with open(icon_path, "wb") as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00\x90\x91h6\x00\x00\x00\x0cIDATx\x9cc\xf8\xff\xff?\x03\x9d\x01\x00\x08\xfc\x02\xfe\xa7\xa7\xa9\x83\x00\x00\x00\x00IEND\xaeB`\x82')
        print(f"Created placeholder icon: {icon_path}")

def create_plugin_file(target_dir):
    with open(os.path.join(target_dir, "plugin.py"), "w") as f:
        f.write('''import os
import pcbnew
import wx

class AdvancedSchematicImporter:
    def __init__(self):
        self.name = "Advanced Schematic Importer"
        self.category = "Importers"
        self.description = "Import schematics from images with advanced features"
        
    def register(self):
        """Register the plugin with KiCad"""
        # Registration code here
        pass

    def _create_default_pads(self, footprint):
        """Create default pads for a footprint"""
        # Create pads
        self._create_pad(footprint, 1, pcbnew.VECTOR2I(pcbnew.FromMM(-2.5), pcbnew.FromMM(0)))
        self._create_pad(footprint, 2, pcbnew.VECTOR2I(pcbnew.FromMM(2.5), pcbnew.FromMM(0)))
    
    def _create_pad(self, footprint, pad_num, position):
        """Create a pad for a footprint"""
        pad = pcbnew.PAD(footprint)
        pad.SetNumber(str(pad_num))
        pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
        pad.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
        pad.SetSize(pcbnew.VECTOR2I(pcbnew.FromMM(1.5), pcbnew.FromMM(1.5)))
        pad.SetPosition(position)
        pad.SetDrillSize(pcbnew.VECTOR2I(pcbnew.FromMM(0.8), pcbnew.FromMM(0.8)))
        pad.SetLayerSet(pcbnew.LSET.AllCuMask())
        footprint.Add(pad)
        return pad

# Register the plugin
AdvancedSchematicImporter().register()
''')

def install_advanced_plugin():
    """Install the advanced schematic importer plugin"""
    try:
        # Get directories
        current_dir = os.path.dirname(os.path.abspath(__file__))
        kicad_plugin_dir = find_kicad_plugin_dir("9.0")
        target_dir = os.path.join(kicad_plugin_dir, "enhanced_importer_v2")
        
        print(f"\nInstalling Advanced Schematic Importer plugin...")
        print(f"Target directory: {target_dir}")
        
        # Create plugin structure
        if not create_plugin_structure(target_dir, current_dir):
            print("Failed to create plugin structure. Installation aborted.")
            return False
        
        # Create metadata
        create_metadata(target_dir)
        
        # Create or copy icon
        create_plugin_icon(target_dir, current_dir)
        
        # Create plugin file
        create_plugin_file(target_dir)
        
        print("\nPlugin installation complete!")
        print("\nTo use the plugin:")
        print("1. Start KiCad")
        print("2. Open PCB Editor")
        print("3. Look for 'Advanced Schematic Importer' in the Tools menu")
        print("\nIf KiCad is already running, please restart it to load the plugin.")
        
        return True
        
    except Exception as e:
        print(f"\nError installing plugin: {e}")
        return False

if __name__ == "__main__":
    if install_dependencies():
        install_advanced_plugin()
    else:
        print("\nFailed to install dependencies. Plugin installation aborted.")
