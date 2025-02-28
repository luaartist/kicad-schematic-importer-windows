import cv2
import numpy as np
import os
import json
import pcbnew
import logging
from pathlib import Path
from debug_plugin import DebugManager

class SchematicImporter:
    """Main class for importing schematics from images"""
    
    def __init__(self, config_path=None):
        self.config = self._load_config(config_path)
        self.components = []
        self.connections = []
        self.debug = DebugManager.get()
    
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
        
        # Show debug window and start timing
        self.debug.show_window()
        self.debug.start_processing()
        self.debug.log_message(f"Starting import from {image_path}")
        
        # Merge options with config
        use_online = options.get('use_online', self.config.get('use_online_detection', True))
        fallback_local = options.get('fallback_local', self.config.get('fallback_to_local', True))
        save_debug = options.get('save_debug', self.config.get('save_debug_images', True))
        
        # Load image
        self.debug.log_message("Loading image...")
        image = cv2.imread(image_path)
        if image is None:
            self.debug.log_message(f"Failed to load image: {image_path}", logging.ERROR)
            raise ValueError(f"Could not load image: {image_path}")
        self.debug.log_message(f"Image loaded successfully: {image.shape}")
        
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
        self.debug.log_message("Starting image preprocessing...")
        
        # Convert to grayscale
        self.debug.log_message("Converting to grayscale...")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.debug.update_image(gray)
        
        # Apply Gaussian blur to reduce noise
        self.debug.log_message("Applying Gaussian blur...")
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        self.debug.update_image(blurred)
        
        # Apply adaptive thresholding
        self.debug.log_message("Applying adaptive threshold...")
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 11, 2)
        self.debug.update_image(thresh)
        
        # Perform morphological operations to clean up the image
        self.debug.log_message("Performing morphological operations...")
        kernel = np.ones((3, 3), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        self.debug.update_image(cleaned)
        
        self.debug.log_message("Image preprocessing complete")
        return cleaned
    
    def _detect_components_online(self, image):
        """Detect components using online API"""
        # TODO: Implement online detection with FLUX.AI
        raise NotImplementedError("Online detection not yet implemented")
    
    def _detect_components_local(self, image):
        """Detect components using local processing with improved classification"""
        self.debug.log_message("Starting local component detection...")
        components = []
        component_templates = self.config.get('component_templates', {})
        
        # Find contours in the image
        self.debug.log_message("Finding contours...")
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.debug.log_message(f"Found {len(contours)} initial contours")
        
        # Filter and merge overlapping contours
        min_area = 100  # Minimum component area
        merged_contours = []
        used_contours = set()
        
        for i, contour in enumerate(contours):
            if i in used_contours or cv2.contourArea(contour) < min_area:
                continue
                
            current_contour = contour
            # Check for nearby contours that might be part of the same component
            for j, other_contour in enumerate(contours):
                if i != j and j not in used_contours:
                    x1, y1, w1, h1 = cv2.boundingRect(current_contour)
                    x2, y2, w2, h2 = cv2.boundingRect(other_contour)
                    
                    # If contours are close, merge them
                    if (abs(x1 - x2) < 20 and abs(y1 - y2) < 20):
                        current_contour = np.concatenate([current_contour, other_contour])
                        used_contours.add(j)
            
            merged_contours.append(current_contour)
            used_contours.add(i)
        
        # Process each merged contour
        for i, contour in enumerate(merged_contours):
            # Get bounding rectangle and rotated rectangle
            x, y, w, h = cv2.boundingRect(contour)
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            
            # Calculate features for classification
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            aspect_ratio = float(w) / h if h > 0 else 0
            extent = float(area) / (w * h) if w * h > 0 else 0
            
            # Advanced component classification
            component_type = self._classify_component(area, perimeter, aspect_ratio, extent, w, h)
            
            # Get template data
            template = component_templates.get(component_type, {
                'pins': 2,
                'footprint': 'Resistor_SMD:R_0805_2012Metric'  # Default footprint
            })
            
            # Detect pin locations
            pins = self._detect_pins(image, contour, template['pins'])
            
            # Create component object with additional data
            component = {
                'id': i,
                'type': component_type,
                'x': x,
                'y': y,
                'width': w,
                'height': h,
                'rotation': rect[-1],  # Component rotation angle
                'pins': pins,
                'footprint': template['footprint'],
                'contour': contour.tolist(),  # Convert to list for JSON serialization
                'box': box.tolist()  # Rotated bounding box
            }
            
            components.append(component)
        
        # Remove duplicate components
        unique_components = self._remove_duplicates(components)
        
        return unique_components
    
    def _classify_component(self, area, perimeter, aspect_ratio, extent, width, height):
        """Advanced component classification using multiple features"""
        # Classification rules based on component characteristics
        if 0.9 < aspect_ratio < 1.1 and width < 50:
            if extent > 0.7:  # More filled area suggests capacitor
                return "capacitor"
            else:  # Less filled area suggests connector
                return "connector"
        elif aspect_ratio > 2:
            if extent < 0.6:  # Less filled area suggests resistor
                return "resistor"
            else:  # More filled area suggests diode
                return "diode"
        elif width > 100 and height > 100:
            if extent > 0.8:  # Very filled area suggests IC
                return "ic"
            else:  # Less filled area suggests complex component
                return "transistor"
        elif perimeter / area > 0.1:  # Complex shape suggests transistor
            return "transistor"
        
        return "unknown"
    
    def _detect_pins(self, image, contour, expected_pins):
        """Detect component pin locations"""
        pins = []
        x, y, w, h = cv2.boundingRect(contour)
        
        # Create mask for the component
        mask = np.zeros(image.shape, dtype=np.uint8)
        cv2.drawContours(mask, [contour], 0, 255, -1)
        
        # Detect potential pin locations using Harris corner detection
        corners = cv2.goodFeaturesToTrack(
            image,
            maxCorners=expected_pins * 2,  # Look for more corners than expected pins
            qualityLevel=0.1,
            minDistance=10,
            mask=mask
        )
        
        if corners is not None:
            corners = np.int0(corners)
            
            # Filter corners to match expected pin count
            # Sort by x-coordinate for horizontal components, y-coordinate for vertical
            if w > h:  # Horizontal component
                corners = sorted(corners, key=lambda x: x[0][0])
            else:  # Vertical component
                corners = sorted(corners, key=lambda x: x[0][1])
            
            # Take the outermost corners as pins
            step = len(corners) // expected_pins
            for i in range(0, len(corners), step):
                if len(pins) < expected_pins:
                    x, y = corners[i][0]
                    pins.append({'x': int(x), 'y': int(y)})
        
        # If not enough pins found, generate evenly spaced pins
        while len(pins) < expected_pins:
            if w > h:  # Horizontal component
                x_step = w / (expected_pins + 1)
                new_pin = {
                    'x': int(x + x_step * (len(pins) + 1)),
                    'y': int(y + h/2)
                }
            else:  # Vertical component
                y_step = h / (expected_pins + 1)
                new_pin = {
                    'x': int(x + w/2),
                    'y': int(y + y_step * (len(pins) + 1))
                }
            pins.append(new_pin)
        
        return pins
    
    def _remove_duplicates(self, components):
        """Remove duplicate components based on position and type"""
        unique_components = []
        
        for comp in components:
            # Check if component is too close to any existing component
            is_duplicate = False
            for existing in unique_components:
                if (existing['type'] == comp['type'] and
                    abs(existing['x'] - comp['x']) < 20 and
                    abs(existing['y'] - comp['y']) < 20):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_components.append(comp)
        
        return unique_components
    
    def _detect_connections(self, image):
        """Detect connections between components using line detection"""
        self.debug.log_message("Starting connection detection...")
        connections = []
        
        # Create a copy of the image for line detection
        line_image = image.copy()
        
        # Apply edge detection
        edges = cv2.Canny(line_image, 50, 150, apertureSize=3)
        
        # Use probabilistic Hough transform to detect lines
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi/180,
            threshold=50,
            minLineLength=30,
            maxLineGap=10
        )
        
        if lines is None:
            return connections
            
        # Process detected lines
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            # Find components connected by this line
            start_component = self._find_nearest_component_pin(x1, y1)
            end_component = self._find_nearest_component_pin(x2, y2)
            
            if start_component and end_component and start_component != end_component:
                connection = {
                    'start': {
                        'component_id': start_component['id'],
                        'pin': start_component['pin'],
                        'x': x1,
                        'y': y1
                    },
                    'end': {
                        'component_id': end_component['id'],
                        'pin': end_component['pin'],
                        'x': x2,
                        'y': y2
                    },
                    'points': [[x1, y1], [x2, y2]]
                }
                
                # Check if connection already exists
                if not self._is_duplicate_connection(connection, connections):
                    connections.append(connection)
        
        return connections
    
    def _find_nearest_component_pin(self, x, y, max_distance=20):
        """Find the nearest component pin to a point"""
        nearest = None
        min_dist = float('inf')
        
        for component in self.components:
            for pin_idx, pin in enumerate(component['pins']):
                dist = np.sqrt((pin['x'] - x)**2 + (pin['y'] - y)**2)
                if dist < min_dist and dist < max_distance:
                    min_dist = dist
                    nearest = {
                        'id': component['id'],
                        'pin': pin_idx,
                        'distance': dist
                    }
        
        return nearest
    
    def _is_duplicate_connection(self, new_conn, existing_conns):
        """Check if a connection already exists"""
        for conn in existing_conns:
            # Check both directions
            if ((conn['start']['component_id'] == new_conn['start']['component_id'] and
                 conn['end']['component_id'] == new_conn['end']['component_id']) or
                (conn['start']['component_id'] == new_conn['end']['component_id'] and
                 conn['end']['component_id'] == new_conn['start']['component_id'])):
                return True
        return False
    
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
        self.debug.log_message("Starting KiCad component creation...")
        
        # Set up KiCad board
        if not isinstance(board, pcbnew.BOARD):
            self.debug.log_message("Invalid board object", logging.ERROR)
            raise TypeError("board must be a pcbnew.BOARD instance")
            
        # Load component templates
        templates = self.config.get('component_templates', {})
        
        # Track created components for connections
        created_components = {}
        
        # Create components
        for component in self.components:
            try:
                # Create module (footprint)
                template = templates.get(component['type'], templates['resistor'])
                self.debug.log_message(f"Loading footprint for {component['type']}: {template['footprint']}")
                module = pcbnew.FootprintLoad(
                    pcbnew.FOOTPRINT_LIBRARY_PATH,
                    template['footprint']
                )
                
                if not module:
                    self.debug.log_message(f"Failed to load footprint for {component['type']}", logging.WARNING)
                    continue
                self.debug.log_message(f"Successfully loaded footprint for {component['type']}")
                
                # Set position (convert from pixels to KiCad units)
                pos_x = pcbnew.FromMM(component['x'] / 10)  # Assuming 10 pixels = 1mm
                pos_y = pcbnew.FromMM(component['y'] / 10)
                module.SetPosition(pcbnew.wxPoint(pos_x, pos_y))
                
                # Set rotation
                if 'rotation' in component:
                    module.SetOrientation(component['rotation'] * 10)  # KiCad uses tenths of degrees
                
                # Set reference
                ref = f"{component['type'][0].upper()}{component['id'] + 1}"
                module.SetReference(ref)
                
                # Add to board
                board.Add(module)
                
                # Store for connection creation
                created_components[component['id']] = module
                
            except Exception as e:
                print(f"Error creating component {component['id']}: {e}")
        
        # Create connections (tracks)
        for connection in self.connections:
            try:
                start_comp = created_components.get(connection['start']['component_id'])
                end_comp = created_components.get(connection['end']['component_id'])
                
                if start_comp and end_comp:
                    # Create track
                    self.debug.log_message(f"Creating track between components {connection['start']['component_id']} and {connection['end']['component_id']}")
                    track = pcbnew.PCB_TRACK(board)
                    
                    # Set start point
                    start_pad = start_comp.Pads()[connection['start']['pin']]
                    track.SetStart(start_pad.GetPosition())
                    self.debug.log_message(f"Set track start point at pin {connection['start']['pin']}")
                    
                    # Set end point
                    end_pad = end_comp.Pads()[connection['end']['pin']]
                    track.SetEnd(end_pad.GetPosition())
                    self.debug.log_message(f"Set track end point at pin {connection['end']['pin']}")
                    
                    # Set track width
                    track.SetWidth(pcbnew.FromMM(0.25))  # Default 0.25mm width
                    
                    # Add to board
                    board.Add(track)
                    self.debug.log_message("Track added to board successfully")
                    
            except Exception as e:
                self.debug.log_message(f"Error creating track: {e}", logging.ERROR)
