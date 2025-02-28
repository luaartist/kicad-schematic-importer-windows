import pcbnew
import wx
import logging
from pathlib import Path
from ..utils.alternative_image_processor import AlternativeImageProcessor
from ..ui.import_dialog import ImportDialog
from ..debug.debug_plugin import DebugManager

class SchematicImporterPlugin(pcbnew.ActionPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Schematic Importer"
        self.category = "Import"
        self.description = "Import schematics from images using computer vision"
        self.show_toolbar_button = True
        self.icon_file_name = ""  # Remove icon reference to allow plugin to load without an icon
        self.processor = AlternativeImageProcessor()
        self.debug = DebugManager.get()  # Use the plugin version

    def Run(self):
        try:
            # Initialize debug logging
            self.debug.show_window()
            self.debug.log_message("Starting schematic import plugin")
            
            # Get the current board
            board = pcbnew.GetBoard()
            if not board:
                self.debug.log_message("No board loaded", logging.ERROR)
                wx.MessageBox("Please open a PCB file first", "Error", wx.OK | wx.ICON_ERROR)
                return
            
            # Create and show the import dialog
            dialog = ImportDialog(None, board)
            result = dialog.ShowModal()
            
            if result == wx.ID_OK:
                try:
                    # Process the vector file
                    file_path = dialog.get_file_path()
                    self.debug.log_message(f"Processing file: {file_path}")
                    
                    processed_path = self.processor.process_vector_file(file_path)
                    self.debug.log_message("File processing completed")
                    
                    self.import_schematic(board, processed_path)
                    pcbnew.Refresh()
                    self.debug.log_message("Import completed successfully")
                    
                except Exception as e:
                    error_msg = f"Error importing schematic: {str(e)}"
                    self.debug.log_message(error_msg, logging.ERROR)
                    wx.MessageBox(error_msg, "Import Error", wx.OK | wx.ICON_ERROR)
            
            dialog.Destroy()
            
        except Exception as e:
            error_msg = f"Plugin error: {str(e)}"
            self.debug.log_message(error_msg, logging.ERROR)
            wx.MessageBox(error_msg, "Error", wx.OK | wx.ICON_ERROR)

    def import_schematic(self, board, svg_path):
        """Import the SVG schematic into the board"""
        self.debug.log_message(f"Importing schematic from {svg_path}")
        
        try:
            # Implementation will go here
            # For now, just log that we reached this point
            self.debug.log_message("Import implementation pending")
            pass
            
        except Exception as e:
            self.debug.log_message(f"Import failed: {str(e)}", logging.ERROR)
            raise

# Register the plugin
SchematicImporterPlugin().register()
