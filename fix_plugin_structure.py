#!/usr/bin/env python3
import os
import shutil
import re

def ensure_init_files():
    """Ensure all directories have __init__.py files"""
    print("Ensuring all directories have __init__.py files...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Walk through all directories
    for root, dirs, files in os.walk(current_dir):
        # Skip .git directory
        if ".git" in root:
            continue
        
        # Skip __pycache__ directories
        if "__pycache__" in root:
            continue
        
        # Check if __init__.py exists in the directory
        init_file = os.path.join(root, "__init__.py")
        if not os.path.exists(init_file):
            # Create __init__.py file
            with open(init_file, "w") as f:
                f.write("# This file makes the directory a Python package\n")
            print(f"Created __init__.py in {root}")

def copy_action_plugin():
    """Copy action_plugin.py to the root directory"""
    print("Copying action_plugin.py to the root directory...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if action_plugin.py exists
    if os.path.exists(os.path.join(current_dir, "action_plugin.py")):
        print("action_plugin.py already exists in the root directory")
        return
    
    # Check if minimal_plugin.py exists
    if os.path.exists(os.path.join(current_dir, "minimal_plugin.py")):
        # Copy minimal_plugin.py to action_plugin.py
        shutil.copy2(
            os.path.join(current_dir, "minimal_plugin.py"),
            os.path.join(current_dir, "action_plugin.py")
        )
        print("Copied minimal_plugin.py to action_plugin.py")
        return
    
    # Check if src/plugin/schematic_importer.py exists
    if os.path.exists(os.path.join(current_dir, "src", "plugin", "schematic_importer.py")):
        # Create action_plugin.py based on src/plugin/schematic_importer.py
        with open(os.path.join(current_dir, "src", "plugin", "schematic_importer.py"), "r") as f:
            content = f.read()
        
        # Update imports
        content = content.replace("from ..", "from src")
        
        # Write to action_plugin.py
        with open(os.path.join(current_dir, "action_plugin.py"), "w") as f:
            f.write(content)
        
        print("Created action_plugin.py based on src/plugin/schematic_importer.py")
        return
    
    # If no existing file is found, create a basic action_plugin.py
    print("Creating a basic action_plugin.py...")
    with open(os.path.join(current_dir, "action_plugin.py"), "w") as f:
        f.write("""import pcbnew
import wx
import os
import sys

# Add the plugin directory to the Python path
plugin_dir = os.path.dirname(os.path.abspath(__file__))
if plugin_dir not in sys.path:
    sys.path.insert(0, plugin_dir)

from src.utils.alternative_image_processor import AlternativeImageProcessor
from src.ui.import_dialog import ImportDialog

class SchematicImporter(pcbnew.ActionPlugin):
    \"\"\"
    A plugin to import schematics from images
    \"\"\"
    def defaults(self):
        self.name = "Schematic Importer"
        self.category = "Import"
        self.description = "Import schematics from images using computer vision"
        self.show_toolbar_button = True
        # Set the icon file path
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "icons", "icon.png")
        self.icon_file_name = icon_path if os.path.exists(icon_path) else ""

    def Run(self):
        # Get the current board
        board = pcbnew.GetBoard()
        
        # Create and show the import dialog
        dialog = ImportDialog(None, board)
        result = dialog.ShowModal()
        
        if result == wx.ID_OK:
            try:
                # Process the vector file
                file_path = dialog.get_file_path()
                processor = AlternativeImageProcessor()
                processed_path = processor.process_vector_file(file_path)
                self.import_schematic(board, processed_path)
                pcbnew.Refresh()
            except Exception as e:
                wx.MessageBox(f"Error importing schematic: {str(e)}", 
                            "Import Error", wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()

    def import_schematic(self, board, svg_path):
        \"\"\"Import the SVG schematic into the board\"\"\"
        # Implementation will go here
        pass

# Register the plugin
SchematicImporter().register()
""")

def ensure_metadata_json():
    """Ensure metadata.json exists in the root directory"""
    print("Ensuring metadata.json exists in the root directory...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if metadata.json exists
    if os.path.exists(os.path.join(current_dir, "metadata.json")):
        print("metadata.json already exists in the root directory")
        return
    
    # Check if src/plugin/metadata.json exists
    if os.path.exists(os.path.join(current_dir, "src", "plugin", "metadata.json")):
        # Copy src/plugin/metadata.json to the root directory
        shutil.copy2(
            os.path.join(current_dir, "src", "plugin", "metadata.json"),
            os.path.join(current_dir, "metadata.json")
        )
        print("Copied src/plugin/metadata.json to the root directory")
        return
    
    # If no existing file is found, create a basic metadata.json
    print("Creating a basic metadata.json...")
    with open(os.path.join(current_dir, "metadata.json"), "w") as f:
        f.write("""{
    "identifier": "com.augmentcode.kicad.schematicimporter",
    "name": "Schematic Importer",
    "description": "Import schematics from images using computer vision",
    "description_full": "A powerful KiCad plugin that uses computer vision to convert images of schematics into editable KiCad projects. Perfect for digitizing hand-drawn circuits, photographed schematics, or legacy documentation.",
    "category": "Importers",
    "author": {
        "name": "Augment Code",
        "contact": {
            "web": "https://github.com/augmentcode/kicad-schematic-importer"
        }
    },
    "license": "MIT",
    "resources": {
        "homepage": "https://github.com/augmentcode/kicad-schematic-importer"
    },
    "versions": [
        {
            "version": "0.3.2",
            "status": "testing",
            "kicad_version": "9.0",
            "platforms": ["linux", "windows", "macos"]
        }
    ],
    "tags": ["import", "computer vision", "automation"]
}""")

def ensure_icon():
    """Ensure icon.png exists in the resources/icons directory"""
    print("Ensuring icon.png exists in the resources/icons directory...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if resources/icons directory exists
    icons_dir = os.path.join(current_dir, "resources", "icons")
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir, exist_ok=True)
        print(f"Created directory: {icons_dir}")
    
    # Check if icon.png exists
    icon_path = os.path.join(icons_dir, "icon.png")
    if os.path.exists(icon_path):
        print("icon.png already exists in the resources/icons directory")
        return
    
    # Check if resources/icon.png exists
    if os.path.exists(os.path.join(current_dir, "resources", "icon.png")):
        # Copy resources/icon.png to resources/icons/icon.png
        shutil.copy2(
            os.path.join(current_dir, "resources", "icon.png"),
            icon_path
        )
        print("Copied resources/icon.png to resources/icons/icon.png")
        return
    
    # If no existing file is found, create a placeholder icon.png
    print("Creating a placeholder icon.png...")
    with open(icon_path, "wb") as f:
        # This is a minimal 16x16 PNG file (a red square)
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00\x90\x91h6\x00\x00\x00\x0cIDATx\x9cc\xf8\xff\xff?\x03\x9d\x01\x00\x08\xfc\x02\xfe\xa7\xa7\xa9\x83\x00\x00\x00\x00IEND\xaeB`\x82')

def update_import_paths():
    """Update import paths in the code"""
    print("Updating import paths in the code...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Files to process
    python_files = []
    for root, _, files in os.walk(current_dir):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    
    # Patterns to replace
    patterns = [
        (r"from \.\.", r"from src"),  # Replace relative imports with absolute imports
        (r"from \.", r"from src"),    # Replace relative imports with absolute imports
    ]
    
    for file_path in python_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Apply replacements
            modified = False
            for pattern, replacement in patterns:
                new_content = re.sub(pattern, replacement, content)
                if new_content != content:
                    content = new_content
                    modified = True
            
            if modified:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                
                print(f"Updated import paths in {file_path}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

def create_install_script():
    """Create an install script for the plugin"""
    print("Creating install script...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if install.py exists
    if os.path.exists(os.path.join(current_dir, "install.py")):
        print("install.py already exists")
        return
    
    # Create install.py
    with open(os.path.join(current_dir, "install.py"), "w") as f:
        f.write('''#!/usr/bin/env python3
import os
import sys
import shutil
import platform
import argparse

def find_kicad_plugin_dir(kicad_version="7.0"):
    """Find KiCad plugin directory"""
    if platform.system() == "Windows":
        if kicad_version == "9.0":
            # KiCad 9.0 uses a different location on Windows
            return os.path.join(os.path.expanduser("~"), "Documents", "KiCad", "9.0", "3rdparty", "plugins")
        else:
            # Windows: %APPDATA%\\kicad\\7.0\\scripting\\plugins
            return os.path.join(os.getenv("APPDATA"), "kicad", kicad_version, "scripting", "plugins")
    elif platform.system() == "Darwin":  # macOS
        # macOS: ~/Library/Application Support/kicad/scripting/plugins
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "kicad", kicad_version, "scripting", "plugins")
    else:  # Linux
        # Linux: ~/.local/share/kicad/scripting/plugins
        return os.path.join(os.path.expanduser("~"), ".local", "share", "kicad", kicad_version, "scripting", "plugins")

def install_plugin(plugin_dir=None, kicad_plugin_dir=None, kicad_version="7.0"):
    """Install the plugin to KiCad plugins directory"""
    if not plugin_dir:
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
    
    if not kicad_plugin_dir:
        kicad_plugin_dir = find_kicad_plugin_dir(kicad_version)
    
    target_dir = os.path.join(kicad_plugin_dir, "schematic_importer")
    
    # Create plugin directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Copy plugin files
    files_copied = 0
    for source in os.listdir(plugin_dir):
        if source.startswith((".", "__")) or source == "install.py":
            continue
            
        source_path = os.path.join(plugin_dir, source)
        destination = os.path.join(target_dir, source)
        
        if os.path.isdir(source_path):
            shutil.copytree(source_path, destination, dirs_exist_ok=True)
            files_copied += len([f for _, _, files in os.walk(source_path) for f in files])
        else:
            shutil.copy2(source_path, destination)
            files_copied += 1
    
    print(f"Plugin installed to: {target_dir}")
    print(f"Copied {files_copied} files")
    
    print("\\nTo use the plugin:")
    print("1. Start KiCad")
    print("2. Open PCB Editor")
    print("3. Look for 'Schematic Importer' in the Tools menu or toolbar")
    print("\\nIf KiCad is already running, please restart it to load the plugin.")
    
    return target_dir

def main():
    parser = argparse.ArgumentParser(description="Install KiCad Schematic Importer Plugin")
    parser.add_argument("--plugin-dir", type=str, help="Plugin source directory")
    parser.add_argument("--kicad-dir", type=str, help="KiCad plugins directory")
    parser.add_argument("--kicad-version", type=str, default="7.0", help="KiCad version (default: 7.0)")
    
    args = parser.parse_args()
    
    install_plugin(args.plugin_dir, args.kicad_dir, args.kicad_version)

if __name__ == "__main__":
    main()
""")
    
    print("Created install.py")

def main():
    print("Fixing plugin structure...")
    
    # Ensure all directories have __init__.py files
    ensure_init_files()
    
    # Copy action_plugin.py to the root directory
    copy_action_plugin()
    
    # Ensure metadata.json exists in the root directory
    ensure_metadata_json()
    
    # Ensure icon.png exists in the resources/icons directory
    ensure_icon()
    
    # Update import paths in the code
    update_import_paths()
    
    # Create install script
    create_install_script()
    
    print("\nPlugin structure fixed!")
    print("\nTo install the plugin, run:")
    print("python install.py --kicad-version 9.0")

if __name__ == "__main__":
    main()
