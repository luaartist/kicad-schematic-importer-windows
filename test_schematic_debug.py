"""
Test script to verify the debug functionality in KiCad's Python console.
"""

import os
import sys
import cv2
import numpy as np
import pcbnew
import logging
import logging

def create_test_image():
    """Create a test schematic image"""
    # Create a white background
    image = np.ones((400, 600), dtype=np.uint8) * 255
    
    # Draw some test components
    cv2.rectangle(image, (100, 100), (200, 150), 0, 2)  # Resistor
    cv2.rectangle(image, (300, 200), (350, 250), 0, 2)  # Capacitor
    cv2.line(image, (200, 125), (300, 225), 0, 2)  # Connection
    
    # Save test image
    test_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    os.makedirs(test_dir, exist_ok=True)
    test_image_path = os.path.join(test_dir, 'test_schematic.png')
    cv2.imwrite(test_image_path, image)
    
    return test_image_path

def test_debug_window():
    """Test the debug window functionality"""
    # Create test image
    test_image_path = create_test_image()
    print(f"\nCreated test schematic: {test_image_path}")
    
    # Import debug plugin
    plugin_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'KiCad', '9.0', '3rdparty', 'plugins', 'enhanced_importer_v2')
    if plugin_dir not in sys.path:
        sys.path.append(plugin_dir)
    
    import debug_plugin
    debug = debug_plugin.DebugManager.get()
    
    # Show debug window
    debug.show_window()
    debug.log_message("Starting debug test...")
    
    # Load test image
    image = cv2.imread(test_image_path)
    if image is None:
        debug.log_message(f"Failed to load test image: {test_image_path}", level=logging.ERROR)
        return
    
    # Test image visualization
    debug.update_image(image)
    debug.log_message("Loaded test schematic image")
    
    # Test processing steps
    debug.start_processing()
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    debug.update_image(gray)
    debug.log_message("Converted to grayscale")
    
    # Apply threshold
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    debug.update_image(thresh)
    debug.log_message("Applied threshold")
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    debug.log_message(f"Found {len(contours)} components")
    
    # Draw contours
    result = image.copy()
    cv2.drawContours(result, contours, -1, (0, 255, 0), 2)
    debug.update_image(result)
    debug.log_message("Test complete!")

if __name__ == '__main__':
    print("\nTo test the debug window:")
    print("1. Open KiCad PCB Editor")
    print("2. Go to View → Python Console")
    print("3. Run these commands:")
    print("   >>> import test_schematic_debug")
    print("   >>> test_schematic_debug.test_debug_window()")
