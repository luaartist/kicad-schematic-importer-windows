from src.integration.plugin_env_manager import PluginEnvironmentManager

def main():
    # Initialize manager
    manager = PluginEnvironmentManager()
    
    # Create isolated environment for plugin using Python 3.12
    manager.create_plugin_env("schematic_importer", "3.12")
    
    # Run plugin script in isolated environment
    manager.run_plugin_script("schematic_importer", "main.py")

if __name__ == "__main__":
    main()