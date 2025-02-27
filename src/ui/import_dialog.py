import wx
import os
from ..utils.image_processor import ImageProcessor

class ImportDialog(wx.Dialog):
    def __init__(self, parent, board):
        super(ImportDialog, self).__init__(parent, title="Import Schematic", 
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        
        self.board = board
        self.image_processor = ImageProcessor()
        self.setup_ui()
    
    def setup_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # File selection
        file_box = wx.StaticBox(self, label="Image Selection")
        file_sizer = wx.StaticBoxSizer(file_box, wx.VERTICAL)
        
        self.file_picker = wx.FilePickerCtrl(self, wildcard="Image files|*.png;*.jpg;*.jpeg;*.svg")
        file_sizer.Add(self.file_picker, 0, wx.EXPAND|wx.ALL, 5)
        
        # Conversion section
        conv_box = wx.StaticBox(self, label="Image Conversion")
        conv_sizer = wx.StaticBoxSizer(conv_box, wx.VERTICAL)
        
        self.conv_text = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)
        conv_sizer.Add(self.conv_text, 1, wx.EXPAND|wx.ALL, 5)
        
        self.convert_btn = wx.Button(self, label="Show Conversion Commands")
        self.convert_btn.Bind(wx.EVT_BUTTON, self.on_show_conversion)
        conv_sizer.Add(self.convert_btn, 0, wx.ALL, 5)
        
        self.svg_picker = wx.FilePickerCtrl(self, wildcard="SVG files|*.svg")
        conv_sizer.Add(self.svg_picker, 0, wx.EXPAND|wx.ALL, 5)
        
        # Add to main sizer
        main_sizer.Add(file_sizer, 0, wx.EXPAND|wx.ALL, 5)
        main_sizer.Add(conv_sizer, 1, wx.EXPAND|wx.ALL, 5)
        
        # Standard dialog buttons
        button_sizer = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        main_sizer.Add(button_sizer, 0, wx.EXPAND|wx.ALL, 5)
        
        self.SetSizer(main_sizer)
    
    def on_show_conversion(self, event):
        input_path = self.file_picker.GetPath()
        if not input_path:
            wx.MessageBox("Please select an input file first", "Error")
            return
            
        output_path = os.path.splitext(input_path)[0] + ".svg"
        try:
            instructions = self.image_processor.convert_to_svg(input_path, output_path)
            self.conv_text.SetValue(instructions)
        except Exception as e:
            wx.MessageBox(str(e), "Error")
    
    def get_file_paths(self):
        """Get both original and converted file paths"""
        return {
            'original': self.file_picker.GetPath(),
            'converted': self.svg_picker.GetPath()
        }
