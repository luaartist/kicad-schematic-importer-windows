"""
Test script for KiCad debug functionality.
This script can be run either:
1. From KiCad's Python Console
2. Using KiCad's Python interpreter
"""

import os
import sys
import cv2
import numpy as np
import logging
from pathlib import Path

def setup_kicad_environment():
    """Setup KiCad environment if running from external Python"""
    try:
        import pcbnew
    except ImportError:
        # Try to add KiCad's Python path
        kicad_paths = [
            r"C:\Program Files\KiCad\9.0\lib\python3.9\site-packages",
            r"C:\Program Files\KiCad\lib\python3.9\site-packages",
            r"C:\Program Files\KiCad\bin\python\site-packages"
        ]
        
        for path in kicad_paths:
            if os.path.exists(path):
                sys.path.append(path)
                print(f"Added KiCad Python path: {path}")
                break
        else:
            print("\nError: Could not find KiCad's Python path.")
            print("Please run this script using one of these methods:")
            print("1. From KiCad PCB Editor > Tools > Python Console:")
            print("   >>> import sys")
            print("   >>> sys.path.append(r'c:/kicad-schematic-importer-windows')")
            print("   >>> import test_debug_kicad")
            print("   >>> test_debug_kicad.test_debug_window()")
            print("\n2. Using KiCad's Python interpreter:")
            print('   "C:\\Program Files\\KiCad\\9.0\\bin\\python.exe" test_debug_kicad.py')
            sys.exit(1)
        
        try:
            import pcbnew
        except ImportError:
            print("\nError: Failed to import pcbnew module.")
            print("Please run this script from KiCad's Python Console")
            sys.exit(1)

def create_test_environment():
    """Create test directories and files"""
    # Get KiCad plugin directory and ensure it exists
    plugin_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'KiCad', '9.0', '3rdparty', 'plugins', 'enhanced_importer_v2')
    if not os.path.exists(plugin_dir):
        print(f"\nError: Plugin directory not found: {plugin_dir}")
        print("Please run install_advanced_plugin.py first")
        return None
    
    # Create test directories
    test_dirs = [
        os.path.join(plugin_dir, 'debug'),
        os.path.join(plugin_dir, 'debug', 'images'),
        os.path.join(plugin_dir, 'test_data')
    ]
    
    for dir_path in test_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")
    
    # Create test image
    test_image = np.ones((400, 600), dtype=np.uint8) * 255  # White background
    
    # Draw test components
    cv2.rectangle(test_image, (100, 100), (200, 150), 0, 2)  # Resistor
    cv2.rectangle(test_image, (300, 200), (350, 250), 0, 2)  # Capacitor
    cv2.line(test_image, (200, 125), (300, 225), 0, 2)  # Connection
    
    # Save test image
    test_image_path = os.path.join(plugin_dir, 'test_data', 'test_schematic.png')
    cv2.imwrite(test_image_path, test_image)
    print(f"\nCreated test schematic: {test_image_path}")
    
    return test_image_path

def test_debug_window():
    """Test the debug window functionality"""
    try:
        # Setup KiCad environment if needed
        setup_kicad_environment()
        
        # Import debug plugin
        plugin_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'KiCad', '9.0', '3rdparty', 'plugins', 'enhanced_importer_v2')
        if plugin_dir not in sys.path:
            sys.path.append(plugin_dir)
        
        import debug_plugin
        debug = debug_plugin.DebugManager.get()
        
        # Create test environment
        test_image_path = create_test_environment()
        if test_image_path is None:
            return
        
        # Show debug window
        debug.show_window()
        debug.log_message("Starting debug test...")
        
        # Load and display test image
        image = cv2.imread(test_image_path)
        if image is None:
            debug.log_message(f"Failed to load test image: {test_image_path}", level=logging.ERROR)
            print(f"\nError: Could not load test image: {test_image_path}")
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
        
        print("\nDebug test completed successfully!")
        print("\nVerify the following:")
        print("1. Debug window appeared and shows component detection")
        print("2. Log messages are displayed in the window")
        print("3. Check debug files in:")
        print(f"   - Log: {os.path.join(plugin_dir, 'debug', 'schematic_importer_debug.log')}")
        print(f"   - Images: {os.path.join(plugin_dir, 'debug', 'images')}")
        
    except Exception as e:
        print(f"\nError during debug test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("\nKiCad Debug Test")
    print("================")
    print("\nThis script can be run in two ways:")
    print("\n1. From KiCad PCB Editor > Tools > Python Console:")
    print("   >>> import sys")
    print("   >>> sys.path.append(r'c:/kicad-schematic-importer-windows')")
    print("   >>> import test_debug_kicad")
    print("   >>> test_debug_kicad.test_debug_window()")
    print("\n2. Using KiCad's Python interpreter:")
    print('   "C:\\Program Files\\KiCad\\9.0\\bin\\python.exe" test_debug_kicad.py')
    
    # If running directly, try to run the test
    test_debug_window()
