import cv2
import numpy as np
import uuid

class ComponentRecognizer:
    """Recognizes components in schematic diagrams"""
    
    def __init__(self):
        """Initialize the component recognizer"""
        self.min_component_size = 10  # Minimum size for a component in pixels
        self.max_component_size = 100  # Maximum size for a component in pixels
    
    def recognize_components(self, image):
        """
        Recognize components in an image
        
        Args:
            image: OpenCV image (numpy array)
            
        Returns:
            List of components, where each component is a dict with:
                - id: Unique component ID
                - type: Component type (e.g., 'resistor', 'capacitor', etc.)
                - x, y: Center coordinates
                - width, height: Component dimensions
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
            
        # Apply threshold to get binary image
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        components = []
        
        # Process each contour
        for i, contour in enumerate(contours):
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter by size
            if (w >= self.min_component_size and h >= self.min_component_size and 
                w <= self.max_component_size and h <= self.max_component_size):
                
                # Calculate center
                cx = x + w // 2
                cy = y + h // 2
                
                # Create component object
                component = {
                    'id': str(uuid.uuid4())[:8],  # Generate unique ID
                    'type': self._determine_component_type(contour, gray),
                    'x': cx,
                    'y': cy,
                    'width': w,
                    'height': h
                }
                
                components.append(component)
                
        return components
    
    def _determine_component_type(self, contour, image):
        """
        Determine component type based on contour analysis
        This is a simplified version - a real implementation would use more 
        advanced shape analysis or deep learning
        """
        # Get shape characteristics
        perimeter = cv2.arcLength(contour, True)
        area = cv2.contourArea(contour)
        if perimeter == 0:
            return "unknown"
        
        circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
        
        # Determine type based on shape
        if 0.7 <= circularity <= 1.0:
            return "circular"  # Could be a capacitor
        elif circularity < 0.6:
            # Get aspect ratio
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h if h > 0 else 0
            
            if 0.8 <= aspect_ratio <= 1.2:
                return "square"  # Could be an IC
            elif aspect_ratio > 1.2:
                return "horizontal"  # Could be a resistor
            else:
                return "vertical"  # Could be a diode
        else:
            return "unknown"
