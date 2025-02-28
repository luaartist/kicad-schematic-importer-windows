import pcbnew
import wx

class MinimalPlugin(pcbnew.ActionPlugin):
    """A minimal plugin that shows a message box when clicked"""
    
    def defaults(self):
        self.name = "Minimal Plugin"
        self.category = "Test"
        self.description = "A minimal plugin that shows a message box when clicked"
        self.show_toolbar_button = True
        self.icon_file_name = ""
    
    def Run(self):
        wx.MessageBox("Hello from Minimal Plugin!", "Minimal Plugin", wx.OK | wx.ICON_INFORMATION)

# Register the plugin
MinimalPlugin().register()
