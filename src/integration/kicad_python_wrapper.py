import os
import sys
import platform
from pathlib import Path
from typing import Optional, Dict, Any, Union

class KicadPythonWrapper:
    """Windows-specific wrapper for KiCad Python API"""
    
    def __init__(self):
        if platform.system() != "Windows":
            raise RuntimeError("This plugin only supports Windows")
            
        self.kicad_version = self._detect_kicad_version()
        self.is_kicad9 = float(self.kicad_version.split('.')[0]) >= 9.0
        self._setup_paths()
        self.board = None
        self.initialized = False
        
    def reinitialize(self) -> bool:
        """Reinitialize KiCad integration after loading project"""
        try:
            # Reset paths and reload modules
            self._setup_paths()
            modules = self.import_kicad_modules()
            
            # Reinitialize board if it was previously loaded
            if self.board and modules.get('pcbnew'):
                self.board = modules['pcbnew'].GetBoard()
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"Error reinitializing KiCad integration: {e}")
            self.initialized = False
            return False

    def sync_project(self, project_path: str) -> bool:
        """Synchronize with KiCad project at given path"""
        if not os.path.exists(project_path):
            print(f"Project path not found: {project_path}")
            return False
            
        try:
            # Store project path
            self.project_path = project_path
            
            # Reinitialize KiCad integration
            if not self.reinitialize():
                return False
                
            # Load board if .kicad_pcb file exists
            board_file = os.path.join(project_path, os.path.basename(project_path) + '.kicad_pcb')
            if os.path.exists(board_file):
                return self.initialize_board(board_file)
                
            return True
        except Exception as e:
            print(f"Error synchronizing project: {e}")
            return False

    def _detect_kicad_version(self) -> str:
        """Detect installed KiCad version"""
        try:
            import pcbnew
            return pcbnew.GetBuildVersion()
        except ImportError:
            return "7.0"  # Default to 7.0 if not detected
    
    def initialize_board(self, filepath: Optional[str] = None) -> bool:
        """Initialize board from file or editor"""
        try:
            import pcbnew
            if filepath:
                if not os.path.exists(filepath):
                    print(f"Board file not found: {filepath}")
                    return False
                self.board = pcbnew.LoadBoard(filepath)
            else:
                self.board = pcbnew.GetBoard()
            return True
        except Exception as e:
            print(f"Error initializing board: {e}")
            return False
    
    def get_board(self):
        """Get current board instance"""
        return self.board
    
    def _setup_paths(self):
        """Setup KiCad Python paths based on detected version"""
        kicad_install = self._find_kicad_install()
        if kicad_install:
            sys.path.append(os.path.join(kicad_install, 'lib', 'python'))
    
    def _find_kicad_install(self) -> Optional[str]:
        """Find KiCad installation directory on Windows"""
        possible_paths = [
            os.path.join(os.environ.get('ProgramFiles', ''), 'KiCad'),
            os.path.join(os.environ.get('ProgramFiles(x86)', ''), 'KiCad')
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
        
    def _normalize_path(self, path: str) -> str:
        """Normalize path according to platform."""
        if platform.system() == "Windows":
            return str(Path(path).resolve()).replace('/', '\\')
        return str(Path(path).resolve())

    def import_kicad_modules(self) -> Dict[str, Any]:
        """Import and return KiCad modules safely"""
        modules = {}
        try:
            import pcbnew
            modules['pcbnew'] = pcbnew
        except ImportError:
            print("Warning: Failed to import pcbnew")
        
        try:
            import wx
            modules['wx'] = wx
        except ImportError:
            print("Warning: Failed to import wx")
        
        return modules
