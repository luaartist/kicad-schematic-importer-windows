import os
import wx
import pcbnew

class ImportDialog(wx.Dialog):
    """Dialog for importing schematics from images"""
    
    def __init__(self, parent, board):
        wx.Dialog.__init__(self, parent, title="Import Schematic from Image", 
                          size=(400, 500), style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        
        self.board = board
        self.image_path = None
        self.config = self._load_config()
        
        # Create UI elements
        self._create_ui()
        self._bind_events()
        
        # Center dialog on screen
        self.Center()
    
    def _load_config(self):
        """Load configuration from file"""
        # TODO: Implement proper config loading
        return {
            "last_directory": "",
            "save_debug_images": True
        }
    
    def _create_ui(self):
        """Create the UI elements"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Image selection
        img_box = wx.StaticBox(self, label="Image Selection")
        img_sizer = wx.StaticBoxSizer(img_box, wx.VERTICAL)
        
        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.file_text = wx.TextCtrl(self, style=wx.TE_READONLY)
        browse_btn = wx.Button(self, label="Browse...")
        file_sizer.Add(self.file_text, 1, wx.EXPAND|wx.RIGHT, 5)
        file_sizer.Add(browse_btn, 0)
        
        img_sizer.Add(file_sizer, 0, wx.EXPAND|wx.ALL, 5)
        
        # Preview (placeholder)
        self.preview = wx.StaticBitmap(self, bitmap=wx.NullBitmap, size=(350, 200))
        img_sizer.Add(self.preview, 1, wx.EXPAND|wx.ALL, 5)
        
        main_sizer.Add(img_sizer, 1, wx.EXPAND|wx.ALL, 10)
        
        # Options
        options_box = wx.StaticBox(self, label="Import Options")
        options_sizer = wx.StaticBoxSizer(options_box, wx.VERTICAL)
        
        # AI detection options
        self.use_online = wx.CheckBox(self, label="Use online detection (FLUX.AI)")
        self.fallback_local = wx.CheckBox(self, label="Fallback to local detection if online fails")
        self.save_debug = wx.CheckBox(self, label="Save debug images")
        
        options_sizer.Add(self.use_online, 0, wx.ALL, 5)
        options_sizer.Add(self.fallback_local, 0, wx.ALL, 5)
        options_sizer.Add(self.save_debug, 0, wx.ALL, 5)
        
        main_sizer.Add(options_sizer, 0, wx.EXPAND|wx.ALL, 10)
        
        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        import_btn = wx.Button(self, wx.ID_OK, label="Import")
        cancel_btn = wx.Button(self, wx.ID_CANCEL)
        
        btn_sizer.Add(import_btn, 0, wx.RIGHT, 5)
        btn_sizer.Add(cancel_btn, 0)
        
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT|wx.ALL, 10)
        
        self.SetSizer(main_sizer)
        
        # Set default values
        self.use_online.SetValue(True)
        self.fallback_local.SetValue(True)
        self.save_debug.SetValue(True)
    
    def _bind_events(self):
        """Bind event handlers"""
        self.Bind(wx.EVT_BUTTON, self._on_browse, id=wx.ID_ANY)
        self.Bind(wx.EVT_BUTTON, self._on_import, id=wx.ID_OK)
    
    def _on_browse(self, event):
        """Handle browse button click"""
        wildcard = "Image files (*.png;*.jpg;*.jpeg)|*.png;*.jpg;*.jpeg"
        dlg = wx.FileDialog(self, message="Choose an image file",
                           defaultDir=self.config["last_directory"],
                           defaultFile="",
                           wildcard=wildcard,
                           style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.image_path = dlg.GetPath()
            self.file_text.SetValue(self.image_path)
            self._load_preview(self.image_path)
            
            # Save last directory
            self.config["last_directory"] = os.path.dirname(self.image_path)
        
        dlg.Destroy()
    
    def _load_preview(self, image_path):
        """Load image preview"""
        if os.path.exists(image_path):
            img = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
            
            # Scale image to fit preview area
            preview_size = self.preview.GetSize()
            img_width, img_height = img.GetWidth(), img.GetHeight()
            
            scale_factor = min(preview_size[0]/img_width, preview_size[1]/img_height)
            new_width, new_height = int(img_width * scale_factor), int(img_height * scale_factor)
            
            img = img.Scale(new_width, new_height)
            self.preview.SetBitmap(wx.Bitmap(img))
            self.Layout()
    
    def _on_import(self, event):
        """Handle import button click"""
        if not self.image_path or not os.path.exists(self.image_path):
            wx.MessageBox("Please select a valid image file first.", "Error", wx.OK|wx.ICON_ERROR)
            return
        
        # Get options
        options = {
            "use_online": self.use_online.GetValue(),
            "fallback_local": self.fallback_local.GetValue(),
            "save_debug": self.save_debug.GetValue(),
            "image_path": self.image_path
        }
        
        # TODO: Implement actual import functionality
        wx.MessageBox("Import functionality not yet implemented.", "Information", wx.OK|wx.ICON_INFORMATION)
        
        # Close dialog
        pass
