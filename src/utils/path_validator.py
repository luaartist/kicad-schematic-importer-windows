import os
import ctypes
from pathlib import Path
from typing import Union
import tempfile
from PIL import Image

class PathValidator:
    def __init__(self):
        # Existing initialization code
        pass
    
    def is_safe_path(self, path):
        """Check if a path is safe to use."""
        # Implement path safety checks
        return True
    
    def get_image_dpi(self, image_path):
        """Get the DPI of an image.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            float: The DPI of the image, defaults to 96.0 if not available
        """
        try:
            from PIL import Image
            with Image.open(image_path) as img:
                dpi = img.info.get('dpi')
                if dpi:
                    return float(dpi[0])
            return 96.0  # Default DPI
        except Exception:
            return None
    
    def validate_image_dpi(self, image_path, min_dpi=300):
        """Validate that an image has sufficient DPI.
        
        Args:
            image_path (str): Path to the image file
            min_dpi (float): Minimum required DPI (default: 300)
            
        Returns:
            float: The image DPI if valid
            
        Raises:
            ValueError: If the image DPI is below the minimum required
        """
        dpi = self.get_image_dpi(image_path)
        if dpi < min_dpi:
            raise ValueError(f"Image resolution too low: {dpi} DPI. Minimum required: {min_dpi} DPI")
        return dpi

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
