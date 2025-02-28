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
import pcbnew  # import pcbnew

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
    init_content = """# This file makes the directory a Python package
# It allows the plugin to be imported by KiCad

try:
    from .action_plugin import AdvancedSchematicImporter
except Exception as e:
    import traceback
    traceback.print_exc()
"""
    with open(os.path.join(target_dir, "__init__.py"), "w") as f:
        f.write(init_content)
    
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
    
    # Create action_plugin.py
    action_plugin_content = """import pcbnew
import wx
import os
import sys
import cv2
import numpy as np
from pathlib import Path

# Add the plugin directory to the Python path
plugin_dir = os.path.dirname(os.path.abspath(__file__))
if plugin_dir not in sys.path:
    sys.path.insert(0, plugin_dir)

# Import plugin modules
from src.recognition.component_recognizer import ComponentRecognizer
from src.recognition.connection_tracer import ConnectionTracer
from src.utils.pdf_importer import PDFImporter
from src.utils.alternative_image_processor import AlternativeImageProcessor
from src.utils.path_validator import PathValidator

class AdvancedSchematicImporter(pcbnew.ActionPlugin):
    \"\"\"
    Advanced Schematic Importer plugin for KiCad
    \"\"\"
    def __init__(self):
        super().__init__()
        self.component_recognizer = ComponentRecognizer()
        self.connection_tracer = ConnectionTracer()
        self.pdf_importer = PDFImporter()
        self.image_processor = AlternativeImageProcessor()
        self.path_validator = PathValidator()
        self.components = []
        self.connections = []
        
    def defaults(self):
        self.name = "Advanced Schematic Importer"
        self.category = "Import"
        self.description = "Import schematics from images with advanced features"
        self.show_toolbar_button = True
        # Set the icon file path
        self.icon_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                           "resources", "icons", "icon.png")

    def Run(self):
        # Get the current board
        board = pcbnew.GetBoard()
        
        # Create the main dialog
        dialog = wx.Dialog(None, title="Advanced Schematic Importer", size=(500, 400))
        
        # Create a panel
        panel = wx.Panel(dialog)
        
        # Create a vertical box sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add a file picker
        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        file_label = wx.StaticText(panel, label="Input File:")
        self.file_picker = wx.FilePickerCtrl(
            panel, 
            message="Select a file",
            wildcard="All supported files (*.png;*.jpg;*.jpeg;*.bmp;*.svg;*.pdf)|*.png;*.jpg;*.jpeg;*.bmp;*.svg;*.pdf"
        )
        file_sizer.Add(file_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        file_sizer.Add(self.file_picker, 1, wx.EXPAND)
        main_sizer.Add(file_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Add PDF options
        self.pdf_panel = wx.Panel(panel)
        pdf_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Page selection
        page_sizer = wx.BoxSizer(wx.HORIZONTAL)
        page_label = wx.StaticText(self.pdf_panel, label="PDF Page:")
        self.page_spinner = wx.SpinCtrl(self.pdf_panel, min=1, max=1000, initial=1)
        page_sizer.Add(page_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        page_sizer.Add(self.page_spinner, 0)
        pdf_sizer.Add(page_sizer, 0, wx.EXPAND | wx.BOTTOM, 5)
        
        # DPI selection
        dpi_sizer = wx.BoxSizer(wx.HORIZONTAL)
        dpi_label = wx.StaticText(self.pdf_panel, label="DPI:")
        self.dpi_spinner = wx.SpinCtrl(self.pdf_panel, min=72, max=600, initial=300)
        dpi_sizer.Add(dpi_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        dpi_sizer.Add(self.dpi_spinner, 0)
        pdf_sizer.Add(dpi_sizer, 0, wx.EXPAND)
        
        self.pdf_panel.SetSizer(pdf_sizer)
        main_sizer.Add(self.pdf_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        self.pdf_panel.Hide()
        
        # Add processing options
        options_sizer = wx.StaticBoxSizer(wx.VERTICAL, panel, "Processing Options")
        
        # Component recognition
        self.recognize_components_cb = wx.CheckBox(panel, label="Recognize Components")
        self.recognize_components_cb.SetValue(True)
        options_sizer.Add(self.recognize_components_cb, 0, wx.ALL, 5)
        
        # Connection tracing
        self.trace_connections_cb = wx.CheckBox(panel, label="Trace Connections")
        self.trace_connections_cb.SetValue(True)
        options_sizer.Add(self.trace_connections_cb, 0, wx.ALL, 5)
        
        # Text recognition
        self.recognize_text_cb = wx.CheckBox(panel, label="Recognize Text (OCR)")
        self.recognize_text_cb.SetValue(True)
        options_sizer.Add(self.recognize_text_cb, 0, wx.ALL, 5)
        
        main_sizer.Add(options_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        # Add a description
        description = wx.StaticText(
            panel, 
            label="Import schematics from images or PDFs with advanced component recognition and connection tracing."
        )
        main_sizer.Add(description, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        # Add a separator
        main_sizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.ALL, 10)
        
        # Add the buttons
        button_sizer = wx.StdDialogButtonSizer()
        self.ok_button = wx.Button(panel, wx.ID_OK)
        self.cancel_button = wx.Button(panel, wx.ID_CANCEL)
        button_sizer.AddButton(self.ok_button)
        button_sizer.AddButton(self.cancel_button)
        button_sizer.Realize()
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Bind events
        self.file_picker.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_file_changed)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        
        # Set the sizer
        panel.SetSizer(main_sizer)
        
        # Show the dialog
        if dialog.ShowModal() == wx.ID_OK:
            try:
                # Get the selected file path
                file_path = self.file_picker.GetPath()
                
                # Show progress dialog
                progress_dialog = wx.ProgressDialog(
                    "Processing Schematic",
                    "Importing schematic... This may take a moment.",
                    maximum=100,
                    parent=None,
                    style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
                )
                
                # Process the file
                if file_path.lower().endswith('.pdf'):
                    # Process PDF
                    progress_dialog.Update(10, "Processing PDF...")
                    page_number = self.page_spinner.GetValue() - 1  # Convert to 0-based index
                    dpi = self.dpi_spinner.GetValue()
                    
                    # Extract page as image
                    image = self.pdf_importer.extract_page_as_image(file_path, page_number)
                    if image is None:
                        wx.MessageBox("Failed to extract page from PDF.", "Error", wx.OK | wx.ICON_ERROR)
                        progress_dialog.Destroy()
                        dialog.Destroy()
                        return
                    
                    # Preprocess image
                    progress_dialog.Update(30, "Preprocessing image...")
                    preprocessed = self.pdf_importer.preprocess_for_schematic(image)
                    
                    # Save as temporary image
                    temp_image_path = os.path.join(os.path.dirname(file_path), "temp_pdf_page.png")
                    cv2.imwrite(temp_image_path, preprocessed)
                    
                    # Vectorize image
                    progress_dialog.Update(50, "Vectorizing image...")
                    svg_path = self.image_processor.vectorize_image(temp_image_path)
                else:
                    # Process image or SVG
                    progress_dialog.Update(20, "Processing image...")
                    
                    # Check if the file is already an SVG
                    if file_path.lower().endswith('.svg'):
                        svg_path = file_path
                    else:
                        # Vectorize the image
                        progress_dialog.Update(40, "Vectorizing image...")
                        svg_path = self.image_processor.vectorize_image(file_path)
                
                # Recognize components
                if self.recognize_components_cb.IsChecked():
                    progress_dialog.Update(60, "Recognizing components...")
                    # For SVG, we need to convert back to an image for component recognition
                    if svg_path.lower().endswith('.svg'):
                        # Load SVG as image (simplified approach)
                        image = cv2.imread(file_path) if not file_path.lower().endswith('.pdf') else image
                    else:
                        image = cv2.imread(svg_path)
                    
                    if image is not None:
                        self.components = self.component_recognizer.recognize_components(image)
                        
                        # Extract text if enabled
                        if self.recognize_text_cb.IsChecked():
                            progress_dialog.Update(70, "Recognizing text...")
                            self.component_recognizer.extract_text_near_components(image, self.components)
                    
                    # Trace connections
                    if self.trace_connections_cb.IsChecked() and image is not None:
                        progress_dialog.Update(80, "Tracing connections...")
                        self.connections = self.connection_tracer.trace_connections(image, self.components)
                
                # Import to board
                progress_dialog.Update(90, "Importing to board...")
                self.import_to_board(board, svg_path)
                
                # Refresh the board view
                pcbnew.Refresh()
                
                progress_dialog.Update(100, "Import complete!")
                progress_dialog.Destroy()
                
                # Show summary dialog
                summary = f"Import Summary:\\n\\n"
                summary += f"- Source file: {os.path.basename(file_path)}\\n"
                summary += f"- Components detected: {len(self.components)}\\n"
                summary += f"- Connections traced: {len(self.connections)}\\n\\n"
                summary += "Components were placed on the board."
                
                wx.MessageBox(summary, "Import Complete", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                import traceback
                traceback.print_exc()
                wx.MessageBox(f"Error importing schematic: {str(e)}", 
                            "Import Error", wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()
    
    def on_file_changed(self, event):
        \"\"\"Handle file picker change event\"\"\"
        file_path = self.file_picker.GetPath()
        
        # Show/hide PDF options based on file type
        if file_path.lower().endswith('.pdf'):
            self.pdf_panel.Show()
            
            # Update page spinner max value based on PDF page count
            try:
                info = self.pdf_importer.get_pdf_info(file_path)
                page_count = info.get("page_count", 1)
                self.page_spinner.SetMax(page_count)
                self.page_spinner.SetValue(1)  # Reset to first page
            except Exception:
                pass
        else:
            self.pdf_panel.Hide()
        
        # Refresh layout
        self.pdf_panel.GetParent().Layout()
    
    def on_ok(self, event):
        \"\"\"Handle OK button click event\"\"\"
        file_path = self.file_picker.GetPath()
        
        if not file_path:
            wx.MessageBox("Please select a file.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        if not os.path.exists(file_path):
            wx.MessageBox("The selected file does not exist.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        event.Skip()
    
    def import_to_board(self, board, svg_path):
        \"\"\"Import the schematic to the board\"\"\"
        # Create a text item on the board to show the import was successful
        title_text = pcbnew.PCB_TEXT(board)
        title_text.SetText(f"Advanced Import: {os.path.basename(svg_path)}")
        title_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(10), pcbnew.FromMM(10)))
        title_text.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(2), pcbnew.FromMM(2)))
        board.Add(title_text)
        
        # Place components on the board
        for component in self.components:
            # Create a footprint
            footprint = pcbnew.FOOTPRINT(board)
            footprint.SetReference(component["id"])
            footprint.SetValue(component.get("value", component["type"].upper()))
            
            # Set position
            x_mm = component["x"] / 10  # Convert to mm (assuming SVG units are in 0.1mm)
            y_mm = component["y"] / 10
            footprint.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x_mm), pcbnew.FromMM(y_mm)))
            
            # Create pads based on component type
            if component["type"] == "resistor":
                self._create_resistor_pads(footprint)
            elif component["type"] == "capacitor":
                self._create_capacitor_pads(footprint)
            elif component["type"] == "diode":
                self._create_diode_pads(footprint)
            elif component["type"] == "ic":
                self._create_ic_pads(footprint)
            else:
                # Default: create two pads
                self._create_default_pads(footprint)
            
            # Add to board
            board.Add(footprint)
        
        # Add connections (tracks)
        for connection in self.connections:
            if "coordinates" in connection and len(connection["coordinates"]) > 0:
                # Create tracks for each segment of the path
                coords = connection["coordinates"]
                for i in range(len(coords) - 1):
                    x1, y1 = coords[i]
                    x2, y2 = coords[i+1]
                    
                    # Convert to mm
                    x1_mm = x1 / 10
                    y1_mm = y1 / 10
                    x2_mm = x2 / 10
                    y2_mm = y2 / 10
                    
                    # Create a track
                    track = pcbnew.PCB_TRACK(board)
                    track.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1_mm), pcbnew.FromMM(y1_mm)))
                    track.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2_mm), pcbnew.FromMM(y2_mm)))
                    track.SetWidth(pcbnew.FromMM(0.2))  # 0.2mm track width
                    
                    # Add to board
                    board.Add(track)
            else:
                # Create direct connection between components
                comp1_id = connection["start_component"]
                comp2_id = connection["end_component"]
                
                # Find components
                comp1 = next((c for c in self.components if c["id"] == comp1_id), None)
                comp2 = next((c for c in self.components if c["id"] == comp2_id), None)
                
                if comp1 and comp2:
                    # Convert to mm
                    x1_mm = comp1["x"] / 10
                    y1_mm = comp1["y"] / 10
                    x2_mm = comp2["x"] / 10
                    y2_mm = comp2["y"] / 10
                    
                    # Create a track
                    track = pcbnew.PCB_TRACK(board)
                    track.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1_mm), pcbnew.FromMM(y1_mm)))
                    track.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2_mm), pcbnew.FromMM(y2_mm)))
                    track.SetWidth(pcbnew.FromMM(0.2))  # 0.2mm track width
                    
                    # Add to board
                    board.Add(track)
    
    def _create_resistor_pads(self, footprint):
        \"\"\"Create pads for a resistor footprint\"\"\"
        # Create pads
        self._create_pad(footprint, 1, pcbnew.VECTOR2I(pcbnew.FromMM(-5), pcbnew.FromMM(0)))
        self._create_pad(footprint, 2, pcbnew.VECTOR2I(pcbnew.FromMM(5), pcbnew.FromMM(0)))
    
    def _create_capacitor_pads(self, footprint):
        \"\"\"Create pads for a capacitor footprint\"\"\"
        # Create pads
        self._create_pad(footprint, 1, pcbnew.VECTOR2I(pcbnew.FromMM(-2.5), pcbnew.FromMM(0)))
        self._create_pad(footprint, 2, pcbnew.VECTOR2I(pcbnew.FromMM(2.5), pcbnew.FromMM(0)))
    
    def _create_diode_pads(self, footprint):
        \"\"\"Create pads for a diode footprint\"\"\"
        # Create pads
        self._create_pad(footprint, 1, pcbnew.VECTOR2I(pcbnew.FromMM(-3.5), pcbnew.FromMM(0)))
        self._create_pad(footprint, 2, pcbnew.VECTOR2I(pcbnew.FromMM(3.5), pcbnew.FromMM(0)))
    
    def _create_ic_pads(self, footprint):
        \"\"\"Create pads for an IC footprint\"\"\"
        # Create pads for a DIP-8 package
        pad_spacing = pcbnew.FromMM(2.54)
        for i in range(4):
            # Left side pads
            self._create_pad(
                footprint, i+1, 
                pcbnew.VECTOR2I(pcbnew.FromMM(-3.81), pcbnew.FromMM(-3.81 + i * 2.54))
            )
            # Right side pads
            self._create_pad(
                footprint, 8-i, 
                pcbnew.VECTOR2I(pcbnew.FromMM(3.81), pcbnew.FromMM(-3.81 + i * 2.54))
            )
    
    def _create_default_pads(self, footprint):
        \"\"\"Create default pads for a footprint\"\"\"
        # Create pads
        self._create_pad(footprint, 1, pcbnew.VECTOR2I(pcbnew.FromMM(-2.5), pcbnew.FromMM(0)))
        self._create_pad(footprint, 2, pcbnew.VECTOR2I(pcbnew.FromMM(2.5), pcbnew.FromMM(0)))
    
    def _create_pad(self, footprint, pad_num, position):
        \"\"\"Create a pad for a footprint\"\"\"
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
"""
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
            },
            "credentials": {
                "role": "Lead Developer",
                "expertise": [
                    "KiCad Plugin Development",
                    "Computer Vision Integration",
                    "Cross-platform Development"
                ]
            }
        },
        "development": {
            "methodology": "Hybrid AI-Assisted Development",
            "platforms_used": [
                "OpenAI ChatGPT Pro",
                "Anthropic Claude",
                "NinjaTech AI"
            ],
            "development_period": "2024",
            "development_hours": "100+"
        },
        "license": "MIT",
        "copyright": "© 2024 Wallace Lebrun",
        "resources": {
            "homepage": "https://github.com/augmentcode/kicad-schematic-importer"
        },
        "versions": [
            {
                "version": "0.5.0",
                "status": "testing",
                "kicad_version": "9.0",
                "platforms": ["linux", "windows", "macos"]
            }
        ],
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
