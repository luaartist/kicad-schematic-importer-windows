import cv2
import numpy as np
from PIL import Image
import os
import subprocess  # nosec B404 - subprocess usage is validated
import shutil
from pathlib import Path
from typing import Optional, Tuple, List, Callable
from .path_validator import PathValidator

try:
    import potrace
    HAS_POTRACE = True
except ImportError:
    HAS_POTRACE = False

class ConversionCommandGenerator:
    """Generates commands for image conversion tools."""
    
    def get_inkscape_command(self, input_path: str, output_path: str) -> List[str]:
        """Generate Inkscape command for image conversion."""
        return [
            'inkscape',
            '--export-filename', str(output_path),
            '--export-type=svg',
            str(input_path)
        ]
    
    def get_potrace_command(self, input_path: str, output_path: str) -> List[str]:
        """Generate Potrace command for image conversion."""
        return [
            'potrace',
            '--svg',
            '--output', str(output_path),
            str(input_path)
        ]

class ImageProcessor:
    """Image processor class that provides methods for vectorizing images."""
    
    ALLOWED_TOOLS = ['inkscape', 'potrace']
    
    def __init__(self):
        """Initialize the image processor."""
        self.path_validator = PathValidator()
        self.command_generator = ConversionCommandGenerator()
        self.conversion_callback = None
        
        # Initialize tool availability flags
        self.has_inkscape = False
        self.has_potrace = False
        
        # Validate tools
        self._check_available_tools()
    
    def _check_available_tools(self) -> None:
        """Check which tools are available in the system."""
        self.has_inkscape = self._check_tool_exists('inkscape')
        self.has_potrace = HAS_POTRACE and self._check_tool_exists('potrace')
        
        print(f"Available vectorization tools: " +
              f"Inkscape: {self.has_inkscape}, " +
              f"Potrace: {self.has_potrace}")

    def _check_tool_exists(self, tool_name: str) -> bool:
        """Safely check if a command-line tool exists on Windows."""
        if tool_name not in self.ALLOWED_TOOLS:
            return False
        
        # Check common Windows installation paths
        common_paths = [
            f"C:\\Program Files\\{tool_name}\\bin\\{tool_name}.exe",
            f"C:\\Program Files\\{tool_name}\\{tool_name}.exe",
            f"C:\\Program Files (x86)\\{tool_name}\\bin\\{tool_name}.exe",
            f"C:\\Program Files (x86)\\{tool_name}\\{tool_name}.exe"
        ]
        
        return shutil.which(tool_name) is not None or any(Path(p).exists() for p in common_paths)

    def check_tool_exists(self, tool_name: str) -> bool:
        """Check if a required external tool exists in the system PATH."""
        return self._check_tool_exists(tool_name)

    def get_image_dpi(self, image_path: str) -> Optional[float]:
        """Get image DPI if available."""
        try:
            with Image.open(image_path) as img:
                dpi = img.info.get('dpi')
                if dpi:
                    return float(dpi[0])
            return 96.0  # Default DPI
        except Exception:
            return None

    def _validate_input_path(self, input_path: str) -> Path:
        """Validate input path exists and is safe."""
        input_path = Path(input_path).resolve()
        if not input_path.exists():
            raise ValueError(f"Input file not found: {input_path}")
        return input_path

    def _validate_executable(self, tool_name: str, path: Optional[str]) -> str:
        """Validate executable path for Windows."""
        if not path:
            raise RuntimeError(f"{tool_name} not found")
        
        # Convert to Windows path
        path = str(Path(path).resolve())
        
        # Validate path is in Program Files or Windows directory
        if not any(path.lower().startswith(p.lower()) for p in [
            "C:\\Program Files",
            "C:\\Program Files (x86)",
            "C:\\Windows",
            "C:\\Windows\\System32"
        ]):
            raise ValueError(f"Unsafe executable path: {path}")
        
        return path

    def _run_subprocess(self, cmd: List[str], timeout: int = 30) -> None:
        """Run subprocess with timeout and validation."""
        if not all(isinstance(arg, str) for arg in cmd):
            raise ValueError("All command arguments must be strings")
        
        if not all(self.path_validator.is_safe_path(arg) for arg in cmd if os.path.exists(arg)):
            raise ValueError("Unsafe command arguments detected")
        
        try:
            # nosec B603 - command and arguments are validated above
            subprocess.run(
                cmd,
                check=True,
                timeout=timeout,
                shell=False,  # Explicitly disable shell
                text=True,
                capture_output=True
            )
        except subprocess.TimeoutExpired:
            raise TimeoutError("SVG conversion timed out")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command failed with exit code {e.returncode}: {e.stderr}")

    def convert_to_svg(self, input_path: str, output_path: str, timeout: int = 30) -> str:
        """Convert image to SVG using available tools."""
        input_path = self._validate_input_path(input_path)
        output_path = Path(output_path).resolve()
        
        if self.has_inkscape:
            inkscape_path = self._validate_executable('Inkscape', shutil.which('inkscape'))
            cmd = self.command_generator.get_inkscape_command(str(input_path), str(output_path))
            self._run_subprocess(cmd, timeout)
            
            if not output_path.exists():
                raise ValueError("Inkscape failed to create output file")
                
            return str(output_path)
            
        raise RuntimeError("No suitable conversion tool found")

    def _vectorize_with_inkscape(self, image_path: str) -> str:
        """Vectorize image using Inkscape."""
        inkscape_path = self._validate_executable('Inkscape', shutil.which('inkscape'))
        output_path = str(Path(image_path).with_suffix('.svg'))
        
        cmd = self.command_generator.get_inkscape_command(image_path, output_path)
        self._run_subprocess(cmd, timeout=30)
        
        if not Path(output_path).exists():
            raise ValueError("Inkscape failed to create output file")
        
        return output_path

    def _vectorize_with_potrace(self, image_path: str) -> str:
        """Vectorize image using Potrace."""
        if not HAS_POTRACE:
            raise RuntimeError("Potrace library not available")
            
        potrace_path = self._validate_executable('Potrace', shutil.which('potrace'))
        output_path = str(Path(image_path).with_suffix('.svg'))
        
        cmd = self.command_generator.get_potrace_command(image_path, output_path)
        self._run_subprocess(cmd, timeout=30)
        
        if not Path(output_path).exists():
            raise ValueError("Potrace failed to create output file")
        
        return output_path

    def _vectorize_builtin(self, image_path: str) -> str:
        """Vectorize image using built-in Potrace library."""
        if not HAS_POTRACE:
            raise RuntimeError("Potrace library not available")
            
        output_path = str(Path(image_path).with_suffix('.svg'))
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError("Failed to load image")
            
        # Convert to bitmap
        _, bitmap = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        bitmap = potrace.Bitmap(bitmap)
        
        # Trace and save
        path = bitmap.trace()
        with open(output_path, 'w') as f:
            f.write(path.to_svg())
            
        return output_path

    def vectorize_image(self, image_path: str) -> str:
        """Vectorize image using available tools."""
        errors = []
        
        # Try Inkscape first if available
        if self.has_inkscape:
            try:
                return self._vectorize_with_inkscape(image_path)
            except Exception as e:
                errors.append(f"Inkscape vectorization failed: {e}")
        
        # Try Potrace if available
        if self.has_potrace:
            try:
                return self._vectorize_with_potrace(image_path)
            except Exception as e:
                errors.append(f"Potrace vectorization failed: {e}")
            
            # Try built-in Potrace as last resort
            try:
                return self._vectorize_builtin(image_path)
            except Exception as e:
                errors.append(f"Built-in vectorization failed: {e}")
        
        raise ValueError(f"All vectorization methods failed: {', '.join(errors)}")
