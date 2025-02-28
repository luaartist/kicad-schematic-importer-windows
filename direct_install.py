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

def direct_install():
    """Install the plugin directly to the KiCad 9.0 plugins directory"""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get the KiCad plugin directory
    kicad_plugin_dir = find_kicad_plugin_dir("9.0")
    
    # Define the target directory
    target_dir = os.path.join(kicad_plugin_dir, "schematic_importer_direct")
    
    # Create the target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Create __init__.py
    with open(os.path.join(target_dir, "__init__.py"), "w") as f:
        f.write("""# This file makes the directory a Python package
# It allows the plugin to be imported by KiCad

try:
    from .action_plugin import SchematicImporter
except Exception as e:
    import traceback
    traceback.print_exc()
    raise e
""")
    
    # Create action_plugin.py
    with open(os.path.join(target_dir, "action_plugin.py"), "w") as f:
        f.write("""import pcbnew
import wx

class SchematicImporter(pcbnew.ActionPlugin):
    \"\"\"A minimal plugin that shows a message box when clicked\"\"\"
    
    def defaults(self):
        self.name = "Schematic Importer Direct"
        self.category = "Import"
        self.description = "Import schematics from images using computer vision"
        self.show_toolbar_button = True
        self.icon_file_name = ""
    
    def Run(self):
        wx.MessageBox("Hello from Schematic Importer Direct!", "Schematic Importer", wx.OK | wx.ICON_INFORMATION)

# Register the plugin
SchematicImporter().register()
""")
    
    # Create metadata.json
    with open(os.path.join(target_dir, "metadata.json"), "w") as f:
        f.write("""{
    "identifier": "com.augmentcode.kicad.schematicimporterdirect",
    "name": "Schematic Importer Direct",
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
    
    print(f"Plugin installed directly to: {target_dir}")
    print("\nTo use the plugin:")
    print("1. Start KiCad")
    print("2. Open PCB Editor")
    print("3. Look for 'Schematic Importer Direct' in the Tools menu or toolbar")
    print("\nIf KiCad is already running, please restart it to load the plugin.")

if __name__ == "__main__":
    direct_install()
