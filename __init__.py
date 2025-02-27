import os
import sys

# Try to import KiCad-specific modules, but don't fail if they're not available
try:
    import pcbnew
    import wx
    from .src.core.schematic_importer import SchematicImporter
    from .src.ui.import_dialog import ImportDialog

    class SchematicImporterPlugin(pcbnew.ActionPlugin):
        def defaults(self):
            self.name = "Import Schematic from Image"
            self.category = "Import"
            self.description = "Import schematic from image and create KiCad components"
            self.show_toolbar_button = True
            self.icon_file_name = os.path.join(os.path.dirname(__file__), 'resources/icons/icon.png')
        
        def Run(self):
            # Display the import dialog
            board = pcbnew.GetBoard()
            dialog = ImportDialog(None, board)
            dialog.ShowModal()
            dialog.Destroy()

    # Register the plugin
    SchematicImporterPlugin().register()
except ImportError:
    # KiCad modules not available, skip plugin registration
    pass
