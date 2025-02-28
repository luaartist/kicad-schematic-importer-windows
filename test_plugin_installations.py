import os
import sys
import subprocess
import shutil
from pathlib import Path

class PluginInstallTester:
    def __init__(self):
        self.kicad_python = r"C:\Program Files\KiCad\9.0\bin\pythonw.exe"
        self.system_python = sys.executable
        self.test_results = []
        
    def clean_plugin_directory(self, plugin_name):
        """Remove existing plugin installation"""
        plugin_paths = [
            Path.home() / ".local" / "share" / "kicad" / "9.0" / "scripting" / "plugins" / plugin_name,
            Path.home() / "AppData" / "Roaming" / "kicad" / "9.0" / "scripting" / "plugins" / plugin_name,
            Path(os.environ.get('APPDATA', '')) / "kicad" / "9.0" / "scripting" / "plugins" / plugin_name
        ]
        
        for path in plugin_paths:
            if path.exists():
                shutil.rmtree(path)
                print(f"Removed existing installation at: {path}")

    def run_install_script(self, install_script, python_interpreter, env_vars=None):
        """Run installation script with specified Python interpreter"""
        try:
            env = os.environ.copy()
            if env_vars:
                env.update(env_vars)
            
            cmd = [python_interpreter, install_script]
            result = subprocess.run(cmd, 
                                  env=env,
                                  capture_output=True, 
                                  text=True)
            
            success = result.returncode == 0
            return {
                'interpreter': python_interpreter,
                'success': success,
                'output': result.stdout,
                'error': result.stderr,
                'env_vars': env_vars
            }
        except Exception as e:
            return {
                'interpreter': python_interpreter,
                'success': False,
                'output': '',
                'error': str(e),
                'env_vars': env_vars
            }

    def test_installations(self, install_script, plugin_name):
        """Test plugin installation with different configurations"""
        print(f"\nTesting installations for {plugin_name}")
        print("-" * 50)

        # Test configurations
        configs = [
            {
                'name': "KiCad Python - Default",
                'interpreter': self.kicad_python,
                'env_vars': None
            },
            {
                'name': "KiCad Python - Modified Path",
                'interpreter': self.kicad_python,
                'env_vars': {
                    'PYTHONPATH': os.path.join(os.path.dirname(self.kicad_python), "Lib")
                }
            },
            {
                'name': "System Python",
                'interpreter': self.system_python,
                'env_vars': None
            }
        ]

        for config in configs:
            print(f"\nTrying: {config['name']}")
            print(f"Using interpreter: {config['interpreter']}")
            
            # Clean previous installation
            self.clean_plugin_directory(plugin_name)
            
            # Run installation
            result = self.run_install_script(
                install_script,
                config['interpreter'],
                config['env_vars']
            )
            
            # Store result
            result['config_name'] = config['name']
            self.test_results.append(result)
            
            # Print result
            print(f"Success: {'Yes' if result['success'] else 'No'}")
            if result['error']:
                print(f"Error: {result['error']}")

        # Print summary
        print("\nInstallation Test Summary")
        print("-" * 50)
        for result in self.test_results:
            print(f"\n{result['config_name']}:")
            print(f"Success: {'Yes' if result['success'] else 'No'}")
            if result['error']:
                print(f"Error: {result['error'][:200]}...")

if __name__ == "__main__":
    # List of installation scripts to test
    installations = [
        ("install_advanced_plugin.py", "advanced_importer"),
        ("install_enhanced_plugin.py", "enhanced_importer"),
        ("install_full_plugin.py", "schematic_importer_full"),
        ("simple_install.py", "schematic_importer_simple")
    ]
    
    tester = PluginInstallTester()
    
    for install_script, plugin_name in installations:
        if os.path.exists(install_script):
            tester.test_installations(install_script, plugin_name)
        else:
            print(f"\nSkipping {install_script} - file not found")