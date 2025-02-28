import os
from pathlib import Path
from typing import Optional
from .python_version_manager import KiCadPythonManager

class PluginEnvironmentManager:
    def __init__(self):
        self.python_manager = KiCadPythonManager()
        self.plugin_root = self._get_plugin_root()
        
    def _get_plugin_root(self) -> Path:
        """Get KiCad plugin directory based on version"""
        if os.name == 'nt':  # Windows
            kicad_version = "9.0"  # Could be detected dynamically
            return Path.home() / "Documents" / "KiCad" / kicad_version / "3rdparty" / "plugins"
        return None

    def create_plugin_env(self, plugin_name: str, python_version: str) -> bool:
        """Create isolated environment for plugin development"""
        env_name = f"plugin_{plugin_name}"
        if self.python_manager.create_virtual_env(env_name, python_version):
            # Create symlink to plugin directory
            plugin_path = self.plugin_root / plugin_name
            env_path = self.python_manager.virtual_envs[env_name]
            
            try:
                if not plugin_path.exists():
                    plugin_path.symlink_to(env_path / "lib" / "site-packages" / plugin_name)
                return True
            except Exception as e:
                print(f"Failed to create plugin symlink: {e}")
        return False

    def run_plugin_script(self, plugin_name: str, script_name: str) -> bool:
        """Run plugin script in appropriate environment"""
        env_name = f"plugin_{plugin_name}"
        script_path = self.plugin_root / plugin_name / script_name
        
        return self.python_manager.run_script_in_env(str(script_path), env_name)