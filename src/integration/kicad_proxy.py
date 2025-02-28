"""
KiCad Proxy Module

This module provides a flexible proxy system for integrating with KiCad.
Instead of hardcoding paths to KiCad's installation directory, this module
dynamically locates KiCad and provides access to its functionality.

The proxy system allows for:
1. Dynamic discovery of KiCad installation
2. Flexible configuration of KiCad paths
3. Runtime loading of KiCad libraries and tools
4. Fallback mechanisms when KiCad is not available
"""

import os
import sys
import logging
import platform
import subprocess
import json
import ctypes
from pathlib import Path
from typing import Dict, List, Optional, Union, Callable, Any

class KicadProxy:
    """
    Proxy class for KiCad integration that dynamically discovers and loads KiCad components.
    
    This class avoids hardcoded dependencies on KiCad installation paths and provides
    a flexible way to interact with KiCad functionality.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the KiCad proxy.
        
        Args:
            config_path: Optional path to a configuration file with KiCad settings.
                         If not provided, the proxy will attempt to discover KiCad automatically.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # Add console handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
        
        # Initialize state
        self.kicad_paths = {}
        self.kicad_dlls = {}
        self.kicad_modules = {}
        self.kicad_tools = {}
        self.config = {}
        
        # Load configuration if provided
        if config_path and os.path.exists(config_path):
            self._load_config(config_path)
        
        # Discover KiCad installation
        self._discover_kicad()
        
        # Initialize proxy components
        self._init_components()
    
    def _load_config(self, config_path: str) -> None:
        """
        Load configuration from a JSON file.
        
        Args:
            config_path: Path to the configuration file.
        """
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
            self.logger.info(f"Loaded configuration from {config_path}")
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
    
    def _discover_kicad(self) -> None:
        """
        Discover KiCad installation paths.
        
        This method attempts to find KiCad installation directories and tools
        using various discovery methods.
        """
        # Check if paths are provided in config
        if 'kicad_paths' in self.config:
            self.kicad_paths = self.config['kicad_paths']
            self.logger.info("Using KiCad paths from configuration")
            return
        
        # Discover KiCad installation based on platform
        if platform.system() == "Windows":
            self._discover_kicad_windows()
        elif platform.system() == "Darwin":  # macOS
            self._discover_kicad_macos()
        else:  # Linux and others
            self._discover_kicad_linux()
    
    def _discover_kicad_windows(self) -> None:
        """Discover KiCad installation on Windows."""
        # Check common installation paths
        program_files = os.environ.get('ProgramFiles', 'C:\\Program Files')
        program_files_x86 = os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
        
        # Check for KiCad in Program Files
        kicad_versions = ['9.0', '8.0', '7.0', '6.0']
        for version in kicad_versions:
            # Check 64-bit installation
            path = os.path.join(program_files, 'KiCad', version)
            if os.path.exists(path):
                self.kicad_paths['base'] = path
                self.kicad_paths['bin'] = os.path.join(path, 'bin')
                self.kicad_paths['lib'] = os.path.join(path, 'share', 'kicad', 'library')
                self.kicad_paths['version'] = version
                self.logger.info(f"Found KiCad {version} at {path}")
                break
            
            # Check 32-bit installation
            path = os.path.join(program_files_x86, 'KiCad', version)
            if os.path.exists(path):
                self.kicad_paths['base'] = path
                self.kicad_paths['bin'] = os.path.join(path, 'bin')
                self.kicad_paths['lib'] = os.path.join(path, 'share', 'kicad', 'library')
                self.kicad_paths['version'] = version
                self.logger.info(f"Found KiCad {version} at {path}")
                break
        
        # Check for user data directory
        appdata = os.environ.get('APPDATA', '')
        documents = os.path.join(os.environ.get('USERPROFILE', ''), 'Documents')
        
        # Check for KiCad user data in Documents
        for version in kicad_versions:
            path = os.path.join(documents, 'KiCad', version)
            if os.path.exists(path):
                self.kicad_paths['user_data'] = path
                self.kicad_paths['user_lib'] = os.path.join(path, 'library')
                self.kicad_paths['user_3rdparty'] = os.path.join(path, '3rdparty')
                self.logger.info(f"Found KiCad {version} user data at {path}")
                break
        
        # If KiCad not found, log error
        if 'base' not in self.kicad_paths:
            self.logger.error("KiCad installation not found")
    
    def _discover_kicad_macos(self) -> None:
        """Discover KiCad installation on macOS."""
        # Check common installation paths
        paths = [
            '/Applications/KiCad/KiCad.app',
            '/Applications/KiCad.app'
        ]
        
        for path in paths:
            if os.path.exists(path):
                self.kicad_paths['base'] = path
                self.kicad_paths['bin'] = os.path.join(path, 'Contents', 'MacOS')
                self.kicad_paths['lib'] = os.path.join(path, 'Contents', 'SharedSupport', 'library')
                self.logger.info(f"Found KiCad at {path}")
                break
        
        # Check for user data directory
        home = os.path.expanduser('~')
        user_data = os.path.join(home, 'Library', 'Preferences', 'KiCad')
        if os.path.exists(user_data):
            self.kicad_paths['user_data'] = user_data
            self.logger.info(f"Found KiCad user data at {user_data}")
        
        # If KiCad not found, log error
        if 'base' not in self.kicad_paths:
            self.logger.error("KiCad installation not found")
    
    def _discover_kicad_linux(self) -> None:
        """Discover KiCad installation on Linux."""
        # Check if KiCad is in PATH
        try:
            result = subprocess.run(['which', 'kicad'], capture_output=True, text=True)
            if result.returncode == 0:
                kicad_bin = result.stdout.strip()
                kicad_base = os.path.dirname(os.path.dirname(kicad_bin))
                self.kicad_paths['base'] = kicad_base
                self.kicad_paths['bin'] = os.path.join(kicad_base, 'bin')
                self.kicad_paths['lib'] = os.path.join(kicad_base, 'share', 'kicad', 'library')
                self.logger.info(f"Found KiCad at {kicad_base}")
                return
        except Exception:
            pass
        
        # Check common installation paths
        paths = [
            '/usr/share/kicad',
            '/usr/local/share/kicad'
        ]
        
        for path in paths:
            if os.path.exists(path):
                self.kicad_paths['base'] = path
                self.kicad_paths['lib'] = os.path.join(path, 'library')
                
                # Find bin directory
                bin_paths = ['/usr/bin', '/usr/local/bin']
                for bin_path in bin_paths:
                    if os.path.exists(os.path.join(bin_path, 'kicad')):
                        self.kicad_paths['bin'] = bin_path
                        break
                
                self.logger.info(f"Found KiCad at {path}")
                break
        
        # Check for user data directory
        home = os.path.expanduser('~')
        user_data = os.path.join(home, '.config', 'kicad')
        if os.path.exists(user_data):
            self.kicad_paths['user_data'] = user_data
            self.logger.info(f"Found KiCad user data at {user_data}")
        
        # If KiCad not found, log error
        if 'base' not in self.kicad_paths:
            self.logger.error("KiCad installation not found")
    
    def _init_components(self) -> None:
        """Initialize KiCad components based on discovered paths."""
        if 'bin' in self.kicad_paths:
            self._find_tools()
            self._load_dlls()
            self._init_python_modules()
    
    def _find_tools(self) -> None:
        """Find KiCad command-line tools."""
        bin_path = self.kicad_paths.get('bin', '')
        if not bin_path or not os.path.exists(bin_path):
            self.logger.error("KiCad bin directory not found")
            return
        
        # Define tools to look for
        tools = {
            'kicad': 'kicad',
            'eeschema': 'eeschema',
            'pcbnew': 'pcbnew',
            'kicad-cli': 'kicad-cli',
            'bitmap2component': 'bitmap2component'
        }
        
        # Add .exe extension on Windows
        if platform.system() == "Windows":
            tools = {k: f"{v}.exe" for k, v in tools.items()}
        
        # Find tools
        for tool_name, executable in tools.items():
            tool_path = os.path.join(bin_path, executable)
            if os.path.exists(tool_path):
                self.kicad_tools[tool_name] = tool_path
                self.logger.info(f"Found KiCad tool: {tool_name} at {tool_path}")
            else:
                self.logger.warning(f"KiCad tool not found: {tool_name}")
    
    def _load_dlls(self) -> None:
        """Load KiCad DLLs for direct integration."""
        if platform.system() != "Windows":
            return
        
        bin_path = self.kicad_paths.get('bin', '')
        if not bin_path or not os.path.exists(bin_path):
            self.logger.error("KiCad bin directory not found")
            return
        
        try:
            # Add KiCad bin directory to PATH to find dependent DLLs
            os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]
            
            # Try to load common KiCad DLLs
            dll_names = [
                "kicommon.dll",
                "kigal.dll",
                "_pcbnew.dll",
                "_eeschema.dll"
            ]
            
            for dll_name in dll_names:
                dll_path = os.path.join(bin_path, dll_name)
                if os.path.exists(dll_path):
                    try:
                        self.kicad_dlls[dll_name] = ctypes.CDLL(dll_path)
                        self.logger.info(f"Loaded KiCad DLL: {dll_name}")
                    except Exception as e:
                        self.logger.error(f"Error loading KiCad DLL {dll_name}: {e}")
        
        except Exception as e:
            self.logger.error(f"Error loading KiCad DLLs: {e}")
    
    def _init_python_modules(self) -> None:
        """Initialize KiCad Python modules."""
        bin_path = self.kicad_paths.get('bin', '')
        if not bin_path or not os.path.exists(bin_path):
            self.logger.error("KiCad bin directory not found")
            return
        
        # Add KiCad Python modules to path
        python_path = None
        if platform.system() == "Windows":
            python_paths = [
                os.path.join(bin_path, 'scripting'),
                os.path.join(bin_path, 'scripting', 'plugins')
            ]
            for path in python_paths:
                if os.path.exists(path) and path not in sys.path:
                    sys.path.append(path)
                    python_path = path
        else:
            # For Linux/macOS, Python modules might be in different locations
            python_paths = [
                os.path.join(self.kicad_paths.get('base', ''), 'lib', 'python3', 'dist-packages'),
                os.path.join(self.kicad_paths.get('base', ''), 'share', 'kicad', 'scripting')
            ]
            for path in python_paths:
                if os.path.exists(path) and path not in sys.path:
                    sys.path.append(path)
                    python_path = path
        
        if python_path:
            self.logger.info(f"Added KiCad Python modules path: {python_path}")
            
            # Try to import KiCad Python modules
            try:
                # Import pcbnew module
                import pcbnew
                self.kicad_modules['pcbnew'] = pcbnew
                self.logger.info("Imported KiCad pcbnew module")
            except ImportError as e:
                self.logger.warning(f"Could not import KiCad pcbnew module: {e}")
            
            try:
                # Import eeschema module (if available)
                import eeschema
                self.kicad_modules['eeschema'] = eeschema
                self.logger.info("Imported KiCad eeschema module")
            except ImportError as e:
                self.logger.warning(f"Could not import KiCad eeschema module: {e}")
    
    def get_tool_path(self, tool_name: str) -> Optional[str]:
        """
        Get the path to a KiCad tool.
        
        Args:
            tool_name: Name of the tool (e.g., 'kicad', 'pcbnew', 'bitmap2component')
            
        Returns:
            Path to the tool executable, or None if not found.
        """
        return self.kicad_tools.get(tool_name)
    
    def run_tool(self, tool_name: str, args: List[str], timeout: Optional[int] = None) -> subprocess.CompletedProcess:
        """
        Run a KiCad tool with the specified arguments.
        
        Args:
            tool_name: Name of the tool to run
            args: List of command-line arguments
            timeout: Timeout in seconds (optional)
            
        Returns:
            CompletedProcess instance with return code, stdout, and stderr
            
        Raises:
            FileNotFoundError: If the tool is not found
            subprocess.TimeoutExpired: If the tool times out
            subprocess.SubprocessError: If the tool fails to run
        """
        tool_path = self.get_tool_path(tool_name)
        if not tool_path:
            raise FileNotFoundError(f"KiCad tool not found: {tool_name}")
        
        cmd = [tool_path] + args
        self.logger.info(f"Running KiCad tool: {' '.join(cmd)}")
        
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    
    def get_module(self, module_name: str) -> Any:
        """
        Get a KiCad Python module.
        
        Args:
            module_name: Name of the module (e.g., 'pcbnew', 'eeschema')
            
        Returns:
            The module object, or None if not found.
        """
        return self.kicad_modules.get(module_name)
    
    def get_dll(self, dll_name: str) -> Any:
        """
        Get a KiCad DLL.
        
        Args:
            dll_name: Name of the DLL (e.g., 'kicommon.dll')
            
        Returns:
            The DLL object, or None if not found.
        """
        return self.kicad_dlls.get(dll_name)
    
    def get_path(self, path_type: str) -> Optional[str]:
        """
        Get a KiCad path.
        
        Args:
            path_type: Type of path (e.g., 'base', 'bin', 'lib', 'user_data')
            
        Returns:
            The path, or None if not found.
        """
        return self.kicad_paths.get(path_type)
    
    def bitmap_to_component(self, input_path: str, output_format: str, output_path: str, 
                           options: Optional[List[str]] = None) -> bool:
        """
        Convert a bitmap image to a KiCad component using bitmap2component.
        
        Args:
            input_path: Path to the input bitmap image
            output_format: Output format (-l: Library, -m: Module, -p: Page layout, -s: Schematic)
            output_path: Path to the output file
            options: Additional options for bitmap2component
            
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(input_path):
            self.logger.error(f"Input file not found: {input_path}")
            return False
        
        try:
            args = [input_path, output_format, output_path]
            if options:
                args.extend(options)
            
            result = self.run_tool('bitmap2component', args, timeout=30)
            
            if result.returncode != 0:
                self.logger.error(f"bitmap2component error: {result.stderr}")
                return False
            
            if not os.path.exists(output_path):
                self.logger.error("bitmap2component did not create output file")
                return False
            
            return True
            
        except FileNotFoundError:
            self.logger.error("bitmap2component not found")
            return False
        except subprocess.TimeoutExpired:
            self.logger.error("bitmap2component command timed out")
            return False
        except Exception as e:
            self.logger.error(f"Error running bitmap2component: {e}")
            return False
    
    def save_config(self, config_path: str) -> bool:
        """
        Save the current configuration to a file.
        
        Args:
            config_path: Path to save the configuration file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create config dictionary
            config = {
                'kicad_paths': self.kicad_paths,
                'kicad_tools': {k: str(v) for k, v in self.kicad_tools.items()},
                'kicad_modules': list(self.kicad_modules.keys()),
                'kicad_dlls': list(self.kicad_dlls.keys())
            }
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(config_path)), exist_ok=True)
            
            # Save config
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.logger.info(f"Saved configuration to {config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            return False


# Singleton instance for global access
_kicad_proxy = None

def get_kicad_proxy(config_path: Optional[str] = None) -> KicadProxy:
    """
    Get the global KicadProxy instance.
    
    Args:
        config_path: Optional path to a configuration file
        
    Returns:
        KicadProxy instance
    """
    global _kicad_proxy
    if _kicad_proxy is None:
        _kicad_proxy = KicadProxy(config_path)
    return _kicad_proxy
