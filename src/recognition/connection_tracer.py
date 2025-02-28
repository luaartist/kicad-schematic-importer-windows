import cv2
import numpy as np

class ConnectionTracer:
    """Class for tracing connections between components in images"""
    
    def __init__(self):
        self.min_line_length = 20
        self.max_line_gap = 10
        self.next_id = 1
    
    def trace_connections(self, image, components):
        """Trace connections between components in an image"""
        if image is None or not components:
            return []
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Threshold to get binary image
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Detect lines using HoughLinesP
        lines = cv2.HoughLinesP(
            binary, 
            rho=1,
            theta=np.pi/180,
            threshold=50,
            minLineLength=self.min_line_length,
            maxLineGap=self.max_line_gap
        )
        
        connections = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                
                # Find components connected by this line
                start_component = self._find_nearest_component(x1, y1, components)
                end_component = self._find_nearest_component(x2, y2, components)
                
                if start_component and end_component and start_component != end_component:
                    # Create connection object
                    connection = {
                        "id": f"W{self.next_id}",
                        "start_component": start_component["id"],
                        "end_component": end_component["id"],
                        "points": [(x1, y1), (x2, y2)]
                    }
                    connections.append(connection)
                    self.next_id += 1
        
        return connections
    
    def _find_nearest_component(self, x, y, components):
        """Find the nearest component to a point"""
        nearest = None
        min_dist = float('inf')
        
        for component in components:
            # Calculate distance to component center
            dx = component["x"] - x
            dy = component["y"] - y
            dist = dx*dx + dy*dy  # Square of distance
            
            # Check if point is within component bounds
            half_width = component["width"] // 2
            half_height = component["height"] // 2
            if (abs(dx) <= half_width and abs(dy) <= half_height and dist < min_dist):
                min_dist = dist
                nearest = component
        
        return nearest
