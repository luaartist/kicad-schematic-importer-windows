#!/usr/bin/env python3
import os
import platform

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

def check_plugin_installation():
    """Check if the plugin is installed correctly"""
    # Get the KiCad plugin directory
    kicad_plugin_dir = find_kicad_plugin_dir("9.0")
    
    # Check if the plugin directory exists
    plugin_dir = os.path.join(kicad_plugin_dir, "schematic_importer")
    if not os.path.exists(plugin_dir):
        print(f"Plugin directory not found: {plugin_dir}")
        return
    
    print(f"Plugin directory found: {plugin_dir}")
    
    # Check if the required files exist
    required_files = [
        "__init__.py",
        "action_plugin.py",
        "metadata.json",
        os.path.join("resources", "icons", "icon.png")
    ]
    
    for file in required_files:
        file_path = os.path.join(plugin_dir, file)
        if os.path.exists(file_path):
            print(f"Found: {file}")
        else:
            print(f"Missing: {file}")
    
    # List all files in the plugin directory
    print("\nAll files in the plugin directory:")
    for root, dirs, files in os.walk(plugin_dir):
        for file in files:
            print(os.path.join(root, file).replace(plugin_dir, "").lstrip(os.sep))

if __name__ == "__main__":
    check_plugin_installation()
