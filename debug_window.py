import wx
import os
from debug_plugin import KiCadDebugger

class DebugWindow(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="KiCad Debug Monitor", size=(600, 400))
        self.debugger = KiCadDebugger()
        
        # Create UI
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Status section
        status_box = wx.StaticBox(panel, label="Connection Status")
        status_sizer = wx.StaticBoxSizer(status_box, wx.VERTICAL)
        
        self.status_text = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.status_text.SetValue(f"Socket Path: {self.debugger.socket_path}")
        status_sizer.Add(self.status_text, 0, wx.ALL | wx.EXPAND, 5)
        
        # Connect button
        self.connect_btn = wx.Button(panel, label="Connect to KiCad")
        self.connect_btn.Bind(wx.EVT_BUTTON, self.on_connect)
        status_sizer.Add(self.connect_btn, 0, wx.ALL, 5)
        
        # Debug log
        log_box = wx.StaticBox(panel, label="Debug Log")
        log_sizer = wx.StaticBoxSizer(log_box, wx.VERTICAL)
        
        self.log = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        log_sizer.Add(self.log, 1, wx.ALL | wx.EXPAND, 5)
        
        # Add all sections
        vbox.Add(status_sizer, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(log_sizer, 1, wx.ALL | wx.EXPAND, 5)
        
        panel.SetSizer(vbox)
        
    def on_connect(self, event):
        """Handle connection button click"""
        if self.debugger.connect():
            self.log.AppendText("Successfully connected to KiCad API\n")
            self.start_monitoring()
        else:
            self.log.AppendText("Failed to connect to KiCad API\n")
            
    def start_monitoring(self):
        """Start monitoring KiCad events"""
        response = self.debugger.start_debug_session()
        if response:
            self.log.AppendText(f"Debug session started: {response}\n")
            # Start periodic updates
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.update_debug_info)
            self.timer.Start(1000)  # Update every second
            
    def update_debug_info(self, event):
        """Update debug information"""
        elements = self.debugger.get_pcb_elements()
        if elements:
            self.log.AppendText(f"PCB Elements: {elements}\n")