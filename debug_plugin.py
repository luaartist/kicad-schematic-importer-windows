import os
import sys
import logging
import shutil
from datetime import datetime
import socket
import json
import tempfile

# Try to import KiCad modules
try:
    import pcbnew
    import wx
    import wx.aui
except ImportError:
    print("\nError: This script must be run from KiCad's Python console.")
    print("\nTo install the debug functionality:")
    print("1. Open KiCad PCB Editor")
    print("2. Go to View → Python Console")
    print("3. In the console, run:")
    print("   >>> import sys")
    print(f"   >>> sys.path.append(r'{os.path.dirname(os.path.abspath(__file__))}')")
    print("   >>> import debug_plugin")
    print("   >>> debug_plugin.register_debug_plugin()")
    sys.exit(1)

class KiCadDebugger:
    def __init__(self):
        self.socket_path = os.path.join(tempfile.gettempdir(), 'api.sock')
        self.socket = None
        
    def connect(self):
        """Connect to KiCad's IPC socket"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(('localhost', self.get_socket_port()))
            print(f"Connected to KiCad API at: {self.socket_path}")
            return True
        except Exception as e:
            print(f"Failed to connect to KiCad API: {str(e)}")
            return False
            
    def get_socket_port(self):
        """Get the port number from the socket file"""
        try:
            with open(self.socket_path, 'r') as f:
                return int(f.read().strip())
        except:
            return None
            
    def send_command(self, command, params=None):
        """Send command to KiCad"""
        if not self.socket:
            if not self.connect():
                return None
                
        try:
            msg = {
                'command': command,
                'parameters': params or {}
            }
            self.socket.send(json.dumps(msg).encode())
            response = self.socket.recv(4096).decode()
            return json.loads(response)
        except Exception as e:
            print(f"Error sending command: {str(e)}")
            return None

    def start_debug_session(self):
        """Initialize debug session"""
        return self.send_command('start_debug_session')
        
    def get_pcb_elements(self):
        """Get PCB elements for debugging"""
        return self.send_command('get_pcb_elements')
        
    def close(self):
        """Close the socket connection"""
        if self.socket:
            self.socket.close()

def find_kicad_plugin_dir():
    """Find the appropriate KiCad plugin directory"""
    possible_dirs = [
        # KiCad 9.0 3rdparty plugins (primary location)
        os.path.join(os.path.expanduser('~'), 'Documents', 'KiCad', '9.0', '3rdparty', 'plugins'),
        # KiCad 9.0 program files
        os.path.join("C:", "Program Files", "KiCad", "9.0", "share", "kicad", "plugins"),
        # KiCad 9.0 user plugins
        os.path.join(os.path.expanduser('~'), 'Documents', 'KiCad', '9.0', 'plugins'),
        # KiCad scripting plugins
        os.path.join(os.path.expanduser('~'), '.kicad', 'scripting', 'plugins'),
    ]
    
    for d in possible_dirs:
        if os.path.exists(d):
            return d
    
    # Default to 3rdparty plugins directory
    default_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'KiCad', '9.0', '3rdparty', 'plugins')
    os.makedirs(default_dir, exist_ok=True)
    return default_dir

# Global debug manager instance
DEBUG_MANAGER = None

def get_debug_manager():
    """Get the global debug manager instance"""
    global DEBUG_MANAGER
    if DEBUG_MANAGER is None:
        DEBUG_MANAGER = DebugManager()
    return DEBUG_MANAGER

class DebugWindow(wx.Frame):
    def __init__(self, parent=None, title="Schematic Importer Debug"):
        super().__init__(parent, title=title, size=(800, 600))
        
        # Create main panel
        panel = wx.Panel(self)
        
        # Create text control for log messages
        self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        
        # Create image panel for debug visualizations
        self.image_panel = wx.Panel(panel)
        self.image_panel.SetBackgroundColour(wx.BLACK)
        
        # Create status bar
        self.CreateStatusBar()
        
        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.image_panel, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)
        
        # Center window
        self.Center()
        
        # Initialize timestamp for performance tracking
        self.start_time = None
    
    def log_message(self, msg, level=logging.INFO):
        """Append a timestamped message to the debug window"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        level_str = logging.getLevelName(level)
        formatted_msg = f"[{timestamp}] [{level_str}] {msg}\n"
        
        # Calculate elapsed time if processing started
        if self.start_time:
            elapsed = datetime.now() - self.start_time
            self.SetStatusText(f"Processing time: {elapsed.total_seconds():.2f}s")
        
        wx.CallAfter(self.text_ctrl.AppendText, formatted_msg)
    
    def start_processing(self):
        """Mark the start of processing for timing"""
        self.start_time = datetime.now()
        self.log_message("Starting schematic import processing")
    
    def update_image(self, cv_image):
        """Update the debug visualization panel with a new image"""
        try:
            # Convert OpenCV image to wx.Bitmap
            height, width = cv_image.shape[:2]
            wx_image = wx.Bitmap.FromBuffer(width, height, cv_image)
            
            # Create static bitmap if needed
            if not hasattr(self, 'image_ctrl'):
                self.image_ctrl = wx.StaticBitmap(self.image_panel, wx.ID_ANY, wx_image)
            else:
                self.image_ctrl.SetBitmap(wx_image)
            
            # Refresh display
            self.image_panel.Layout()
            self.image_panel.Refresh()
            
        except Exception as e:
            self.log_message(f"Error updating debug image: {e}", logging.ERROR)

class DebugManager:
    """Singleton manager for the debug window"""
    _instance = None
    
    def __init__(self):
        self._debug_window = None
        
        # Set up logging
        self.logger = logging.getLogger("schematic_importer")
        self.logger.setLevel(logging.DEBUG)
        
        # Create handler for debug window
        self.wx_handler = WxDebugHandler()
        formatter = logging.Formatter("%(message)s")
        self.wx_handler.setFormatter(formatter)
        self.logger.addHandler(self.wx_handler)
        
        # Create file handler in the debug directory
        plugin_dir = find_kicad_plugin_dir()
        self.debug_dir = os.path.join(plugin_dir, 'debug')
        os.makedirs(self.debug_dir, exist_ok=True)
        
        log_file = os.path.join(self.debug_dir, 'schematic_importer_debug.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Set up images directory
        self.images_dir = os.path.join(self.debug_dir, 'images')
        os.makedirs(self.images_dir, exist_ok=True)
    
    @staticmethod
    def get():
        """Get the debug manager instance"""
        return get_debug_manager()
    
    def show_window(self):
        """Show or create the debug window"""
        app = wx.GetApp()
        if not app:
            app = wx.App(False)
        
        if self._debug_window is None:
            self._debug_window = DebugWindow()
        
        self._debug_window.Show()
        self._debug_window.Raise()
    
    def log_message(self, msg, level=logging.INFO):
        """Log a message to both the debug window and file"""
        self.logger.log(level, msg)
    
    def start_processing(self):
        """Start timing the processing"""
        if self._debug_window:
            self._debug_window.start_processing()
    
    def update_image(self, image):
        """Update the debug visualization"""
        if self._debug_window:
            wx.CallAfter(self._debug_window.update_image, image)

class WxDebugHandler(logging.Handler):
    """Custom logging handler that writes to the debug window"""
    def emit(self, record):
        msg = self.format(record)
        debug_window = DebugManager.get()._debug_window
        if debug_window:
            debug_window.log_message(msg, record.levelno)

class SchematicImporterDebugPlugin(pcbnew.ActionPlugin):
    """KiCad plugin class for the debug window"""
    def defaults(self):
        self.name = "Schematic Importer Debug"
        self.category = "Import Tools"
        self.description = "Debug window for schematic importing"
        self.show_toolbar_button = True
        
        # Set icon path
        plugin_dir = find_kicad_plugin_dir()
        self.icon_file_name = os.path.join(plugin_dir, 'debug_icon.png')
        self.dark_icon_file_name = self.icon_file_name
    
    def Run(self):
        """Show the debug window when plugin is activated"""
        try:
            debug = DebugManager.get()
            debug.show_window()
            debug.log_message("Debug window opened via KiCad menu")
            debug.log_message(f"Debug log file: {os.path.join(debug.debug_dir, 'schematic_importer_debug.log')}")
            debug.log_message(f"Debug images directory: {debug.images_dir}")
            
        except Exception as e:
            wx.MessageBox(f"Error opening debug window: {e}", "Debug Error", wx.OK | wx.ICON_ERROR)

def register_debug_plugin():
    """Register the debug plugin with KiCad"""
    try:
        # Find plugin directory
        plugin_dir = find_kicad_plugin_dir()
        print(f"\nFound KiCad plugin directory: {plugin_dir}")
        
        # Create plugin directory structure
        target_dir = os.path.join(plugin_dir, 'enhanced_importer_v2_debug')
        os.makedirs(target_dir, exist_ok=True)
        
        # Create __init__.py
        with open(os.path.join(target_dir, "__init__.py"), "w") as f:
            f.write("""# Debug plugin initialization
try:
    from .debug_plugin import SchematicImporterDebugPlugin
    SchematicImporterDebugPlugin().register()
    import wx
    wx.MessageBox("Debug Plugin Loaded Successfully\\n\\nAccess via:\\nTools → External Plugins → Schematic Importer Debug\\n\\nOr shortcut: Alt+S then D",
                  "Debug Plugin Ready",
                  wx.OK | wx.ICON_INFORMATION)
except Exception as e:
    import traceback
    traceback.print_exc()
""")
        
        # Copy this file to plugin directory
        plugin_path = os.path.join(target_dir, 'debug_plugin.py')
        shutil.copy2(__file__, plugin_path)
        print(f"Copied debug plugin to: {plugin_path}")
        
        # Create debug icon
        icon_path = os.path.join(target_dir, 'debug_icon.png')
        icon_size = 24
        icon = wx.Bitmap(icon_size, icon_size)
        dc = wx.MemoryDC(icon)
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()
        dc.SetPen(wx.Pen('black'))
        dc.SetBrush(wx.Brush('red'))
        dc.DrawCircle(icon_size//2, icon_size//2, icon_size//3)
        dc.SelectObject(wx.NullBitmap)
        icon.SaveFile(icon_path, wx.BITMAP_TYPE_PNG)
        
        print("\nDebug plugin registered successfully!")
        print("\nAccess the debug window in KiCad PCB Editor:")
        print("1. Tools → External Plugins → Schematic Importer Debug")
        print("2. Or use shortcut: Alt+S then D")
        
    except Exception as e:
        wx.MessageBox(f"Error registering debug plugin: {str(e)}\n\nCheck the Python console for details.",
                     "Debug Plugin Error",
                     wx.OK | wx.ICON_ERROR)
        raise

if __name__ == '__main__':
    register_debug_plugin()
