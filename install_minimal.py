import os
import shutil

def install_minimal_plugin():
    """Install the minimal plugin to KiCad 9.0 plugins directory"""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the KiCad 9.0 plugins directory
    kicad_plugins_dir = os.path.join(os.path.expanduser("~"), "Documents", "KiCad", "9.0", "3rdparty", "plugins")
    
    # Define the target directory
    target_dir = os.path.join(kicad_plugins_dir, "minimal_plugin")
    
    # Create the target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Copy the minimal plugin files
    shutil.copy2(os.path.join(current_dir, "minimal_plugin.py"), os.path.join(target_dir, "minimal_plugin.py"))
    shutil.copy2(os.path.join(current_dir, "minimal_init.py"), os.path.join(target_dir, "__init__.py"))
    
    print(f"Minimal plugin installed to: {target_dir}")
    print("\nTo use the plugin:")
    print("1. Start KiCad")
    print("2. Open PCB Editor")
    print("3. Look for 'Minimal Plugin' in the Tools menu or toolbar")
    print("\nIf KiCad is already running, please restart it to load the plugin.")

if __name__ == "__main__":
    install_minimal_plugin()
