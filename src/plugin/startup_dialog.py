import wx

class StartupModeDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="KiCad Plugin Mode Selection", size=(400, 300))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Header
        header = wx.StaticText(panel, label="Choose Operating Mode")
        header.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        vbox.Add(header, 0, wx.ALL | wx.CENTER, 10)
        
        # Mode selection buttons
        modes_box = wx.StaticBox(panel, label="Available Modes")
        modes_sizer = wx.StaticBoxSizer(modes_box, wx.VERTICAL)
        
        # Beginner Mode
        beginner_btn = wx.Button(panel, label="Beginner Mode")
        beginner_btn.SetToolTip("Simplified interface with guided assistance")
        modes_sizer.Add(beginner_btn, 0, wx.ALL | wx.EXPAND, 5)
        
        # Advanced Mode
        advanced_btn = wx.Button(panel, label="Advanced Mode")
        advanced_btn.SetToolTip("Full features with detailed controls")
        modes_sizer.Add(advanced_btn, 0, wx.ALL | wx.EXPAND, 5)
        
        # Developer Mode
        developer_btn = wx.Button(panel, label="Developer Mode")
        developer_btn.SetToolTip("Debug features and development tools")
        modes_sizer.Add(developer_btn, 0, wx.ALL | wx.EXPAND, 5)
        
        vbox.Add(modes_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # Remember choice checkbox
        self.remember_choice = wx.CheckBox(panel, label="Remember my choice")
        vbox.Add(self.remember_choice, 0, wx.ALL | wx.CENTER, 5)
        
        # Bind events
        beginner_btn.Bind(wx.EVT_BUTTON, lambda evt: self.on_mode_selected("beginner"))
        advanced_btn.Bind(wx.EVT_BUTTON, lambda evt: self.on_mode_selected("advanced"))
        developer_btn.Bind(wx.EVT_BUTTON, lambda evt: self.on_mode_selected("developer"))
        
        panel.SetSizer(vbox)
        
    def on_mode_selected(self, mode):
        self.selected_mode = mode
        self.remember = self.remember_choice.GetValue()
        self.EndModal(wx.ID_OK)