import sys
import os
import platform
import subprocess
from pathlib import Path

class KiCadPythonConfig:
    def __init__(self):
        self.kicad_path = r"C:\Program Files\KiCad\9.0"
        self.kicad_python = os.path.join(self.kicad_path, "bin", "pythonw.exe")
        self.current_python = sys.executable
        
    def check_python_config(self):
        """Check Python configuration and compatibility"""
        results = {
            'kicad_python_path': self.kicad_python,
            'current_python_path': self.current_python,
            'kicad_python_version': None,
            'current_python_version': sys.version,
            'is_correct_python': False,
            'issues': []
        }
        
        # Check if KiCad Python exists
        if not os.path.exists(self.kicad_python):
            results['issues'].append("KiCad Python interpreter not found")
            return results
            
        # Get KiCad Python version
        try:
            version_cmd = [self.kicad_python, "-c", "import sys; print(sys.version)"]
            kicad_version = subprocess.check_output(version_cmd, text=True)
            results['kicad_python_version'] = kicad_version.strip()
        except subprocess.CalledProcessError as e:
            results['issues'].append(f"Failed to get KiCad Python version: {str(e)}")
            return results
            
        # Check if using correct Python
        results['is_correct_python'] = (self.current_python.lower() == self.kicad_python.lower())
        
        if not results['is_correct_python']:
            results['issues'].append(
                "Currently using external Python interpreter. "
                "Should be using KiCad's built-in Python."
            )
            
        return results
        
    def fix_python_path(self):
        """Try to fix Python path to use KiCad's Python"""
        if not os.path.exists(self.kicad_python):
            return False
            
        try:
            # Add KiCad Python path to environment
            kicad_bin = os.path.join(self.kicad_path, "bin")
            os.environ["PATH"] = kicad_bin + os.pathsep + os.environ["PATH"]
            
            # Add KiCad Python Lib path to PYTHONPATH
            python_lib = os.path.join(kicad_bin, "Lib")
            if "PYTHONPATH" in os.environ:
                os.environ["PYTHONPATH"] = python_lib + os.pathsep + os.environ["PYTHONPATH"]
            else:
                os.environ["PYTHONPATH"] = python_lib
                
            return True
        except Exception as e:
            print(f"Failed to fix Python path: {str(e)}")
            return False

def show_python_config_dialog():
    """Show dialog with Python configuration info"""
    import wx
    
    config = KiCadPythonConfig()
    results = config.check_python_config()
    
    msg = f"""Python Configuration:

KiCad Python: {results['kicad_python_path']}
Version: {results['kicad_python_version']}

Current Python: {results['current_python_path']}
Version: {results['current_python_version']}

Status: {"OK" if results['is_correct_python'] else "Incorrect Python interpreter"}

Issues:
{chr(10).join(results['issues']) if results['issues'] else "None"}
"""
    
    dialog = wx.MessageDialog(None, msg, "Python Configuration", 
                            wx.OK | wx.ICON_INFORMATION)
    dialog.ShowModal()
    dialog.Destroy()
    
    return results