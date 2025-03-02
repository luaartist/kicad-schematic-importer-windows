import cv2
import numpy as np
from pathlib import Path
from ..utils.debug_manager import debug_manager

class ImageProcessor:
    def __init__(self):
        self.debug = debug_manager
        self.processing_cache = {}
        
    @debug_manager.track_processing
    def vectorize_image(self, image_path: str) -> str:
        """Vectorize image using available tools with debugging"""
        cache_key = f"vectorize_{image_path}"
        
        # Check if we've processed this exact image before
        if cache_key in self.processing_cache:
            self.debug.logger.warning(f"Image {image_path} was previously processed. Checking for changes...")
            
            # Check if the image has been modified
            current_mtime = Path(image_path).stat().st_mtime
            cached_mtime = self.processing_cache[cache_key]['mtime']
            
            if current_mtime == cached_mtime:
                self.debug.logger.warning("Using cached result - this might indicate a processing loop")
                return self.processing_cache[cache_key]['result']
        
        # Process the image
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Failed to load image: {image_path}")
            
            # Record image properties
            self.debug.logger.debug(f"Image shape: {image.shape}")
            self.debug.logger.debug(f"Image dtype: {image.dtype}")
            
            # Process image
            result = self._process_image(image)
            
            # Cache the result
            self.processing_cache[cache_key] = {
                'mtime': Path(image_path).stat().st_mtime,
                'result': result
            }
            
            return result
            
        except Exception as e:
            self.debug.logger.error(f"Error processing image: {str(e)}")
            raise
    
    @debug_manager.track_processing
    def _process_image(self, image):
        """Internal image processing with debugging"""
        # Add your image processing steps here
        # Each step should be logged for debugging
        steps = [
            ('grayscale', lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)),
            ('blur', lambda img: cv2.GaussianBlur(img, (5, 5), 0)),
            ('threshold', lambda img: cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]),
            # Add more processing steps as needed
        ]
        
        current_image = image
        for step_name, step_func in steps:
            self.debug.logger.debug(f"Executing step: {step_name}")
            try:
                current_image = step_func(current_image)
                self.debug.logger.debug(f"Step {step_name} completed successfully")
            except Exception as e:
                self.debug.logger.error(f"Error in step {step_name}: {str(e)}")
                raise
        
        return current_image