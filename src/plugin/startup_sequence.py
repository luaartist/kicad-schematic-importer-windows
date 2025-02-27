class PluginStartup:
    def on_kicad_launch(self):
        # Version compatibility check
        kicad_version = self.detect_kicad_version()
        print(f"KiCad Version Detected: {kicad_version}")
        
        # Initialize plugin toolbar and menu
        self.create_toolbar_button("Import Schematic", icon="import_icon.png")
        self.create_menu_item("Tools/Import Schematic from Image")
        
        # Load configuration
        self.load_user_preferences()
        
        # Initialize FLUX.AI connection
        self.initialize_flux_sync()