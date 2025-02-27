import cv2
import numpy as np
import os
import pcbnew
import importlib.util

# Try to import the ImageProcessor
from ..utils.image_processor import ImageProcessor

# Check if we can import the AlternativeImageProcessor
alt_processor_spec = importlib.util.find_spec("src.utils.alternative_image_processor")
has_alt_processor = alt_processor_spec is not None

if has_alt_processor:
    from ..utils.alternative_image_processor import AlternativeImageProcessor

class SchematicImporter:
    """Main class for importing schematics from images"""
    
    def __init__(self, config_path=None):
        self.config = self._load_config(config_path)
        
        # Try to use the regular ImageProcessor first
        try:
            self.image_processor = ImageProcessor()
            print("Using standard ImageProcessor")
        except Exception as e:
            # If it fails (e.g., potrace not available), use the alternative processor
            if has_alt_processor:
                self.image_processor = AlternativeImageProcessor()
                print("Using AlternativeImageProcessor as fallback")
            else:
                # If alternative processor is not available, re-raise the exception
                raise e
        
        self.supported_formats = {
            'vector': ['.svg', '.pdf', '.eps'],
            'raster': ['.png', '.jpg', '.jpeg', '.tiff'],
            'min_resolution': 300  # DPI
        }
    
    def _load_config(self, config_path):
        """Load configuration from file"""
        # Implementation here
        return {}
    
    def validate_image(self, image_path):
        """Validate image format and quality"""
        ext = os.path.splitext(image_path)[1].lower()
        
        # Check if format is supported
        if ext not in (self.supported_formats['vector'] + self.supported_formats['raster']):
            raise ValueError(f"Unsupported file format. Supported formats: {', '.join(self.supported_formats['vector'] + self.supported_formats['raster'])}")
        
        if ext in self.supported_formats['raster']:
            # Check resolution for raster images
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not load image")
            
            # Get image DPI if available
            dpi = self.image_processor.get_image_dpi(image_path)
            if dpi and dpi < self.supported_formats['min_resolution']:
                raise ValueError(f"Image resolution too low. Minimum required: {self.supported_formats['min_resolution']} DPI")
            
            return {
                'type': 'raster',
                'dpi': dpi,
                'dimensions': img.shape,
                'needs_conversion': True
            }
        else:
            return {
                'type': 'vector',
                'needs_conversion': False
            }
    
    def preprocess_image(self, image_path):
        """Preprocess image for better recognition"""
        image_info = self.validate_image(image_path)
        
        if image_info['needs_conversion']:
            # For raster images, attempt to vectorize
            try:
                vector_path = self.image_processor.vectorize_image(image_path)
                return vector_path
            except Exception as e:
                raise ValueError(f"Failed to vectorize image: {str(e)}")
        
        return image_path
    
    def import_from_image(self, image_path, board):
        """Import schematic from image"""
        # Implementation here
        pass
    
    def detect_components(self, image):
        """Detect components in image"""
        # Implementation here
        return []
    
    def detect_connections(self, image):
        """Detect connections in image"""
        # Implementation here
        return []
