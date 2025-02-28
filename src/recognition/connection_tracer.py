#!/usr/bin/env python3
"""
Connection Tracer module for identifying connections between electronic components.
This module provides advanced algorithms for tracing wires and buses in schematic images.
"""

import os
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import networkx as nx

class ConnectionTracer:
    """
    Connection Tracer class that provides methods for identifying connections
    between electronic components in schematic images using various techniques
    including line detection, path finding, and graph algorithms.
    """
    
    def __init__(self):
        """Initialize the connection tracer."""
        self.connection_graph = nx.Graph()
    
    def trace_connections(self, image: np.ndarray, components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Trace connections between components in an image.
        
        Args:
            image: Input image (grayscale or color).
            components: List of recognized components.
        
        Returns:
            List of dictionaries containing traced connections with their
            start and end points, connected components, and path coordinates.
        """
        # Convert to grayscale if it's a color image
        if image.ndim == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply preprocessing
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        
        # Apply morphological operations to enhance lines
        kernel = np.ones((3, 3), np.uint8)
        binary = cv2.dilate(binary, kernel, iterations=1)
        binary = cv2.erode(binary, kernel, iterations=1)
        
        # Detect lines using Hough transform
        lines = self._detect_lines(binary)
        
        # Create a graph representation
        self._build_connection_graph(lines, components)
        
        # Trace connections between components
        connections = self._trace_component_connections(components)
        
        return connections
    
    def _detect_lines(self, binary_image: np.ndarray) -> List[np.ndarray]:
        """
        Detect lines in a binary image using Hough transform.
        
        Args:
            binary_image: Binary input image.
        
        Returns:
            List of detected lines, each represented as [x1, y1, x2, y2].
        """
        # Apply Hough Line Transform
        lines = cv2.HoughLinesP(
            binary_image,
            rho=1,
            theta=np.pi/180,
            threshold=50,
            minLineLength=20,
            maxLineGap=10
        )
        
        if lines is None:
            return []
        
        # Convert lines to [x1, y1, x2, y2] format
        detected_lines = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            detected_lines.append(np.array([x1, y1, x2, y2]))
        
        return detected_lines
    
    def _build_connection_graph(self, lines: List[np.ndarray], components: List[Dict[str, Any]]) -> None:
        """
        Build a graph representation of connections between components.
        
        Args:
            lines: List of detected lines, each represented as [x1, y1, x2, y2].
            components: List of recognized components.
        """
        # Clear the existing graph
        self.connection_graph.clear()
        
        # Add components as nodes
        for component in components:
            self.connection_graph.add_node(
                component["id"],
                type="component",
                data=component
            )
        
        # Add lines as nodes and edges
        for i, line in enumerate(lines):
            x1, y1, x2, y2 = line
            line_id = f"L{i+1}"
            
            # Add line as a node
            self.connection_graph.add_node(
                line_id,
                type="line",
                data={
                    "id": line_id,
                    "start": (x1, y1),
                    "end": (x2, y2)
                }
            )
            
            # Connect line to components
            for component in components:
                x_min, y_min, x_max, y_max = component["bbox"]
                
                # Check if line start point is near or inside component
                if self._is_point_near_component((x1, y1), component):
                    self.connection_graph.add_edge(
                        line_id,
                        component["id"],
                        point=(x1, y1)
                    )
                
                # Check if line end point is near or inside component
                if self._is_point_near_component((x2, y2), component):
                    self.connection_graph.add_edge(
                        line_id,
                        component["id"],
                        point=(x2, y2)
                    )
            
            # Connect lines to other lines (junctions)
            for j, other_line in enumerate(lines):
                if i == j:
                    continue
                
                other_x1, other_y1, other_x2, other_y2 = other_line
                other_line_id = f"L{j+1}"
                
                # Check if lines intersect
                intersection = self._line_intersection(line, other_line)
                if intersection:
                    self.connection_graph.add_edge(
                        line_id,
                        other_line_id,
                        point=intersection
                    )
    
    def _is_point_near_component(self, point: Tuple[int, int], component: Dict[str, Any], margin: int = 5) -> bool:
        """
        Check if a point is near or inside a component.
        
        Args:
            point: Point coordinates (x, y).
            component: Component dictionary.
            margin: Margin around component bounding box.
        
        Returns:
            True if the point is near or inside the component, False otherwise.
        """
        x, y = point
        x_min, y_min, x_max, y_max = component["bbox"]
        
        # Add margin
        x_min -= margin
        y_min -= margin
        x_max += margin
        y_max += margin
        
        return x_min <= x <= x_max and y_min <= y <= y_max
    
    def _line_intersection(self, line1: np.ndarray, line2: np.ndarray, threshold: int = 5) -> Optional[Tuple[int, int]]:
        """
        Find the intersection point of two lines.
        
        Args:
            line1: First line [x1, y1, x2, y2].
            line2: Second line [x1, y1, x2, y2].
            threshold: Distance threshold for considering lines as intersecting.
        
        Returns:
            Intersection point (x, y) or None if lines don't intersect.
        """
        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2
        
        # Check if lines are parallel
        denominator = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        if denominator == 0:
            return None
        
        # Calculate intersection point
        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator
        
        # Check if intersection is within line segments
        if 0 <= ua <= 1 and 0 <= ub <= 1:
            x = int(x1 + ua * (x2 - x1))
            y = int(y1 + ua * (y2 - y1))
            return (x, y)
        
        return None
    
    def _trace_component_connections(self, components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Trace connections between components using the connection graph.
        
        Args:
            components: List of recognized components.
        
        Returns:
            List of dictionaries containing traced connections.
        """
        connections = []
        
        # Find all pairs of connected components
        for i, comp1 in enumerate(components):
            for j, comp2 in enumerate(components):
                if i >= j:
                    continue
                
                # Try to find a path between components
                try:
                    path = nx.shortest_path(
                        self.connection_graph,
                        source=comp1["id"],
                        target=comp2["id"]
                    )
                    
                    # If path exists, create a connection
                    if len(path) > 1:
                        # Extract path coordinates
                        coords = []
                        for k in range(len(path) - 1):
                            edge_data = self.connection_graph.get_edge_data(path[k], path[k+1])
                            if edge_data and "point" in edge_data:
                                coords.append(edge_data["point"])
                        
                        # Create connection dictionary
                        connection = {
                            "id": f"W{len(connections)+1}",
                            "start_component": comp1["id"],
                            "end_component": comp2["id"],
                            "path": path,
                            "coordinates": coords
                        }
                        
                        connections.append(connection)
                except nx.NetworkXNoPath:
                    # No path exists between these components
                    pass
        
        return connections
    
    def detect_buses(self, image: np.ndarray, components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect buses in a schematic image.
        
        Args:
            image: Input image.
            components: List of recognized components.
        
        Returns:
            List of dictionaries containing detected buses.
        """
        # Convert to grayscale if it's a color image
        if image.ndim == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply preprocessing
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        
        # Apply morphological operations to enhance thick lines
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(binary, kernel, iterations=1)
        eroded = cv2.erode(dilated, kernel, iterations=1)
        
        # Find difference (thick lines)
        thick_lines = cv2.subtract(dilated, eroded)
        
        # Detect lines using Hough transform
        lines = cv2.HoughLinesP(
            thick_lines,
            rho=1,
            theta=np.pi/180,
            threshold=50,
            minLineLength=50,
            maxLineGap=10
        )
        
        buses = []
        
        if lines is not None:
            for i, line in enumerate(lines):
                x1, y1, x2, y2 = line[0]
                
                # Create bus dictionary
                bus = {
                    "id": f"B{i+1}",
                    "start": (x1, y1),
                    "end": (x2, y2),
                    "connected_components": []
                }
                
                # Find components connected to this bus
                for component in components:
                    if (self._is_point_near_component((x1, y1), component) or
                        self._is_point_near_component((x2, y2), component)):
                        bus["connected_components"].append(component["id"])
                
                buses.append(bus)
        
        return buses
    
    def visualize_connections(self, image: np.ndarray, components: List[Dict[str, Any]], connections: List[Dict[str, Any]]) -> np.ndarray:
        """
        Visualize connections on the image.
        
        Args:
            image: Input image.
            components: List of recognized components.
            connections: List of traced connections.
        
        Returns:
            Image with visualized connections.
        """
        # Create a copy of the image
        result = image.copy()
        
        # Draw components
        for component in components:
            x_min, y_min, x_max, y_max = component["bbox"]
            cv2.rectangle(result, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(
                result,
                f"{component['id']}: {component['type']}",
                (x_min, y_min - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1
            )
        
        # Draw connections
        for connection in connections:
            if "coordinates" in connection and len(connection["coordinates"]) > 0:
                # Draw path
                coords = connection["coordinates"]
                for i in range(len(coords) - 1):
                    cv2.line(
                        result,
                        coords[i],
                        coords[i+1],
                        (0, 0, 255),
                        2
                    )
            else:
                # Draw direct connection
                comp1_id = connection["start_component"]
                comp2_id = connection["end_component"]
                
                # Find components
                comp1 = next((c for c in components if c["id"] == comp1_id), None)
                comp2 = next((c for c in components if c["id"] == comp2_id), None)
                
                if comp1 and comp2:
                    cv2.line(
                        result,
                        (comp1["x"], comp1["y"]),
                        (comp2["x"], comp2["y"]),
                        (0, 0, 255),
                        2
                    )
        
        return result

# Example usage
if __name__ == "__main__":
    # Create a connection tracer
    tracer = ConnectionTracer()
    
    # Load an image
    image_path = "test_schematic.png"
    if os.path.exists(image_path):
        image = cv2.imread(image_path)
        
        # Example components (normally these would come from a component recognizer)
        components = [
            {
                "id": "C1",
                "type": "resistor",
                "x": 100,
                "y": 100,
                "width": 50,
                "height": 20,
                "bbox": (75, 90, 125, 110)
            },
            {
                "id": "C2",
                "type": "capacitor",
                "x": 200,
                "y": 100,
                "width": 30,
                "height": 30,
                "bbox": (185, 85, 215, 115)
            },
            {
                "id": "C3",
                "type": "ic",
                "x": 150,
                "y": 200,
                "width": 40,
                "height": 40,
                "bbox": (130, 180, 170, 220)
            }
        ]
        
        # Trace connections
        connections = tracer.trace_connections(image, components)
        
        # Visualize connections
        result = tracer.visualize_connections(image, components, connections)
        
        # Save result
        cv2.imwrite("traced_connections.png", result)
        
        # Print traced connections
        for connection in connections:
            print(f"Connection {connection['id']}: {connection['start_component']} -> {connection['end_component']}")
            if "path" in connection:
                print(f"  Path: {' -> '.join(connection['path'])}")
            print()
    else:
        print(f"Image not found: {image_path}")
