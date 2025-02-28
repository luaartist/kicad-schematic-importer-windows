import os
import logging
from pathlib import Path
import pcbnew
import wx

from ..utils.alternative_image_processor import AlternativeImageProcessor
from ..utils.kicad_processor import KicadProcessor

class SchematicImporter(pcbnew.ActionPlugin):
    """KiCad plugin for importing schematics from images"""
    
    def __init__(self):
        super().__init__()
        self.name = "Schematic Importer"
        self.category = "Import"
        self.description = "Import schematics from images with component recognition"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                         "..", "resources", "icons", "icon.png")
        
        # Initialize processors
        self.image_processor = AlternativeImageProcessor()
        self.kicad_processor = KicadProcessor()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # Add console handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
    
    def Run(self):
        """Run the plugin"""
        # Create dialog
        dialog = wx.FileDialog(
            None,
            message="Choose an image file",
            wildcard="Image files (*.png;*.jpg;*.jpeg;*.bmp;*.pdf)|*.png;*.jpg;*.jpeg;*.bmp;*.pdf",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )
        
        if dialog.ShowModal() == wx.ID_OK:
            image_path = dialog.GetPath()
            self.logger.info(f"Selected file: {image_path}")
            
            try:
                # Clean up any existing test/debug files
                self._cleanup_test_files()
                
                # Process image to SVG
                self.logger.info("Converting image to SVG...")
                svg_path = self.image_processor.vectorize_image(image_path)
                if not svg_path:
                    wx.MessageBox("Failed to process image", "Error", wx.OK | wx.ICON_ERROR)
                    return
                
                # Import SVG to KiCad
                self.logger.info("Importing SVG to KiCad...")
                pcb_path = self.kicad_processor.import_svg(svg_path)
                if not pcb_path:
                    wx.MessageBox("Failed to import SVG", "Error", wx.OK | wx.ICON_ERROR)
                    return
                
                # Load the PCB file
                board = pcbnew.LoadBoard(pcb_path)
                if not board:
                    wx.MessageBox("Failed to load PCB file", "Error", wx.OK | wx.ICON_ERROR)
                    return
                
                # Update current board
                current_board = pcbnew.GetBoard()
                if current_board:
                    # Copy elements from imported board to current board
                    for item in board.GetTracks():
                        current_board.Add(item.Duplicate())
                    for item in board.GetFootprints():
                        current_board.Add(item.Duplicate())
                    for item in board.GetDrawings():
                        current_board.Add(item.Duplicate())
                    
                    # Refresh display
                    pcbnew.Refresh()
                    
                    # Show success message with statistics
                    stats = f"Imported:\n"
                    stats += f"- {len(board.GetTracks())} tracks\n"
                    stats += f"- {len(board.GetFootprints())} footprints\n"
                    stats += f"- {len(board.GetDrawings())} drawings"
                    wx.MessageBox(stats, "Import Successful", wx.OK | wx.ICON_INFORMATION)
                else:
                    wx.MessageBox("No active board", "Error", wx.OK | wx.ICON_ERROR)
            
            except Exception as e:
                self.logger.error(f"Error during import: {e}")
                wx.MessageBox(f"Error during import: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()
    
    def _cleanup_test_files(self):
        """Clean up any test or debug files"""
        try:
            # Get plugin directory
            plugin_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Clean up test directories
            test_dirs = [
                os.path.join(plugin_dir, "..", "..", "tests", "test_files"),
                os.path.join(plugin_dir, "..", "..", "debug")
            ]
            
            for test_dir in test_dirs:
                if os.path.exists(test_dir):
                    self.logger.info(f"Cleaning up test directory: {test_dir}")
                    for file in os.listdir(test_dir):
                        file_path = os.path.join(test_dir, file)
                        try:
                            if os.path.isfile(file_path):
                                os.unlink(file_path)
                            elif os.path.isdir(file_path):
                                os.rmdir(file_path)
                        except Exception as e:
                            self.logger.warning(f"Error cleaning up {file_path}: {e}")
                    
                    try:
                        os.rmdir(test_dir)
                    except Exception as e:
                        self.logger.warning(f"Error removing directory {test_dir}: {e}")
        
        except Exception as e:
            self.logger.warning(f"Error during cleanup: {e}")

# Register the plugin
SchematicImporter().register()
