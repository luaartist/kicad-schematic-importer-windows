import cv2
import numpy as np
from PIL import Image
import os
import subprocess  # nosec B404 - subprocess usage is validated
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Tuple, List, Callable
from .command_generator import ConversionCommandGenerator
from .path_validator import PathValidator

try:
    import potrace
    HAS_POTRACE = True
except ImportError:
    HAS_POTRACE = False

class ImageProcessor:
    """Image processor class that provides methods for vectorizing images."""
    
    ALLOWED_TOOLS = ['inkscape', 'potrace']
    
    def __init__(self):
        """Initialize the image processor."""
        self.path_validator = PathValidator()
        self._validate_tools()
        self.command_generator = ConversionCommandGenerator()
        self.conversion_callback: Optional[Callable] = None
    
    def set_conversion_callback(self, callback: Callable):
        """Set callback for handling external conversions"""
        self.conversion_callback = callback
    
    def get_conversion_commands(self, input_path: str, output_path: str) -> dict:
        """Get available conversion commands without executing them"""
        if not self.path_validator.is_safe_input_path(input_path):
            raise ValueError(f"Unsafe input path: {input_path}")
        if not self.path_validator.is_safe_output_path(output_path):
            raise ValueError(f"Unsafe output path: {output_path}")
            
        return self.command_generator.get_available_commands(input_path, output_path)
    
    def convert_to_svg(self, input_path: str, output_path: str) -> str:
        """Convert image to SVG using user-provided callback or manual instructions"""
        commands = self.get_conversion_commands(input_path, output_path)
        
        if not commands:
            raise RuntimeError("No conversion tools available")
        
        if self.conversion_callback:
            # Use callback if provided
            return self.conversion_callback(commands, input_path, output_path)
        else:
            # Provide instructions for manual conversion
            instructions = self._generate_conversion_instructions(commands)
            return instructions
    
    def _generate_conversion_instructions(self, commands: dict) -> str:
        """Generate human-readable conversion instructions"""
        instructions = ["To convert the image, you can use any of these commands:"]
        
        for tool, cmd in commands.items():
            instructions.append(f"\n{tool.title()}:")
            instructions.append(" ".join(cmd))
        
        instructions.append("\nAfter converting, provide the SVG file path to continue processing.")
        return "\n".join(instructions)
    
    def validate_converted_file(self, svg_path: str) -> bool:
        """Validate that a manually converted SVG file exists and is valid"""
        if not self.path_validator.is_safe_input_path(svg_path):
            raise ValueError(f"Unsafe SVG path: {svg_path}")
            
        svg_path = Path(svg_path)
        if not svg_path.exists():
            raise FileNotFoundError(f"SVG file not found: {svg_path}")
        if svg_path.suffix.lower() != '.svg':
            raise ValueError(f"File must be SVG format: {svg_path}")
            
        return True

    def _validate_input_path(self, path: str) -> Path:
        """Validate that an input path exists."""
        resolved_path = Path(path).resolve()
        if not resolved_path.exists():
            raise ValueError(f"Input file not found: {resolved_path}")
        return resolved_path

    def _validate_output_directory(self, path: str) -> Path:
        """Validate that the output directory exists."""
        resolved_path = Path(path).resolve()
        if not resolved_path.parent.exists():
            raise ValueError(f"Output directory does not exist: {resolved_path.parent}")
        return resolved_path

    def _validate_executable(self, name: str, path: str) -> str:
        """Validate that an executable is safe to use."""
        if not path:
            raise RuntimeError(f"{name} not found")
        if not self.path_validator.is_safe_executable(path):
            raise ValueError(f"Unsafe {name} path: {path}")
        return path

    def _run_subprocess(self, cmd: list, timeout: int = None) -> None:
        """Run a subprocess with validated arguments."""
        try:
            # nosec B603 - command and arguments are validated before calling
            subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                timeout=timeout
            )
        except subprocess.SubprocessError as e:
            raise RuntimeError(f"Command failed: {' '.join(cmd)}") from e

    def convert_to_svg(self, input_path: str, output_path: str, timeout: int = 30) -> str:
        """Convert image to SVG safely."""
        input_path = Path(input_path).resolve()
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Validate output path is safe
        if not self.path_validator.is_safe_output_path(output_path):
            raise ValueError(f"Unsafe output path: {output_path}")
        output_path = Path(output_path).resolve()
        
        # Validate Inkscape installation
        inkscape_path = self._validate_executable('Inkscape', shutil.which('inkscape'))
        
        cmd = [
            inkscape_path,
            '--export-filename', str(output_path),
            str(input_path)
        ]
        
        # nosec B603 - all arguments are validated above
        self._run_subprocess(cmd, timeout)
        
        if not output_path.exists():
            raise ValueError("Inkscape failed to create output file")
        
        return str(output_path)

    def get_image_dpi(self, image_path: str) -> Optional[float]:
        """Get image DPI if available.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Horizontal DPI value if available, None otherwise
        """
        try:
            with Image.open(image_path) as img:
                dpi = img.info.get('dpi')
                return float(dpi[0]) if dpi else None
        except Exception:
            return None
    
    def vectorize_image(self, image_path: str) -> str:
        """Convert raster image to vector format using best available method.
        
        Args:
            image_path: Path to source image
            
        Returns:
            Path to generated SVG file
            
        Raises:
            ValueError: If vectorization fails with all methods
        """
        errors = []
        
        # Try methods in order of preference
        if self.has_inkscape:
            try:
                return self._vectorize_with_inkscape(image_path)
            except Exception as e:
                errors.append(f"Inkscape failed: {str(e)}")
        
        if self.has_potrace:
            try:
                return self._vectorize_with_potrace(image_path)
            except Exception as e:
                errors.append(f"Potrace failed: {str(e)}")
        
        try:
            return self._vectorize_builtin(image_path)
        except Exception as e:
            errors.append(f"Built-in vectorization failed: {str(e)}")
            
        raise ValueError(f"All vectorization methods failed:\n" + "\n".join(errors))
    
    def _vectorize_with_inkscape(self, image_path: str) -> str:
        """Use Inkscape for vectorization."""
        output_path = str(Path(image_path).with_suffix('.svg'))
        inkscape_path = shutil.which('inkscape')
        
        result = subprocess.run([
            inkscape_path,
            '--export-filename=' + output_path,
            '--export-type=svg',
            '--export-plain-svg',
            image_path
        ], check=True, capture_output=True, text=True)
        
        if not Path(output_path).exists():
            raise ValueError(f"Inkscape failed to create output file: {result.stderr}")
        return output_path
    
    def _vectorize_with_potrace(self, image_path: str) -> str:
        """Safely vectorize using potrace."""
        input_path = self._validate_input_path(image_path)
        output_path = self._validate_output_directory(input_path.with_suffix('.svg'))
        
        potrace_path = shutil.which('potrace')
        if not potrace_path:
            raise RuntimeError("Potrace not found")
        
        cmd = [
            potrace_path,
            '--svg',
            '--output', str(output_path),
            str(input_path)
        ]
        
        self._run_subprocess(cmd)
        
        if not output_path.exists():
            raise ValueError("Potrace failed to create output file")
        return str(output_path)
    
    def _vectorize_builtin(self, image_path: str) -> str:
        """Built-in vectorization using OpenCV and potrace library."""
        if not HAS_POTRACE:
            raise ValueError("Python-potrace library is not available. Please install it with 'pip install python-potrace'")
            
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Failed to load image: {image_path}")
            
        # Enhance image quality
        img = cv2.GaussianBlur(img, (3, 3), 0)
        _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Convert to bitmap for potrace
        bmp = potrace.Bitmap(binary)
        path = bmp.trace()
        
        output_path = str(Path(image_path).with_suffix('.svg'))
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_svg(path))
        
        return output_path
    
    def _generate_svg(self, path) -> str:
        """Generate SVG from potrace path."""
        parts: List[str] = []
        
        for curve in path:
            parts.append('M')
            for segment in curve:
                parts.extend([
                    f"{segment.start_point[0]},{segment.start_point[1]}",
                    'L' if segment.is_corner else 'C'
                ])
                
                if not segment.is_corner:
                    parts.extend([
                        f"{segment.c1[0]},{segment.c1[1]}",
                        f"{segment.c2[0]},{segment.c2[1]}"
                    ])
                    
                parts.append(f"{segment.end_point[0]},{segment.end_point[1]}")
        
        path_data = ' '.join(parts)
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
    <path d="{path_data}" fill="none" stroke="black"/>
</svg>'''

    def check_tool_exists(self, tool_name: str) -> bool:
        """Check if a tool exists in the system PATH.
        
        Args:
            tool_name: Name of the tool to check
        
        Returns:
            bool: True if tool exists, False otherwise
        """
        return bool(shutil.which(tool_name))
