import cv2
import numpy as np

class ConnectionTracer:
    """Traces connections between components in schematic diagrams"""
    
    def __init__(self):
        """Initialize the connection tracer"""
        self.min_line_length = 20  # Minimum line length to consider
        self.line_threshold = 40    # HoughLines parameter
        self.max_gap = 10          # Maximum gap between line segments
    
    def trace_connections(self, image, components):
        """
        Trace connections between components in an image
        
        Args:
            image: OpenCV image (numpy array)
            components: List of detected components
            
        Returns:
            List of connections, where each connection is a dict with:
                - points: List of points [(x1,y1), (x2,y2), ...]
                - from_component: Component ID of source
                - to_component: Component ID of destination
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
            
        # Edge detection
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # Line detection using HoughLinesP for better line segment detection
        lines = cv2.HoughLinesP(
            edges, 
            rho=1, 
            theta=np.pi/180, 
            threshold=self.line_threshold, 
            minLineLength=self.min_line_length,
            maxLineGap=self.max_gap
        )
        
        if lines is None:
            return []
            
        connections = []
        
        # Process each line
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            # Find which components are connected by this line
            from_component = self._find_closest_component(components, x1, y1)
            to_component = self._find_closest_component(components, x2, y2)
            
            # Only add connection if it connects two different components
            if from_component is not None and to_component is not None and from_component != to_component:
                connections.append({
                    'points': [(x1, y1), (x2, y2)],
                    'from_component': from_component["id"],
                    'to_component': to_component["id"]
                })
                
        return connections
    
    def _find_closest_component(self, components, x, y, max_distance=15):
        """Find component closest to the point (x,y)"""
        closest = None
        min_dist = float('inf')
        
        for component in components:
            # Calculate distance from point to component center
            dx = component["x"] - x
            dy = component["y"] - y
            dist = np.sqrt(dx*dx + dy*dy)
            
            if dist < min_dist and dist <= max_distance:
                min_dist = dist
                closest = component
                
        return closest
