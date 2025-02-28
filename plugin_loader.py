import os
import sys
import subprocess

def ensure_kicad_python():
    """Ensure we're using KiCad's Python interpreter"""
    kicad_python = r"C:\Program Files\KiCad\9.0\bin\pythonw.exe"
    
    if sys.executable.lower() != kicad_python.lower():
        # Restart script using KiCad's Python
        args = [kicad_python] + sys.argv
        os.execv(kicad_python, args)
        
def initialize_plugin():
    """Initialize the plugin with correct Python configuration"""
    ensure_kicad_python()
    
    # Show Python configuration on startup
    config_results = show_python_config_dialog()
    
    if not config_results['is_correct_python']:
        config = KiCadPythonConfig()
        if config.fix_python_path():
            print("Fixed Python path to use KiCad's Python interpreter")
        else:
            print("Failed to fix Python path")
            
    return config_results['is_correct_python']