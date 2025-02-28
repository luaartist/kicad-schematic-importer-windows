#!/usr/bin/env python3
import os
import shutil
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

def fix_missing_files():
    """Fix missing files in the plugin directory"""
    # Get the KiCad plugin directory
    kicad_plugin_dir = find_kicad_plugin_dir("9.0")
    
    # Define the plugin directory
    plugin_dir = os.path.join(kicad_plugin_dir, "schematic_importer")
    
    # Check if the plugin directory exists
    if not os.path.exists(plugin_dir):
        print(f"Plugin directory not found: {plugin_dir}")
        return
    
    # Create __init__.py
    init_file = os.path.join(plugin_dir, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            f.write("""# This file makes the directory a Python package
# It allows the plugin to be imported by KiCad

try:
    from .action_plugin import SchematicImporter
except Exception as e:
    import traceback
    traceback.print_exc()
    raise e
""")
        print(f"Created __init__.py in {plugin_dir}")
    
    # Create resources/icons directory
    icons_dir = os.path.join(plugin_dir, "resources", "icons")
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir, exist_ok=True)
        print(f"Created directory: {icons_dir}")
    
    # Check if icon.png exists in resources/icons
    icon_path = os.path.join(icons_dir, "icon.png")
    if not os.path.exists(icon_path):
        # Check if resources/icon.png exists
        if os.path.exists(os.path.join(plugin_dir, "resources", "icon.png")):
            # Copy resources/icon.png to resources/icons/icon.png
            shutil.copy2(
                os.path.join(plugin_dir, "resources", "icon.png"),
                icon_path
            )
            print(f"Copied resources/icon.png to resources/icons/icon.png")
        # Check if src/plugin/icon.png exists
        elif os.path.exists(os.path.join(plugin_dir, "src", "plugin", "icon.png")):
            # Copy src/plugin/icon.png to resources/icons/icon.png
            shutil.copy2(
                os.path.join(plugin_dir, "src", "plugin", "icon.png"),
                icon_path
            )
            print(f"Copied src/plugin/icon.png to resources/icons/icon.png")
        # Check if resources/icons/schematic_importer.png exists
        elif os.path.exists(os.path.join(plugin_dir, "resources", "icons", "schematic_importer.png")):
            # Copy resources/icons/schematic_importer.png to resources/icons/icon.png
            shutil.copy2(
                os.path.join(plugin_dir, "resources", "icons", "schematic_importer.png"),
                icon_path
            )
            print(f"Copied resources/icons/schematic_importer.png to resources/icons/icon.png")
        else:
            # Create a placeholder icon.png
            with open(icon_path, "wb") as f:
                # This is a minimal 16x16 PNG file (a red square)
                f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00\x90\x91h6\x00\x00\x00\x0cIDATx\x9cc\xf8\xff\xff?\x03\x9d\x01\x00\x08\xfc\x02\xfe\xa7\xa7\xa9\x83\x00\x00\x00\x00IEND\xaeB`\x82')
            print(f"Created placeholder icon.png in {icons_dir}")
    
    # Update action_plugin.py to reference the icon
    action_plugin_path = os.path.join(plugin_dir, "action_plugin.py")
    if os.path.exists(action_plugin_path):
        with open(action_plugin_path, "r") as f:
            content = f.read()
        
        # Check if the icon_file_name is empty
        if 'self.icon_file_name = ""' in content:
            # Update the icon_file_name
            content = content.replace(
                'self.icon_file_name = ""',
                'self.icon_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "icons", "icon.png")'
            )
            
            with open(action_plugin_path, "w") as f:
                f.write(content)
            
            print(f"Updated action_plugin.py to reference the icon")
    
    print("\nMissing files fixed!")
    print("\nTo use the plugin:")
    print("1. Start KiCad")
    print("2. Open PCB Editor")
    print("3. Look for 'Schematic Importer' in the Tools menu or toolbar")
    print("\nIf KiCad is already running, please restart it to load the plugin.")

if __name__ == "__main__":
    fix_missing_files()
