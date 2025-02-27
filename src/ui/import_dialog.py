import wx
import os
import pcbnew
from ..integration.kicad_integration import KiCadSchematicGenerator

class ImportDialog(wx.Dialog):
    def __init__(self, parent, board):
        super(ImportDialog, self).__init__(parent, title="Import Schematic from Image", 
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.board = board
        self.generator = KiCadSchematicGenerator()
        
        # Create main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add image selection
        img_box = wx.StaticBox(self, label="Image Selection")
        img_sizer = wx.StaticBoxSizer(img_box, wx.VERTICAL)
        
        self.img_path = wx.TextCtrl(self)
        browse_btn = wx.Button(self, label="Browse...")
        browse_btn.Bind(wx.EVT_BUTTON, self.on_browse_image)
        
        img_path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        img_path_sizer.Add(self.img_path, 1, wx.EXPAND|wx.ALL, 5)
        img_path_sizer.Add(browse_btn, 0, wx.ALL, 5)
        img_sizer.Add(img_path_sizer, 0, wx.EXPAND)
        
        # Add output directory selection
        out_box = wx.StaticBox(self, label="Output Directory")
        out_sizer = wx.StaticBoxSizer(out_box, wx.VERTICAL)
        
        self.out_path = wx.TextCtrl(self)
        browse_out_btn = wx.Button(self, label="Browse...")
        browse_out_btn.Bind(wx.EVT_BUTTON, self.on_browse_output)
        
        out_path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        out_path_sizer.Add(self.out_path, 1, wx.EXPAND|wx.ALL, 5)
        out_path_sizer.Add(browse_out_btn, 0, wx.ALL, 5)
        out_sizer.Add(out_path_sizer, 0, wx.EXPAND)
        
        # Add processing options
        opt_box = wx.StaticBox(self, label="Processing Options")
        opt_sizer = wx.StaticBoxSizer(opt_box, wx.VERTICAL)
        
        self.detect_components = wx.CheckBox(self, label="Detect Components")
        self.detect_connections = wx.CheckBox(self, label="Detect Connections")
        self.detect_components.SetValue(True)
        self.detect_connections.SetValue(True)
        
        opt_sizer.Add(self.detect_components, 0, wx.ALL, 5)
        opt_sizer.Add(self.detect_connections, 0, wx.ALL, 5)
        
        # Add buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, wx.ID_OK, "Process")
        cancel_button = wx.Button(self, wx.ID_CANCEL, "Cancel")
        button_sizer.Add(ok_button, 0, wx.ALL, 5)
        button_sizer.Add(cancel_button, 0, wx.ALL, 5)
        
        # Add progress gauge
        self.progress = wx.Gauge(self, range=100)
        
        # Add all sizers to main sizer
        main_sizer.Add(img_sizer, 0, wx.EXPAND|wx.ALL, 5)
        main_sizer.Add(out_sizer, 0, wx.EXPAND|wx.ALL, 5)
        main_sizer.Add(opt_sizer, 0, wx.EXPAND|wx.ALL, 5)
        main_sizer.Add(self.progress, 0, wx.EXPAND|wx.ALL, 5)
        main_sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        
        self.SetSizer(main_sizer)
        self.Fit()
        
        # Bind events
        self.Bind(wx.EVT_BUTTON, self.on_ok, id=wx.ID_OK)
        
    def on_browse_image(self, event):
        with wx.FileDialog(self, "Select Schematic Image", 
                         wildcard="All supported files|*.svg;*.pdf;*.eps;*.png;*.jpg;*.jpeg;*.tiff",
                         style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            
            try:
                image_path = dialog.GetPath()
                image_info = self.generator.validate_image(image_path)
                
                if image_info['needs_conversion']:
                    msg = "This image will need to be converted to vector format for best results. Continue?"
                    if image_info.get('dpi'):
                        msg += f"\nCurrent resolution: {image_info['dpi']} DPI"
                    
                    dlg = wx.MessageDialog(self, msg, "Image Conversion Required",
                                         wx.YES_NO | wx.ICON_INFORMATION)
                    if dlg.ShowModal() == wx.ID_YES:
                        self.img_path.SetValue(image_path)
                    dlg.Destroy()
                else:
                    self.img_path.SetValue(image_path)
                    
            except ValueError as e:
                wx.MessageBox(str(e), "Invalid Image", wx.OK | wx.ICON_ERROR)
            
    def on_browse_output(self, event):
        with wx.DirDialog(self, "Select Output Directory",
                         style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            self.out_path.SetValue(dialog.GetPath())
            
    def on_ok(self, event):
        try:
            # Get values
            image_path = self.img_path.GetValue()
            output_dir = self.out_path.GetValue()
            
            if not image_path or not output_dir:
                wx.MessageBox("Please select both image and output directory", "Error",
                            wx.OK|wx.ICON_ERROR)
                return
                
            # Initialize generator
            self.generator = KiCadSchematicGenerator(output_dir)
            
            # Process image
            if self.detect_components.GetValue():
                self.progress.SetValue(25)
                wx.CallAfter(self.notify, "Detecting components...")
                components = self.generator.detect_components_from_image(image_path)
                wx.CallAfter(self.notify, f"Detected {len(components)} components")
                
            if self.detect_connections.GetValue():
                self.progress.SetValue(75)
                wx.CallAfter(self.notify, "Detecting connections...")
                connections = self.generator.detect_connections(image_path)
                wx.CallAfter(self.notify, f"Detected {len(connections)} connections")
                
            self.progress.SetValue(100)
            wx.CallAfter(self.notify, "Processing complete!")
            
            event.Skip()
            
        except Exception as e:
            wx.MessageBox(f"Error during processing: {str(e)}", "Error",
                        wx.OK|wx.ICON_ERROR)
            
    def notify(self, message):
        """Show notification to user"""
        dialog = wx.MessageDialog(self, message, "Processing Status", wx.OK|wx.ICON_INFORMATION)
        dialog.ShowModal()
        dialog.Destroy()
