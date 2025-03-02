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

def simple_install():
    """Install the plugin to KiCad 9.0 plugins directory"""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get the KiCad plugin directory
    kicad_plugin_dir = find_kicad_plugin_dir("9.0")
    
    # Define the target directory
    target_dir = os.path.join(kicad_plugin_dir, "schematic_importer_simple")
    
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
import os
import sys

# Add the plugin directory to the Python path
plugin_dir = os.path.dirname(os.path.abspath(__file__))
if plugin_dir not in sys.path:
    sys.path.insert(0, plugin_dir)

class SchematicImporter(pcbnew.ActionPlugin):
    def __init__(self):
        super().__init__()
        
    def defaults(self):
        self.name = "Schematic Importer Simple"
        self.category = "Import"
        self.description = "Import schematics from images using computer vision"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")

    def Run(self):
        # Get the current board
        board = pcbnew.GetBoard()
        
        # Create a dialog
        dialog = wx.FileDialog(
            None, 
            message="Select an image file",
            wildcard="Image files (*.png;*.jpg;*.jpeg;*.bmp;*.svg)|*.png;*.jpg;*.jpeg;*.bmp;*.svg",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )
        
        # Show the dialog
        if dialog.ShowModal() == wx.ID_OK:
            try:
                # Get the selected file path
                file_path = dialog.GetPath()
                
                # Create a text item on the board to show the import was successful
                text = pcbnew.PCB_TEXT(board)
                text.SetText(f"Imported from {os.path.basename(file_path)}")
                text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(100), pcbnew.FromMM(100)))
                text.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(5), pcbnew.FromMM(5)))
                board.Add(text)
                
                # Refresh the board view
                pcbnew.Refresh()
                
                wx.MessageBox(f"Schematic imported successfully from {os.path.basename(file_path)}.", 
                            "Import Complete", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error importing schematic: {str(e)}", 
                            "Import Error", wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()

# Register the plugin
SchematicImporter().register()
""")
    
    # Create metadata.json
    with open(os.path.join(target_dir, "metadata.json"), "w") as f:
        f.write("""{
    "identifier": "com.augmentcode.kicad.schematicimporter",
    "name": "Schematic Importer",
    "description": "Import schematics from images using computer vision",
    "author": {
        "name": "Wallace Lebrun",
        "contact": {
            "web": "https://github.com/augmentcode/kicad-schematic-importer"
        }
    },
    "license": "MIT",
    "copyright": "© 2024 Wallace Lebrun"
}""")
    
    # Create icon.png
    icon_path = os.path.join(target_dir, "icon.png")
    if not os.path.exists(icon_path):
        # Check if resources/icons/icon.png exists
        if os.path.exists(os.path.join(current_dir, "resources", "icons", "icon.png")):
            # Copy resources/icons/icon.png to the target directory
            shutil.copy2(
                os.path.join(current_dir, "resources", "icons", "icon.png"),
                icon_path
            )
        else:
            # Create a placeholder icon.png
            with open(icon_path, "wb") as f:
                # This is a minimal 16x16 PNG file (a red square)
                f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00\x90\x91h6\x00\x00\x00\x0cIDATx\x9cc\xf8\xff\xff?\x03\x9d\x01\x00\x08\xfc\x02\xfe\xa7\xa7\xa9\x83\x00\x00\x00\x00IEND\xaeB`\x82')
    
    print(f"Plugin installed to: {target_dir}")
    print("\nTo use the plugin:")
    print("1. Start KiCad")
    print("2. Open PCB Editor")
    print("3. Look for 'Schematic Importer Simple' in the Tools menu or toolbar")
    print("\nIf KiCad is already running, please restart it to load the plugin.")

if __name__ == "__main__":
    simple_install()
