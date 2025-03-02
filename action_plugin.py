import pcbnew
import wx
import os
import sys
from pathlib import Path

# Add the plugin directory to the Python path
plugin_dir = os.path.dirname(os.path.abspath(__file__))
if plugin_dir not in sys.path:
    sys.path.insert(0, plugin_dir)

from src.utils.alternative_image_processor import AlternativeImageProcessor

class SchematicImporter(pcbnew.ActionPlugin):
    def __init__(self):
        super().__init__()
        self.processor = AlternativeImageProcessor()
        
    def defaults(self):
        self.name = "Schematic Importer"
        self.category = "Import"
        self.description = "Import schematics from images using computer vision"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                         "resources", "icons", "icon.png")

    def Run(self):
        board = pcbnew.GetBoard()
        
        # Create and show file dialog
        wildcard = "Image files (*.png;*.jpg;*.jpeg)|*.png;*.jpg;*.jpeg"
        dialog = wx.FileDialog(None, "Choose an image file", "", "", 
                             wildcard, wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        
        if dialog.ShowModal() == wx.ID_OK:
            try:
                file_path = dialog.GetPath()
                
                # Process the image and get component data
                components = self.processor.process_image(file_path)
                
                # Create components on the board
                for component in components:
                    # Create footprint
                    footprint = pcbnew.FootprintLoad(self.get_lib_path(), component.footprint)
                    if footprint:
                        # Set position
                        position = pcbnew.VECTOR2I(
                            pcbnew.FromMM(component.x),
                            pcbnew.FromMM(component.y)
                        )
                        footprint.SetPosition(position)
                        
                        # Set rotation
                        footprint.SetOrientation(component.rotation * 10)  # KiCad uses decidegrees
                        
                        # Add to board
                        board.Add(footprint)
                
                # Create tracks/connections
                for connection in self.processor.get_connections():
                    track = pcbnew.PCB_TRACK(board)
                    track.SetStart(pcbnew.VECTOR2I(
                        pcbnew.FromMM(connection.start_x),
                        pcbnew.FromMM(connection.start_y)
                    ))
                    track.SetEnd(pcbnew.VECTOR2I(
                        pcbnew.FromMM(connection.end_x),
                        pcbnew.FromMM(connection.end_y)
                    ))
                    track.SetWidth(pcbnew.FromMM(0.2))  # Default track width
                    board.Add(track)
                
                # Add import marker
                text = pcbnew.PCB_TEXT(board)
                text.SetText(f"Imported from {os.path.basename(file_path)}")
                text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(10), pcbnew.FromMM(10)))
                text.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(2), pcbnew.FromMM(2)))
                board.Add(text)
                
                # Refresh the board view
                pcbnew.Refresh()
                
                wx.MessageBox(
                    f"Successfully imported {len(components)} components from {os.path.basename(file_path)}", 
                    "Import Complete", 
                    wx.OK | wx.ICON_INFORMATION
                )
            except Exception as e:
                wx.MessageBox(f"Error importing schematic: {str(e)}", 
                            "Import Error", wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()

    def get_lib_path(self):
        """Get the KiCad library path"""
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "library"
        )

# Register the plugin
SchematicImporter().register()
