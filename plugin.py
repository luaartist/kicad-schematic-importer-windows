import pcbnew
import wx
from pathlib import Path
import os
import sys

# Add the plugin directory to the Python path
plugin_dir = os.path.dirname(os.path.abspath(__file__))
if plugin_dir not in sys.path:
    sys.path.insert(0, plugin_dir)

from src.utils.alternative_image_processor import AlternativeImageProcessor
from src.ui.import_dialog import ImportDialog

class SchematicImporterPlugin(pcbnew.ActionPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Schematic Importer"
        self.category = "Import"
        self.description = "Import schematics from images using computer vision"
        self.show_toolbar_button = True
        # Remove icon reference to allow plugin to load without an icon
        self.icon_file_name = ""
        self.processor = AlternativeImageProcessor()

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
                processed_path = self.processor.process_vector_file(file_path)
                self.import_schematic(board, processed_path)
                pcbnew.Refresh()
            except Exception as e:
                wx.MessageBox(f"Error importing schematic: {str(e)}", 
                            "Import Error", wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()

    def import_schematic(self, board, svg_path):
        """Import the SVG schematic into the board"""
        # Implementation will go here
        pass

# Register the plugin
SchematicImporterPlugin().register()
