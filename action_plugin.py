import pcbnew
import wx
import os
import sys
import re
import math
import tempfile
from pathlib import Path
import xml.etree.ElementTree as ET

# Add the plugin directory to the Python path
plugin_dir = os.path.dirname(os.path.abspath(__file__))
if plugin_dir not in sys.path:
    sys.path.insert(0, plugin_dir)

from src.utils.alternative_image_processor import AlternativeImageProcessor
from src.ui.import_dialog import ImportDialog

# Component definitions for recognition
COMPONENT_PATTERNS = {
    "resistor": {
        "pattern": r"(R|Resistor|res)",
        "footprint": "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
        "symbol": "Device:R"
    },
    "capacitor": {
        "pattern": r"(C|Capacitor|cap)",
        "footprint": "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm",
        "symbol": "Device:C"
    },
    "inductor": {
        "pattern": r"(L|Inductor|ind)",
        "footprint": "Inductor_THT:L_Axial_L5.3mm_D2.2mm_P10.16mm_Horizontal_Vishay_IM-1",
        "symbol": "Device:L"
    },
    "diode": {
        "pattern": r"(D|Diode)",
        "footprint": "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal",
        "symbol": "Device:D"
    },
    "led": {
        "pattern": r"(LED)",
        "footprint": "LED_THT:LED_D5.0mm",
        "symbol": "Device:LED"
    },
    "transistor": {
        "pattern": r"(Q|Transistor|NPN|PNP)",
        "footprint": "Package_TO_SOT_THT:TO-92_Inline",
        "symbol": "Device:Q_NPN_EBC"
    },
    "ic": {
        "pattern": r"(IC|U|Chip)",
        "footprint": "Package_DIP:DIP-8_W7.62mm",
        "symbol": "Device:IC"
    }
}

class SchematicImporter(pcbnew.ActionPlugin):
    """
    A plugin to import schematics from images using computer vision
    """
    def __init__(self):
        super().__init__()
        self.processor = AlternativeImageProcessor()
        self.components = []
        self.connections = []
        
    def defaults(self):
        self.name = "Schematic Importer"
        self.category = "Import"
        self.description = "Import schematics from images using computer vision"
        self.show_toolbar_button = True
        # Set the icon file path
        self.icon_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "icons", "icon.png")

    def Run(self):
        # Get the current board
        board = pcbnew.GetBoard()
        
        # Create and show the import dialog
        dialog = ImportDialog(None, board)
        result = dialog.ShowModal()
        
        if result == wx.ID_OK:
            try:
                # Get the selected file path
                file_path = dialog.get_file_path()
                
                # Check if the file is already an SVG
                if file_path.lower().endswith('.svg'):
                    svg_path = file_path
                else:
                    # Vectorize the image
                    progress_dialog = wx.ProgressDialog(
                        "Processing Image",
                        "Vectorizing image... This may take a moment.",
                        maximum=100,
                        parent=None,
                        style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
                    )
                    progress_dialog.Update(10, "Preprocessing image...")
                    
                    # Vectorize the image
                    svg_path = self.processor.vectorize_image(file_path)
                    progress_dialog.Update(50, "Detecting components...")
                    
                    # Detect components and connections
                    self.detect_components(svg_path)
                    progress_dialog.Update(80, "Tracing connections...")
                    
                    self.trace_connections(svg_path)
                    progress_dialog.Update(100, "Import complete!")
                    progress_dialog.Destroy()
                
                # Import the SVG into the board
                self.import_schematic(board, svg_path)
                
                # Refresh the board view
                pcbnew.Refresh()
                
                # Show summary dialog
                summary = f"Import Summary:\n\n"
                summary += f"- Source file: {os.path.basename(file_path)}\n"
                summary += f"- Components detected: {len(self.components)}\n"
                summary += f"- Connections traced: {len(self.connections)}\n\n"
                summary += "Components were placed on the board."
                
                wx.MessageBox(summary, "Import Complete", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error importing schematic: {str(e)}", 
                            "Import Error", wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()

    def detect_components(self, svg_path):
        """Detect components in the SVG file"""
        self.components = []
        
        try:
            # Parse the SVG file
            tree = ET.parse(svg_path)
            root = tree.getroot()
            
            # Find all path elements
            paths = root.findall(".//{http://www.w3.org/2000/svg}path") + root.findall(".//{http://www.w3.org/2000/svg}rect")
            
            # Process each path
            for i, path in enumerate(paths):
                # Get the path data
                if path.tag.endswith("path"):
                    d = path.get("d", "")
                    # Calculate bounding box
                    points = self._parse_path_data(d)
                    if not points:
                        continue
                    
                    x_coords = [p[0] for p in points]
                    y_coords = [p[1] for p in points]
                    
                    x_min, x_max = min(x_coords), max(x_coords)
                    y_min, y_max = min(y_coords), max(y_coords)
                    
                    width = x_max - x_min
                    height = y_max - y_min
                    
                    # Center point
                    center_x = (x_min + x_max) / 2
                    center_y = (y_min + y_max) / 2
                else:  # rect
                    x = float(path.get("x", "0"))
                    y = float(path.get("y", "0"))
                    width = float(path.get("width", "0"))
                    height = float(path.get("height", "0"))
                    
                    x_min, y_min = x, y
                    x_max, y_max = x + width, y + height
                    
                    # Center point
                    center_x = x + width / 2
                    center_y = y + height / 2
                
                # Determine component type based on aspect ratio and size
                component_type = self._identify_component_type(width, height)
                
                # Add component to the list
                component = {
                    "id": f"C{i+1}",
                    "type": component_type,
                    "x": center_x,
                    "y": center_y,
                    "width": width,
                    "height": height,
                    "bbox": (x_min, y_min, x_max, y_max)
                }
                
                self.components.append(component)
            
            print(f"Detected {len(self.components)} components")
            return self.components
        except Exception as e:
            print(f"Error detecting components: {e}")
            return []

    def _parse_path_data(self, d):
        """Parse SVG path data to extract points"""
        points = []
        
        # Simple regex to extract coordinates
        pattern = r"[ML]\s*(-?\d+\.?\d*)[,\s](-?\d+\.?\d*)"
        matches = re.findall(pattern, d)
        
        for match in matches:
            x, y = float(match[0]), float(match[1])
            points.append((x, y))
        
        return points

    def _identify_component_type(self, width, height):
        """Identify component type based on dimensions"""
        aspect_ratio = width / height if height != 0 else 999
        
        if 0.8 <= aspect_ratio <= 1.2:
            if width < 20:
                return "ic"  # Small square - likely an IC
            else:
                return "ic"  # Larger square - could be a microcontroller
        elif aspect_ratio > 3 or aspect_ratio < 0.33:
            return "resistor"  # Very elongated - likely a resistor
        elif 1.5 <= aspect_ratio <= 2.5 or 0.4 <= aspect_ratio <= 0.67:
            return "capacitor"  # Moderately elongated - could be a capacitor
        else:
            return "unknown"  # Default

    def trace_connections(self, svg_path):
        """Trace connections between components"""
        self.connections = []
        
        try:
            # Parse the SVG file
            tree = ET.parse(svg_path)
            root = tree.getroot()
            
            # Find all path elements that could be connections (lines)
            paths = root.findall(".//{http://www.w3.org/2000/svg}path") + root.findall(".//{http://www.w3.org/2000/svg}line")
            
            # Process each path
            for i, path in enumerate(paths):
                if path.tag.endswith("path"):
                    # Get the path data
                    d = path.get("d", "")
                    
                    # Check if this is a line (connection)
                    if "L" in d and d.count("L") == 1 and d.count("M") == 1:
                        # Extract start and end points
                        points = self._parse_path_data(d)
                        if len(points) != 2:
                            continue
                        
                        start_point, end_point = points
                        
                        # Find components at the start and end points
                        start_component = self._find_component_at_point(start_point)
                        end_component = self._find_component_at_point(end_point)
                        
                        if start_component and end_component and start_component != end_component:
                            # Add connection to the list
                            connection = {
                                "id": f"W{i+1}",
                                "start_component": start_component["id"],
                                "end_component": end_component["id"],
                                "start_point": start_point,
                                "end_point": end_point
                            }
                            
                            self.connections.append(connection)
                elif path.tag.endswith("line"):
                    # Get line coordinates
                    x1 = float(path.get("x1", "0"))
                    y1 = float(path.get("y1", "0"))
                    x2 = float(path.get("x2", "0"))
                    y2 = float(path.get("y2", "0"))
                    
                    start_point = (x1, y1)
                    end_point = (x2, y2)
                    
                    # Find components at the start and end points
                    start_component = self._find_component_at_point(start_point)
                    end_component = self._find_component_at_point(end_point)
                    
                    if start_component and end_component and start_component != end_component:
                        # Add connection to the list
                        connection = {
                            "id": f"W{i+1}",
                            "start_component": start_component["id"],
                            "end_component": end_component["id"],
                            "start_point": start_point,
                            "end_point": end_point
                        }
                        
                        self.connections.append(connection)
            
            print(f"Traced {len(self.connections)} connections")
            return self.connections
        except Exception as e:
            print(f"Error tracing connections: {e}")
            return []

    def _find_component_at_point(self, point):
        """Find a component that contains the given point"""
        x, y = point
        
        for component in self.components:
            x_min, y_min, x_max, y_max = component["bbox"]
            
            # Add a small margin for connection points
            margin = 5
            x_min -= margin
            y_min -= margin
            x_max += margin
            y_max += margin
            
            if x_min <= x <= x_max and y_min <= y <= y_max:
                return component
        
        return None

    def import_schematic(self, board, svg_path):
        """Import the SVG schematic into the board"""
        try:
            # Clear existing components and connections
            if hasattr(self, 'placed_components'):
                for component_id, footprint in self.placed_components.items():
                    board.Remove(footprint)
            
            self.placed_components = {}
            
            # Create a text item on the board to show the import was successful
            title_text = pcbnew.PCB_TEXT(board)
            title_text.SetText(f"Imported from {os.path.basename(svg_path)}")
            title_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(10), pcbnew.FromMM(10)))
            title_text.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(2), pcbnew.FromMM(2)))
            board.Add(title_text)
            
            # Place components on the board
            for component in self.components:
                # Create a footprint
                footprint_name = self._get_footprint_for_component(component["type"])
                footprint_lib = footprint_name.split(":")[0]
                footprint = pcbnew.FootprintLoad(footprint_lib, footprint_name.split(":")[1])
                
                if footprint:
                    # Set position
                    x_mm = component["x"] / 10  # Convert to mm (assuming SVG units are in 0.1mm)
                    y_mm = component["y"] / 10
                    footprint.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x_mm), pcbnew.FromMM(y_mm)))
                    
                    # Set reference
                    footprint.SetReference(component["id"])
                    
                    # Set value
                    footprint.SetValue(component["type"].upper())
                    
                    # Add to board
                    board.Add(footprint)
                    
                    # Store for later
                    self.placed_components[component["id"]] = footprint
            
            # Add connections (tracks)
            for connection in self.connections:
                # Get start and end points
                start_x, start_y = connection["start_point"]
                end_x, end_y = connection["end_point"]
                
                # Convert to mm
                start_x_mm = start_x / 10
                start_y_mm = start_y / 10
                end_x_mm = end_x / 10
                end_y_mm = end_y / 10
                
                # Create a track
                track = pcbnew.PCB_TRACK(board)
                track.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(start_x_mm), pcbnew.FromMM(start_y_mm)))
                track.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(end_x_mm), pcbnew.FromMM(end_y_mm)))
                track.SetWidth(pcbnew.FromMM(0.2))  # 0.2mm track width
                
                # Add to board
                board.Add(track)
            
            return True
        except Exception as e:
            print(f"Error in import_schematic: {e}")
            # Still add a text item to show something happened
            text = pcbnew.PCB_TEXT(board)
            text.SetText(f"Imported from {os.path.basename(svg_path)} (with errors)")
            text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(100), pcbnew.FromMM(100)))
            text.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(5), pcbnew.FromMM(5)))
            board.Add(text)
            return False

    def _get_footprint_for_component(self, component_type):
        """Get the appropriate footprint for a component type"""
        # Default footprints for common components
        footprints = {
            "resistor": "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
            "capacitor": "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm",
            "inductor": "Inductor_THT:L_Axial_L5.3mm_D2.2mm_P10.16mm_Horizontal_Vishay_IM-1",
            "diode": "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal",
            "led": "LED_THT:LED_D5.0mm",
            "transistor": "Package_TO_SOT_THT:TO-92_Inline",
            "ic": "Package_DIP:DIP-8_W7.62mm",
            "unknown": "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal"
        }
        
        return footprints.get(component_type.lower(), footprints["unknown"])

# Register the plugin
SchematicImporter().register()
