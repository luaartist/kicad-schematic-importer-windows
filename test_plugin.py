import pcbnew
import wx

class TestPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Test Plugin for KiCad 9"
        self.category = "Test"
        self.description = "Simple test plugin for KiCad 9"
        self.show_toolbar_button = True
    
    def Run(self):
        wx.MessageBox("Test plugin is working!", "Success")

# Register the plugin
TestPlugin().register()