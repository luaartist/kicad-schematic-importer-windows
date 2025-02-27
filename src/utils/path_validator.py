import os
import ctypes
from pathlib import Path
from typing import Union
import tempfile

class PathValidator:
    @staticmethod
    def _expand_short_path(path_str: str) -> str:
        """Convert Windows short (8.3) paths to long paths."""
        if os.name != "nt":
            return path_str
        buf = ctypes.create_unicode_buffer(260)
        ctypes.windll.kernel32.GetLongPathNameW(str(path_str), buf, 260)
        return buf.value or path_str

    @staticmethod
    def is_safe_executable(path: Union[str, Path]) -> bool:
        path = Path(PathValidator._expand_short_path(str(path))).resolve()
        
        if not path.is_absolute() or not path.exists():
            return False
            
        safe_dirs = [
            os.environ.get('ProgramFiles', 'C:\\Program Files'),
            os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'),
            os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'system32')
        ]
        
        return any(str(path).startswith(safe_dir) for safe_dir in safe_dirs)
    
    @staticmethod
    def is_safe_output_path(path: Union[str, Path]) -> bool:
        path = Path(PathValidator._expand_short_path(str(path))).resolve()
        temp_dir = Path(tempfile.gettempdir()).resolve()
        
        if not path.is_absolute():
            return False
            
        # Allow paths in temp directory or project directory
        return (
            path.is_relative_to(temp_dir) or 
            path.is_relative_to(Path.cwd())
        )
