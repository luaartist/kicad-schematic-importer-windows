import cv2
import numpy as np
from PIL import Image
import potrace
import subprocess

class ImageProcessor:
    """Utility class for image processing and conversion"""
    
    def __init__(self):
        # Check for optional external tools
        self.has_inkscape = self._check_tool_available('inkscape')
        self.has_potrace = self._check_tool_available('potrace')
    
    def _check_tool_available(self, tool_name):
        """Check if external tool is available"""
        try:
            subprocess.run([tool_name, '--version'], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False
    
    def get_image_dpi(self, image_path):
        """Get image DPI if available"""
        try:
            with Image.open(image_path) as img:
                dpi = img.info.get('dpi')
                if dpi:
                    return dpi[0]  # Return horizontal DPI
        except Exception:
            pass
        return None
    
    def vectorize_image(self, image_path):
        """Convert raster image to vector format"""
        # First try Inkscape if available (best quality)
        if self.has_inkscape:
            return self._vectorize_with_inkscape(image_path)
        
        # Fallback to potrace
        if self.has_potrace:
            return self._vectorize_with_potrace(image_path)
        
        # Final fallback to built-in vectorization
        return self._vectorize_builtin(image_path)
    
    def _vectorize_with_inkscape(self, image_path):
        """Use Inkscape for vectorization"""
        output_path = image_path.rsplit('.', 1)[0] + '.svg'
        try:
            subprocess.run([
                'inkscape',
                '--export-filename=' + output_path,
                '--export-type=svg',
                '--export-plain-svg',
                image_path
            ], check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Inkscape vectorization failed: {str(e)}")
    
    def _vectorize_with_potrace(self, image_path):
        """Use potrace for vectorization"""
        output_path = image_path.rsplit('.', 1)[0] + '.svg'
        try:
            # Convert to bitmap first
            subprocess.run([
                'potrace',
                '--svg',
                '--output=' + output_path,
                image_path
            ], check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Potrace vectorization failed: {str(e)}")
    
    def _vectorize_builtin(self, image_path):
        """Built-in vectorization using OpenCV and potrace library"""
        # Load and preprocess image
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        
        # Convert to bitmap for potrace
        bmp = potrace.Bitmap(binary)
        
        # Trace
        path = bmp.trace()
        
        # Save as SVG
        output_path = image_path.rsplit('.', 1)[0] + '.svg'
        with open(output_path, 'w') as f:
            f.write(self._generate_svg(path))
        
        return output_path
    
    def _generate_svg(self, path):
        """Generate SVG from potrace path"""
        # Basic SVG generation
        parts = []
        for curve in path:
            parts.append('M')
            for segment in curve:
                parts.append(f"{segment.start_point[0]},{segment.start_point[1]}")
                if segment.is_corner:
                    parts.append('L')
                else:
                    parts.append('C')
                    parts.append(f"{segment.c1[0]},{segment.c1[1]}")
                    parts.append(f"{segment.c2[0]},{segment.c2[1]}")
                parts.append(f"{segment.end_point[0]},{segment.end_point[1]}")
        
        path_data = ' '.join(parts)
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
    <path d="{path_data}" fill="none" stroke="black"/>
</svg>'''