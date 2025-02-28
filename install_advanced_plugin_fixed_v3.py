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
    os.makedirs(os.path.join(target_dir, "src", "recognition"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "src", "utils"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "resources", "icons"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "resources", "templates"), exist_ok=True)
    
    # Create __init__.py files
    for dir_path in [
        target_dir,
        os.path.join(target_dir, "src"),
        os.path.join(target_dir, "src", "recognition"),
        os.path.join(target_dir, "src", "utils"),
        os.path.join(target_dir, "resources"),
        os.path.join(target_dir, "resources", "icons"),
        os.path.join(target_dir, "resources", "templates")
    ]:
        with open(os.path.join(dir_path, "__init__.py"), "w") as f:
            f.write("# This file makes the directory a Python package\n")
    
    # Create main __init__.py
    with open(os.path.join(target_dir, "__init__.py"), "w") as f:
        f.write(
            "# This file makes the directory a Python package\n"
            "# It allows the plugin to be imported by KiCad\n"
            "\n"
            "try:\n"
            "    from .action_plugin import AdvancedSchematicImporter\n"
            "except Exception as e:\n"
            "    import traceback\n"
            "    traceback.print_exc()\n"
        )
    
    # Copy source files
    source_files = [
        ("src/recognition/component_recognizer.py", os.path.join(target_dir, "src", "recognition", "component_recognizer.py")),
        ("src/recognition/connection_tracer.py", os.path.join(target_dir, "src", "recognition", "connection_tracer.py")),
        ("src/utils/pdf_importer.py", os.path.join(target_dir, "src", "utils", "pdf_importer.py")),
        ("src/utils/alternative_image_processor.py", os.path.join(target_dir, "src", "utils", "alternative_image_processor.py")),
        ("src/utils/path_validator.py", os.path.join(target_dir, "src", "utils", "path_validator.py"))
    ]
    
    for src, dst in source_files:
        src_path = os.path.join(current_dir, src)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst)
            print(f"Copied {src} to {dst}")
        else:
            print(f"Warning: Source file {src_path} not found")
    
    # Create action_plugin.py content
    action_plugin_content = (
        "import pcbnew\n"
        "import wx\n"
        "import os\n"
        "import sys\n"
        "import cv2\n"
        "import numpy as np\n"
        "from pathlib import Path\n"
        "\n"
        "# Add the plugin directory to the Python path\n"
        "plugin_dir = os.path.dirname(os.path.abspath(__file__))\n"
        "if plugin_dir not in sys.path:\n"
        "    sys.path.insert(0, plugin_dir)\n"
        "\n"
        "# Import plugin modules\n"
        "from src.recognition.component_recognizer import ComponentRecognizer\n"
        "from src.recognition.connection_tracer import ConnectionTracer\n"
        "from src.utils.pdf_importer import PDFImporter\n"
        "from src.utils.alternative_image_processor import AlternativeImageProcessor\n"
        "from src.utils.path_validator import PathValidator\n"
        "\n"
        "class AdvancedSchematicImporter(pcbnew.ActionPlugin):\n"
        "    def __init__(self):\n"
        "        super().__init__()\n"
        "        self.name = \"Advanced Schematic Importer\"\n"
        "        self.category = \"Import\"\n"
        "        self.description = \"Import schematics from images with advanced features\"\n"
        "        self.show_toolbar_button = True\n"
        "        # Set the icon file path\n"
        "        self.icon_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), \n"
        "                                         \"resources\", \"icons\", \"icon.png\")\n"
        "        \n"
        "        self.component_recognizer = ComponentRecognizer()\n"
        "        self.connection_tracer = ConnectionTracer()\n"
        "        self.pdf_importer = PDFImporter()\n"
        "        self.image_processor = AlternativeImageProcessor()\n"
        "        self.path_validator = PathValidator()\n"
        "        self.components = []\n"
        "        self.connections = []\n"
        "\n"
        "    def Run(self):\n"
        "        # Get the current board\n"
        "        board = pcbnew.GetBoard()\n"
        "        \n"
        "        # Create the main dialog\n"
        "        dialog = wx.Dialog(None, title=\"Advanced Schematic Importer\", size=(500, 400))\n"
        "        \n"
        "        # Create a panel\n"
        "        panel = wx.Panel(dialog)\n"
        "        \n"
        "        # Create a vertical box sizer\n"
        "        main_sizer = wx.BoxSizer(wx.VERTICAL)\n"
        "        \n"
        "        # Add a file picker\n"
        "        file_sizer = wx.BoxSizer(wx.HORIZONTAL)\n"
        "        file_label = wx.StaticText(panel, label=\"Input File:\")\n"
        "        self.file_picker = wx.FilePickerCtrl(\n"
        "            panel, \n"
        "            message=\"Select a file\",\n"
        "            wildcard=\"All supported files (*.png;*.jpg;*.jpeg;*.bmp;*.svg;*.pdf)|*.png;*.jpg;*.jpeg;*.bmp;*.svg;*.pdf\"\n"
        "        )\n"
        "        file_sizer.Add(file_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)\n"
        "        file_sizer.Add(self.file_picker, 1, wx.EXPAND)\n"
        "        main_sizer.Add(file_sizer, 0, wx.EXPAND | wx.ALL, 10)\n"
        "        \n"
        "        # Add processing options\n"
        "        options_sizer = wx.StaticBoxSizer(wx.VERTICAL, panel, \"Processing Options\")\n"
        "        \n"
        "        # Component recognition\n"
        "        self.recognize_components_cb = wx.CheckBox(panel, label=\"Recognize Components\")\n"
        "        self.recognize_components_cb.SetValue(True)\n"
        "        options_sizer.Add(self.recognize_components_cb, 0, wx.ALL, 5)\n"
        "        \n"
        "        # Connection tracing\n"
        "        self.trace_connections_cb = wx.CheckBox(panel, label=\"Trace Connections\")\n"
        "        self.trace_connections_cb.SetValue(True)\n"
        "        options_sizer.Add(self.trace_connections_cb, 0, wx.ALL, 5)\n"
        "        \n"
        "        main_sizer.Add(options_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)\n"
        "        \n"
        "        # Add buttons\n"
        "        button_sizer = wx.StdDialogButtonSizer()\n"
        "        ok_button = wx.Button(panel, wx.ID_OK)\n"
        "        cancel_button = wx.Button(panel, wx.ID_CANCEL)\n"
        "        button_sizer.AddButton(ok_button)\n"
        "        button_sizer.AddButton(cancel_button)\n"
        "        button_sizer.Realize()\n"
        "        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 10)\n"
        "        \n"
        "        # Set the sizer\n"
        "        panel.SetSizer(main_sizer)\n"
        "        \n"
        "        # Show the dialog\n"
        "        if dialog.ShowModal() == wx.ID_OK:\n"
        "            # Get the selected file path\n"
        "            file_path = self.file_picker.GetPath()\n"
        "            \n"
        "            # Process the image\n"
        "            image = cv2.imread(file_path)\n"
        "            if image is not None:\n"
        "                # Recognize components if enabled\n"
        "                if self.recognize_components_cb.GetValue():\n"
        "                    self.components = self.component_recognizer.recognize_components(image)\n"
        "                \n"
        "                # Trace connections if enabled\n"
        "                if self.trace_connections_cb.GetValue():\n"
        "                    self.connections = self.connection_tracer.trace_connections(image, self.components)\n"
        "                \n"
        "                # Add components to board\n"
        "                for component in self.components:\n"
        "                    # Create a footprint\n"
        "                    footprint = pcbnew.FOOTPRINT(board)\n"
        "                    footprint.SetReference(component[\"id\"])\n"
        "                    footprint.SetValue(component.get(\"value\", component[\"type\"].upper()))\n"
        "                    \n"
        "                    # Set position\n"
        "                    x_mm = component[\"x\"] / 10  # Convert to mm\n"
        "                    y_mm = component[\"y\"] / 10\n"
        "                    footprint.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x_mm), pcbnew.FromMM(y_mm)))\n"
        "                    \n"
        "                    # Add to board\n"
        "                    board.Add(footprint)\n"
        "                \n"
        "                # Add connections to board\n"
        "                for connection in self.connections:\n"
        "                    if \"points\" in connection:\n"
        "                        points = connection[\"points\"]\n"
        "                        for i in range(len(points) - 1):\n"
        "                            # Create a track\n"
        "                            track = pcbnew.PCB_TRACK(board)\n"
        "                            \n"
        "                            # Set start and end points\n"
        "                            x1_mm = points[i][0] / 10\n"
        "                            y1_mm = points[i][1] / 10\n"
        "                            x2_mm = points[i+1][0] / 10\n"
        "                            y2_mm = points[i+1][1] / 10\n"
        "                            \n"
        "                            track.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1_mm), pcbnew.FromMM(y1_mm)))\n"
        "                            track.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2_mm), pcbnew.FromMM(y2_mm)))\n"
        "                            track.SetWidth(pcbnew.FromMM(0.2))  # 0.2mm track width\n"
        "                            \n"
        "                            # Add to board\n"
        "                            board.Add(track)\n"
        "                \n"
        "                # Refresh the board\n"
        "                pcbnew.Refresh()\n"
        "                \n"
        "                # Show success message\n"
        "                wx.MessageBox(\n"
        "                    f\"Successfully imported {len(self.components)} components and {len(self.connections)} connections\",\n"
        "                    \"Import Complete\",\n"
        "                    wx.OK | wx.ICON_INFORMATION\n"
        "                )\n"
        "            else:\n"
        "                wx.MessageBox(\n"
        "                    \"Failed to load image\",\n"
        "                    \"Import Error\",\n"
        "                    wx.OK | wx.ICON_ERROR\n"
        "                )\n"
        "        \n"
        "        dialog.Destroy()\n"
        "\n"
        "# Register the plugin\n"
        "AdvancedSchematicImporter().register()\n"
    )
    
    # Write action_plugin.py
    with open(os.path.join(target_dir, "action_plugin.py"), "w") as f:
        f.write(action_plugin_content)
    
    # Create metadata.json
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
        "version": "0.5.0",
        "kicad_version": "9.0",
        "platforms": ["linux", "windows", "macos"],
        "tags": ["import", "computer vision", "automation", "pdf", "schematic"]
    }
    
    with open(os.path.join(target_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)
    
    # Create icon.png
    icon_path = os.path.join(target_dir, "resources", "icons", "icon.png")
    if not os.path.exists(icon_path):
        # Check if resources/icons/icon.png exists
        src_icon_path = os.path.join(current_dir, "resources", "icons", "icon.png")
        if os.path.exists(src_icon_path):
            # Copy resources/icons/icon.png to the target directory
            shutil.copy2(src_icon_path, icon_path)
        else:
            # Create a placeholder icon.png
            with open(icon_path, "wb") as f:
                # This is a minimal 16x16 PNG file (a red square)
                f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00\x90\x91h6\x00\x00\x00\x0cIDATx\x9cc\xf8\xff\xff?\x03\x9d\x01\x00\x08\xfc\x02\xfe\xa7\xa7\xa9\x83\x00\x00\x00\x00IEND\xaeB`\x82')
    
    print(f"Advanced Schematic Importer plugin installed to: {target_dir}")
    print("\nTo use the plugin:")
    print("1. Start KiCad")
    print("2. Open PCB Editor")
    print("3. Look for 'Advanced Schematic Importer' in the Tools menu or toolbar")
    print("\nIf KiCad is already running, please restart it to load the plugin.")

if __name__ == "__main__":
    # Install dependencies
    if install_dependencies():
        # Install the plugin
        install_advanced_plugin()
    else:
        print("Failed to install dependencies. Plugin installation aborted.")
