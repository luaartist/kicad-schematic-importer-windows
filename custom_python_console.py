import wx
import wx.stc
import sys
import pcbnew
import os

class PythonConsoleFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="KiCad Python Console", size=(600, 400))
        
        # Show initialization popup
        wx.MessageBox(
            "Python Console Plugin initialized\n\n" + 
            f"Plugin location: {os.path.abspath(__file__)}\n" +
            "Python version: " + sys.version.split()[0],
            "Python Console Plugin",
            wx.OK | wx.ICON_INFORMATION
        )
        
        # Create main panel
        panel = wx.Panel(self)
        
        # Create vertical box sizer
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Create styled text control for output
        self.output = wx.stc.StyledTextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        
        # Set font with proper formatting
        font = wx.Font(
            pointSize=10,
            family=wx.FONTFAMILY_TELETYPE,
            style=wx.FONTSTYLE_NORMAL,
            weight=wx.FONTWEIGHT_NORMAL
        )
        self.output.StyleSetFont(wx.stc.STC_STYLE_DEFAULT, font)
        
        # Create input text control
        self.input = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        
        # Add controls to sizer
        vbox.Add(self.output, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.input, 0, wx.EXPAND | wx.ALL, 5)
        
        # Set panel sizer
        panel.SetSizer(vbox)
        
        # Bind events
        self.input.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
        
        # Redirect stdout to our console
        sys.stdout = self
        sys.stderr = self
        
        # Initialize Python environment
        self.locals = {
            'pcbnew': pcbnew,
            'board': pcbnew.GetBoard(),
            'wx': wx,
            'frame': self
        }
        
        # Print welcome message
        print("KiCad Python Console")
        print("Python " + sys.version.split()[0])
        print('Type "help()" for more information.')
        
    def write(self, text):
        """Redirect stdout/stderr to the text control"""
        self.output.AppendText(text)
        
    def flush(self):
        """Required for stdout/stderr redirection"""
        pass
        
    def on_enter(self, event):
        """Handle command execution when Enter is pressed"""
        command = self.input.GetValue()
        self.input.SetValue("")
        
        # Echo command
        self.write("\n>>> " + command + "\n")
        
        try:
            # Execute the command
            result = eval(command, globals(), self.locals)
            if result is not None:
                print(repr(result))
        except Exception as e:
            try:
                # If eval fails, try exec
                exec(command, globals(), self.locals)
            except Exception as e:
                print("Error:", str(e))

class PythonConsolePlugin(pcbnew.ActionPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Python Console"
        self.category = "Development"
        self.description = "Interactive Python Console for KiCad"
        self.show_toolbar_button = True
        self.icon_file_name = ""  # Add path to icon if you have one
        
    def Run(self):
        frame = PythonConsoleFrame(None)
        frame.Show()

# Register the plugin
PythonConsolePlugin().register()
