import os
import pcbnew
import cv2
import numpy as np
from schematic_importer import SchematicImporter

def test_schematic_import():
    """Test function to verify debug functionality"""
    
    # Create test image
    test_image = np.zeros((400, 600), dtype=np.uint8)
    # Draw some test components
    cv2.rectangle(test_image, (100, 100), (200, 150), 255, 2)  # Resistor
    cv2.rectangle(test_image, (300, 200), (350, 250), 255, 2)  # Capacitor
    cv2.line(test_image, (200, 125), (300, 225), 255, 2)  # Connection
    
    # Save test image
    test_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    os.makedirs(test_dir, exist_ok=True)
    test_image_path = os.path.join(test_dir, 'test_schematic.png')
    cv2.imwrite(test_image_path, test_image)
    
    # Create KiCad board
    board = pcbnew.BOARD()
    
    # Create importer with debug enabled
    importer = SchematicImporter()
    
    print("\nStarting schematic import test...")
    print(f"Debug log will be saved to: {os.path.abspath('schematic_importer_debug.log')}")
    print(f"Debug images will be saved to: {os.path.abspath('debug')}\n")
    
    # Import schematic
    result = importer.import_from_image(test_image_path, board)
    
    # Verify results
    print("\nImport Results:")
    print(f"Components detected: {len(result['components'])}")
    print(f"Connections detected: {len(result['connections'])}")
    print("\nCheck the debug window and log files for detailed information")

if __name__ == '__main__':
    test_schematic_import()
