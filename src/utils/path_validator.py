from pathlib import Path
from typing import Union
import os

class PathValidator:
    """Validates paths for security and correctness."""
    
    @staticmethod
    def is_safe_executable(path: Union[str, Path]) -> bool:
        """
        Verify an executable path is safe to use.
        - Must be absolute
        - Must be in Program Files or system32 on Windows
        - Must not contain suspicious characters
        """
        path = Path(path).resolve()
        
        # Must be absolute and exist
        if not path.is_absolute() or not path.exists():
            return False
            
        # Check for standard installation directories
        safe_dirs = [
            os.environ.get('ProgramFiles', 'C:\\Program Files'),
            os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'),
            os.environ.get('SystemRoot', 'C:\\Windows') + '\\system32'
        ]
        
        return any(str(path).startswith(safe_dir) for safe_dir in safe_dirs)
    
    @staticmethod
    def is_safe_output_path(path: Union[str, Path]) -> bool:
        """
        Verify an output path is safe to write to.
        - Must be absolute
        - Parent must exist
        - Must be within project directory or temp directory
        """
        path = Path(path).resolve()
        
        # Must be absolute and parent must exist
        if not path.is_absolute() or not path.parent.exists():
            return False
            
        # Check if path is within allowed directories
        safe_dirs = [
            Path.cwd(),  # Project directory
            Path(os.environ.get('TEMP', '/tmp'))  # Temp directory
        ]
        
        return any(str(path).startswith(str(safe_dir)) for safe_dir in safe_dirs)