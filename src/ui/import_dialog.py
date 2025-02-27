import wx
import os
import pcbnew
from ..integration.kicad_integration import KiCadSchematicGenerator

class ImportDialog(wx.Dialog):
    def __init__(self, parent, board):
        super(ImportDialog, self).__init__(parent, title="Import Schematic", 
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.board = board
        self.generator = KiCadSchematicGenerator()
        
        # Create main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add file selection
        file_box = wx.StaticBox(self, label="Vector File Selection")
        file_sizer = wx.StaticBoxSizer(file_box, wx.VERTICAL)
        
        # Add instructions
        instructions = wx.StaticText(self, label=(
            "Please create your schematic using your preferred tool\n"
            "and save it as a vector file (.svg, .dxf, or .eps).\n"
            "Then select the file below to import it."
        ))
        file_sizer.Add(instructions, 0, wx.ALL, 5)
        
        self.file_path = wx.TextCtrl(self)
        browse_btn = wx.Button(self, label="Browse...")
        browse_btn.Bind(wx.EVT_BUTTON, self.on_browse_file)
        
        file_path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        file_path_sizer.Add(self.file_path, 1, wx.EXPAND|wx.ALL, 5)
        file_path_sizer.Add(browse_btn, 0, wx.ALL, 5)
        
        file_sizer.Add(file_path_sizer, 0, wx.EXPAND|wx.ALL, 5)
        main_sizer.Add(file_sizer, 0, wx.EXPAND|wx.ALL, 5)
        
        # Add standard buttons
        button_sizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        main_sizer.Add(button_sizer, 0, wx.EXPAND|wx.ALL, 5)
        
        self.SetSizer(main_sizer)
        self.Fit()
        
    def on_browse_file(self, event):
        with wx.FileDialog(self, "Select Vector File", 
                         wildcard="Vector files (*.svg;*.dxf;*.eps)|*.svg;*.dxf;*.eps",
                         style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            
            try:
                file_path = dialog.GetPath()
                self.file_path.SetValue(file_path)
            except Exception as e:
                wx.MessageBox(f"Error selecting file: {str(e)}", "Error",
                            wx.OK|wx.ICON_ERROR)
    
    def get_file_path(self):
        """Return the selected file path"""
        return self.file_path.GetValue()
