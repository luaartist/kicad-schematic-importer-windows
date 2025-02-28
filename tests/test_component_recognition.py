import os
import pytest
import cv2
import numpy as np
from pathlib import Path

def test_component_recognizer():
    """Test that component recognizer can identify components in an image"""
    # Create a test image with a simple component
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.rectangle(image, (20, 20), (40, 40), (255, 255, 255), 2)  # Draw a white rectangle
    
    # Save test image
    test_dir = Path(__file__).parent / "test_files"
    test_dir.mkdir(exist_ok=True)
    test_image_path = test_dir / "test_component.png"
    cv2.imwrite(str(test_image_path), image)
    
    try:
        # Add src directory to Python path
        import sys
        import os
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        
        # Import after adding to path
        from src.recognition.component_recognizer import ComponentRecognizer
        
        # Create recognizer
        recognizer = ComponentRecognizer()
        
        # Load and process test image
        test_image = cv2.imread(str(test_image_path))
        components = recognizer.recognize_components(test_image)
        
        # Verify components were detected
        assert len(components) > 0
        
        # Verify component properties
        component = components[0]
        assert "id" in component
        assert "type" in component
        assert "x" in component
        assert "y" in component
        
        # Verify component position is roughly where we drew it
        assert 15 <= component["x"] <= 45  # Allow some margin for detection
        assert 15 <= component["y"] <= 45
        
    finally:
        # Clean up test file
        if test_image_path.exists():
            test_image_path.unlink()
        if test_dir.exists():
            test_dir.rmdir()

def test_connection_tracer():
    """Test that connection tracer can identify connections between components"""
    # Create a test image with two components and a line connecting them
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    
    # Draw two rectangles (components)
    cv2.rectangle(image, (20, 20), (40, 40), (255, 255, 255), 2)  # Component 1
    cv2.rectangle(image, (120, 120), (140, 140), (255, 255, 255), 2)  # Component 2
    
    # Draw a line connecting them
    cv2.line(image, (40, 30), (120, 130), (255, 255, 255), 2)
    
    # Save test image
    test_dir = Path(__file__).parent / "test_files"
    test_dir.mkdir(exist_ok=True)
    test_image_path = test_dir / "test_connection.png"
    cv2.imwrite(str(test_image_path), image)
    
    try:
        # Add src directory to Python path
        import sys
        import os
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        
        # Import after adding to path
        from src.recognition.component_recognizer import ComponentRecognizer
        from src.recognition.connection_tracer import ConnectionTracer
        
        # Create recognizers
        component_recognizer = ComponentRecognizer()
        connection_tracer = ConnectionTracer()
        
        # Load and process test image
        test_image = cv2.imread(str(test_image_path))
        components = component_recognizer.recognize_components(test_image)
        connections = connection_tracer.trace_connections(test_image, components)
        
        # Verify connections were detected
        assert len(connections) > 0
        
        # Verify connection properties
        connection = connections[0]
        assert "points" in connection
        assert len(connection["points"]) >= 2  # Should have at least start and end points
        
        # Verify connection endpoints are near the components
        start_point = connection["points"][0]
        end_point = connection["points"][-1]
        
        # Check if either endpoint is near component 1
        comp1_near = any(
            15 <= point[0] <= 45 and 15 <= point[1] <= 45
            for point in [start_point, end_point]
        )
        assert comp1_near, "Connection should connect to component 1"
        
        # Check if either endpoint is near component 2
        comp2_near = any(
            115 <= point[0] <= 145 and 115 <= point[1] <= 145
            for point in [start_point, end_point]
        )
        assert comp2_near, "Connection should connect to component 2"
        
    finally:
        # Clean up test files
        if test_image_path.exists():
            test_image_path.unlink()
        if test_dir.exists():
            test_dir.rmdir()
