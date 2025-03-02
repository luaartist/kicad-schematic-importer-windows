class ConfigurationGUI:
    def __init__(self):        self.config = AutoConfig()
        self.root = tk.Tk()        self.root.title("KiCad Plugin Settings")
            def show(self):
        frame = ttk.Frame(self.root, padding="10")        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
                # Get current mode
        current_mode = self.config.config.get("user_mode", "beginner")        
        if current_mode == "beginner":            self.show_beginner_settings(frame)
        elif current_mode == "advanced":            self.show_advanced_settings(frame)
        elif current_mode == "developer":            self.show_developer_settings(frame)
                # Common settings
        self.add_common_settings(frame)        
        # Mode switch button        ttk.Button(frame, text="Change Mode", 
                  command=self.change_mode).grid(row=99, column=0)    
    def show_beginner_settings(self, frame):        """Show simplified settings for beginners"""
        # Basic toggles with clear descriptions        ttk.Label(frame, text="Basic Settings").grid(row=0, column=0)
                ttk.Checkbutton(frame, text="Enable automatic assistance",
                       variable=tk.BooleanVar(value=True)).grid(row=1, column=0)        
        ttk.Checkbutton(frame, text="Show helpful tips",                       variable=tk.BooleanVar(value=True)).grid(row=2, column=0)
        def show_advanced_settings(self, frame):
        """Show full settings for advanced users"""        # Full feature set
        ttk.Label(frame, text="Advanced Settings").grid(row=0, column=0)        
        # Add advanced options...    
    def show_developer_settings(self, frame):        """Show developer settings and debug options"""
        ttk.Label(frame, text="Developer Settings").grid(row=0, column=0)        
        # Add debug options...    
    def change_mode(self):        """Show mode selection dialog"""
        dialog = StartupModeDialog(self.root)        if dialog.ShowModal() == wx.ID_OK:
            self.config.config["user_mode"] = dialog.selected_mode            self.config.config["remember_mode"] = dialog.remember
            self.config.save_config()            
            # Refresh settings display
            self.refresh_settings()






























class ConfigurationGUI:
    def __init__(self):
        self.config = AutoConfig()
        self.root = tk.Tk()
        self.root.title("KiCad Plugin Settings")
        
    def show(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Get current mode
        current_mode = self.config.config.get("user_mode", "beginner")
        
        if current_mode == "beginner":
            self.show_beginner_settings(frame)
        elif current_mode == "advanced":
            self.show_advanced_settings(frame)
        elif current_mode == "developer":
            self.show_developer_settings(frame)
        
        # Common settings
        self.add_common_settings(frame)
        
        # Mode switch button
        ttk.Button(frame, text="Change Mode", 
                  command=self.change_mode).grid(row=99, column=0)
    
    def show_beginner_settings(self, frame):
        """Show simplified settings for beginners"""
        # Basic toggles with clear descriptions
        ttk.Label(frame, text="Basic Settings").grid(row=0, column=0)
        
        ttk.Checkbutton(frame, text="Enable automatic assistance",
                       variable=tk.BooleanVar(value=True)).grid(row=1, column=0)
        
        ttk.Checkbutton(frame, text="Show helpful tips",
                       variable=tk.BooleanVar(value=True)).grid(row=2, column=0)
    
    def show_advanced_settings(self, frame):
        """Show full settings for advanced users"""
        # Full feature set
        ttk.Label(frame, text="Advanced Settings").grid(row=0, column=0)
        
        # Add advanced options...
    
    def show_developer_settings(self, frame):
        """Show developer settings and debug options"""
        ttk.Label(frame, text="Developer Settings").grid(row=0, column=0)
        
        # Add debug options...
    
    def change_mode(self):
        """Show mode selection dialog"""
        dialog = StartupModeDialog(self.root)
        if dialog.ShowModal() == wx.ID_OK:
            self.config.config["user_mode"] = dialog.selected_mode
            self.config.config["remember_mode"] = dialog.remember
            self.config.save_config()
            
            # Refresh settings display
            self.refresh_settings()
