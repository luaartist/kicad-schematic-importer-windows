import wx
from .startup_dialog import StartupModeDialog
from ..integration.auto_config import AutoConfig

class PluginStartup:
    def on_kicad_launch(self):
        config = AutoConfig()
        
        # Check if mode is already set and remembered
        if not config.config.get("user_mode") or not config.config.get("remember_mode"):
            self.show_mode_selection()
        
        # Initialize based on selected mode
        self.initialize_mode(config.config["user_mode"])
        
        # Continue with regular startup
        self.initialize_common_features()
    
    def show_mode_selection(self):
        dialog = StartupModeDialog(None)
        if dialog.ShowModal() == wx.ID_OK:
            config = AutoConfig()
            config.config["user_mode"] = dialog.selected_mode
            config.config["remember_mode"] = dialog.remember
            config.save_config()
        dialog.Destroy()
    
    def initialize_mode(self, mode):
        if mode == "beginner":
            self.initialize_beginner_mode()
        elif mode == "advanced":
            self.initialize_advanced_mode()
        elif mode == "developer":
            self.initialize_developer_mode()
    
    def initialize_beginner_mode(self):
        """Initialize simplified interface for beginners"""
        # Create simplified toolbar
        self.create_toolbar_button("Import Schematic", icon="import_icon.png")
        self.create_toolbar_button("Help", icon="help_icon.png")
        
        # Enable guided assistance
        self.enable_tooltips()
        self.enable_quick_help()
        
        # Disable advanced features
        self.hide_advanced_features()
    
    def initialize_advanced_mode(self):
        """Initialize full feature set for advanced users"""
        # Create full toolbar
        self.create_full_toolbar()
        
        # Enable advanced features
        self.enable_advanced_features()
        
        # Configure normal logging
        self.setup_normal_logging()
    
    def initialize_developer_mode(self):
        """Initialize development environment"""
        # Enable all features
        self.enable_all_features()
        
        # Setup debug tools
        self.setup_debug_environment()
        
        # Show developer toolbar
        self.create_developer_toolbar()
    
    def initialize_common_features(self):
        """Initialize features common to all modes"""
        # Version compatibility check
        kicad_version = self.detect_kicad_version()
        print(f"KiCad Version Detected: {kicad_version}")
        
        # Load configuration
        self.load_user_preferences()
        
        # Initialize FLUX.AI connection
        self.initialize_flux_sync()
    
    def enable_tooltips(self):
        """Enable enhanced tooltips for beginners"""
        wx.ToolTip.Enable(True)
        wx.ToolTip.SetDelay(500)
    
    def enable_quick_help(self):
        """Enable quick help system for beginners"""
        self.quick_help = {
            "import": "Click here to import a schematic from an image",
            "settings": "Basic settings for the plugin",
            "help": "Get help and tutorials"
        }
    
    def hide_advanced_features(self):
        """Hide advanced features in beginner mode"""
        advanced_features = [
            "debug_panel",
            "advanced_settings",
            "developer_tools"
        ]
        for feature in advanced_features:
            self.hide_feature(feature)
    
    def create_developer_toolbar(self):
        """Create developer toolbar with debug tools"""
        self.create_toolbar_button("Debug Console", icon="debug_icon.png")
        self.create_toolbar_button("Performance Monitor", icon="performance_icon.png")
        self.create_toolbar_button("Test Tools", icon="test_icon.png")
