import cv2
import numpy as np
import os
import json
import pcbnew
from pathlib import Path

class SchematicImporter:
    """Main class for importing schematics from images"""
    
    def __init__(self, config_path=None):
        self.config = self._load_config(config_path)
        self.components = []
        self.connections = []
    
    def _load_config(self, config_path=None):
        """Load configuration from file"""
        if config_path is None:
            # Use default config path
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            config_path = os.path.join(base_dir, 'config.json')
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        
        # Return default config if loading fails
        return {
            "api_key": "",
            "api_url": "",
            "use_online_detection": True,
            "fallback_to_local": True,
            "save_debug_images": True,
            "debug_dir": "debug",
            "component_templates": {
                "resistor": {"pins": 2, "footprint": "Resistor_SMD:R_0805_2012Metric"},
                "capacitor": {"pins": 2, "footprint": "Capacitor_SMD:C_0805_2012Metric"},
                "ic": {"pins": 8, "footprint": "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"},
                "connector": {"pins": 4, "footprint": "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical"},
                "diode": {"pins": 2, "footprint": "Diode_SMD:D_SOD-123"},
                "transistor": {"pins": 3, "footprint": "Package_TO_SOT_SMD:SOT-23"}
            }
        }
    
    def import_from_image(self, image_path, board, options=None):
        """Import schematic from image"""
        if options is None:
            options = {}
        
        # Merge options with config
        use_online = options.get('use_online', self.config.get('use_online_detection', True))
        fallback_local = options.get('fallback_local', self.config.get('fallback_to_local', True))
        save_debug = options.get('save_debug', self.config.get('save_debug_images', True))
        
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Preprocess image
        preprocessed = self._preprocess_image(image)
        
        # Detect components
        if use_online:
            try:
                self.components = self._detect_components_online(preprocessed)
            except Exception as e:
                print(f"Online detection failed: {e}")
                if fallback_local:
                    self.components = self._detect_components_local(preprocessed)
        else:
            self.components = self._detect_components_local(preprocessed)
        
        # Detect connections
        self.connections = self._detect_connections(preprocessed)
        
        # Save debug images if requested
        if save_debug:
            self._save_debug_images(image, preprocessed)
        
        # Create KiCad components
        self._create_kicad_components(board)
        
        return {
            'components': self.components,
            'connections': self.connections
        }
    
    def _preprocess_image(self, image):
        """Preprocess image for component detection"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 11, 2)
        
        # Perform morphological operations to clean up the image
        kernel = np.ones((3, 3), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def _detect_components_online(self, image):
        """Detect components using online API"""
        # TODO: Implement online detection with FLUX.AI
        raise NotImplementedError("Online detection not yet implemented")
    
    def _detect_components_local(self, image):
        """Detect components using local processing"""
        components = []
        
        # Find contours in the image
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by size
        min_area = 100  # Minimum component area
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
        
        # Process each contour
        for i, contour in enumerate(filtered_contours):
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Simple classification based on aspect ratio and size
            aspect_ratio = float(w) / h if h > 0 else 0
            
            # Determine component type (very basic heuristic)
            if 0.9 < aspect_ratio < 1.1 and w < 50:
                component_type = "capacitor"
            elif aspect_ratio > 2:
                component_type = "resistor"
            elif w > 100 and h > 100:
                component_type = "ic"
            else:
                component_type = "unknown"
            
            # Create component object
            component = {
                'id': i,
                'type': component_type,
                'x': x,
                'y': y,
                'width': w,
                'height': h,
                'contour': contour.tolist()  # Convert to list for JSON serialization
            }
            
            components.append(component)
        
        return components
    
    def _detect_connections(self, image):
        """Detect connections between components"""
        # TODO: Implement connection detection
        return []
    
    def _save_debug_images(self, original, preprocessed):
        """Save debug images"""
        debug_dir = self.config.get('debug_dir', 'debug')
        os.makedirs(debug_dir, exist_ok=True)
        
        # Save original image
        cv2.imwrite(os.path.join(debug_dir, 'original.png'), original)
        
        # Save preprocessed image
        cv2.imwrite(os.path.join(debug_dir, 'preprocessed.png'), preprocessed)
        
        # Create visualization of detected components
        component_vis = original.copy()
        for comp in self.components:
            # Convert contour back to numpy array
            contour = np.array(comp['contour'], dtype=np.int32)
            
            # Draw contour
            cv2.drawContours(component_vis, [contour], 0, (0, 255, 0), 2)
            
            # Draw label
            cv2.putText(component_vis, comp['type'], (comp['x'], comp['y'] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Save component visualization
        cv2.imwrite(os.path.join(debug_dir, 'components.png'), component_vis)
    
    def _create_kicad_components(self, board):
        """Create KiCad components from detected components"""
        # TODO: Implement KiCad component creation
        pass
