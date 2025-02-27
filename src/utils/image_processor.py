import cv2
import numpy as np
from PIL import Image
import potrace
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Tuple, List

class ImageProcessor:
    """Utility class for image processing and conversion"""
    
    def __init__(self):
        self.ALLOWED_TOOLS = frozenset({'inkscape', 'potrace'})  # Use frozenset for immutable set
        self.has_inkscape = self.check_tool_exists('inkscape')
        self.has_potrace = self.check_tool_exists('potrace')
    
    def check_tool_exists(self, tool_name: str) -> bool:
        """Check if external tool is available in system PATH."""
        if tool_name not in self.ALLOWED_TOOLS:
            return False
        return shutil.which(tool_name) is not None

    def convert_to_svg(self, image_path: str, output_path: str) -> str:
        """Convert image to SVG format using Inkscape.
        
        Args:
            image_path: Path to source image
            output_path: Desired output SVG path
            
        Returns:
            Path to generated SVG file
            
        Raises:
            ValueError: If paths are invalid
            TimeoutError: If conversion times out
            subprocess.CalledProcessError: If conversion fails
        """
        image_path = Path(image_path).resolve()
        output_path = Path(output_path).resolve()
        
        if not image_path.exists():
            raise ValueError(f"Input image not found: {image_path}")
        if not output_path.parent.exists():
            raise ValueError(f"Output directory does not exist: {output_path.parent}")
            
        inkscape_path = shutil.which('inkscape')
        if not inkscape_path:
            raise RuntimeError("Inkscape not found in PATH")
            
        try:
            result = subprocess.run([
                inkscape_path,
                f'--export-filename={output_path}',
                '--export-type=svg',
                '--export-plain-svg',
                str(image_path)
            ], check=True, capture_output=True, text=True, timeout=30)
            return str(output_path)
        except subprocess.TimeoutExpired:
            raise TimeoutError("SVG conversion timed out after 30 seconds")
    
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
        """Use potrace for vectorization."""
        output_path = str(Path(image_path).with_suffix('.svg'))
        potrace_path = shutil.which('potrace')
        
        result = subprocess.run([
            potrace_path,
            '--svg',
            '--output=' + output_path,
            image_path
        ], check=True, capture_output=True, text=True)
        
        if not Path(output_path).exists():
            raise ValueError(f"Potrace failed to create output file: {result.stderr}")
        return output_path
    
    def _vectorize_builtin(self, image_path: str) -> str:
        """Built-in vectorization using OpenCV and potrace library."""
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
