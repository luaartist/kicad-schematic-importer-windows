import cv2
import numpy as np

class ComponentRecognizer:
    """Class for recognizing electronic components in images"""
    
    def __init__(self):
        self.component_types = {
            "resistor": [(20, 10), (40, 20)],  # Width/height ratios for resistors
            "capacitor": [(10, 20), (15, 30)],  # Width/height ratios for capacitors
            "diode": [(15, 25), (20, 35)],      # Width/height ratios for diodes
            "ic": [(40, 40), (60, 60)]          # Width/height ratios for ICs
        }
        self.next_id = 1
    
    def recognize_components(self, image):
        """Recognize components in an image"""
        if image is None:
            return []
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Threshold to get binary image
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        components = []
        for contour in contours:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Skip very small contours
            if w < 10 or h < 10:
                continue
            
            # Determine component type based on aspect ratio
            aspect_ratio = w / h
            component_type = self._determine_component_type(aspect_ratio)
            
            # Create component object
            component = {
                "id": f"C{self.next_id}",
                "type": component_type,
                "x": x + w//2,  # Center x
                "y": y + h//2,  # Center y
                "width": w,
                "height": h
            }
            components.append(component)
            self.next_id += 1
        
        return components
    
    def _determine_component_type(self, aspect_ratio):
        """Determine component type based on aspect ratio"""
        # Default to resistor if we can't determine type
        best_type = "resistor"
        best_diff = float('inf')
        
        for comp_type, ratios in self.component_types.items():
            for ratio in ratios:
                target_ratio = ratio[0] / ratio[1]
                diff = abs(aspect_ratio - target_ratio)
                if diff < best_diff:
                    best_diff = diff
                    best_type = comp_type
        
        return best_type
