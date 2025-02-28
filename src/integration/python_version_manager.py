import os
import sys
import platform
from pathlib import Path
from typing import Dict, Optional

class KiCadPythonManager:
    def __init__(self):
        self.kicad_python_path = self._get_kicad_python_path()
        self.system_python_paths = self._find_python_installations()
        self.virtual_envs = {}
        
    def _get_kicad_python_path(self) -> Path:
        """Get KiCad's built-in Python path"""
        if platform.system() == "Windows":
            base = Path(r"C:\Program Files\KiCad")
            # Check for both 9.0 and newer versions
            versions = sorted([d for d in base.glob("*") if d.is_dir()], reverse=True)
            if versions:
                return versions[0] / "bin" / "pythonw.exe"
        return None

    def _find_python_installations(self) -> Dict[str, Path]:
        """Find all Python installations on the system"""
        python_paths = {}
        if platform.system() == "Windows":
            search_paths = [
                r"C:\Program Files\Python*",
                r"C:\Python*",
                str(Path.home() / "AppData" / "Local" / "Programs" / "Python")
            ]
            
            for search_path in search_paths:
                for path in Path().glob(search_path):
                    if path.is_dir():
                        python_exe = path / "python.exe"
                        if python_exe.exists():
                            version = self._get_python_version(python_exe)
                            python_paths[version] = python_exe
        
        return python_paths

    def create_virtual_env(self, name: str, python_version: str) -> bool:
        """Create a new virtual environment for a specific Python version"""
        if python_version not in self.system_python_paths:
            return False
            
        venv_path = Path("venvs") / name
        python_path = self.system_python_paths[python_version]
        
        try:
            import venv
            venv.create(venv_path, with_pip=True)
            self.virtual_envs[name] = venv_path
            return True
        except Exception as e:
            print(f"Failed to create virtual environment: {e}")
            return False

    def run_script_in_env(self, script_path: str, env_name: Optional[str] = None) -> bool:
        """Run a script in specified environment or KiCad's Python"""
        try:
            if env_name and env_name in self.virtual_envs:
                python_exe = self.virtual_envs[env_name] / "Scripts" / "python.exe"
            else:
                python_exe = self.kicad_python_path
                
            import subprocess
            result = subprocess.run([str(python_exe), script_path], capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"Failed to run script: {e}")
            return False