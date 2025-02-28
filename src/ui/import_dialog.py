import wx
import os

class ImportDialog(wx.Dialog):
    """Dialog for importing schematics from images"""
    
    def __init__(self, parent, board):
        """Initialize the dialog"""
        super().__init__(parent, title="Import Schematic from Image", 
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        
        self.board = board
        self.file_path = ""
        
        # Create the dialog layout
        self.create_layout()
        
        # Set the dialog size
        self.SetSize((500, 300))
        
        # Center the dialog on the screen
        self.Centre()
    
    def create_layout(self):
        """Create the dialog layout"""
        # Create a vertical box sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add a file picker
        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        file_label = wx.StaticText(self, label="Image File:")
        self.file_picker = wx.FilePickerCtrl(self, message="Select an image file",
                                            wildcard="Image files (*.png;*.jpg;*.jpeg;*.bmp;*.svg)|*.png;*.jpg;*.jpeg;*.bmp;*.svg")
        file_sizer.Add(file_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        file_sizer.Add(self.file_picker, 1, wx.EXPAND)
        main_sizer.Add(file_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Add a description
        description = wx.StaticText(self, label="Select an image file containing a schematic to import.\n"
                                               "Supported formats: PNG, JPG, BMP, SVG")
        main_sizer.Add(description, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        # Add a spacer
        main_sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.ALL, 10)
        
        # Add the buttons
        button_sizer = wx.StdDialogButtonSizer()
        self.ok_button = wx.Button(self, wx.ID_OK)
        self.cancel_button = wx.Button(self, wx.ID_CANCEL)
        button_sizer.AddButton(self.ok_button)
        button_sizer.AddButton(self.cancel_button)
        button_sizer.Realize()
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Bind events
        self.file_picker.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_file_changed)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        
        # Set the sizer
        self.SetSizer(main_sizer)
    
    def on_file_changed(self, event):
        """Handle file picker change event"""
        self.file_path = event.GetPath()
    
    def on_ok(self, event):
        """Handle OK button click event"""
        if not self.file_path:
            wx.MessageBox("Please select an image file.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        if not os.path.exists(self.file_path):
            wx.MessageBox("The selected file does not exist.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        event.Skip()
    
    def get_file_path(self):
        """Get the selected file path"""
        return self.file_path
